from __future__ import annotations

import logging
import os
import re
import tempfile
import threading
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("papaya-api")

YOLO_DRIVE_ID = "11AGUogBofR0hayelb804A_2SqZwGmwCW"
CNN_DRIVE_ID = "1pxd6ORKrs7qhEDsfaTlLKWqMWnLKi0cj"

YOLO_CLASS_NAMES = ["Anthracnose", "BacterialSpot", "Curl", "RingSpot"]
CNN_CLASS_NAMES = ["Anthracnose", "BacterialSpot", "Curl", "Healthy", "RingSpot"]
ALL_CLASS_NAMES = CNN_CLASS_NAMES

YOLO_ID_TO_CLASS = {i: name for i, name in enumerate(YOLO_CLASS_NAMES)}
CNN_ID_TO_CLASS = {i: name for i, name in enumerate(CNN_CLASS_NAMES)}

VALID_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def resolve_project_root() -> Path:
    explicit = os.getenv("PROJECT_ROOT")
    if explicit:
        return Path(explicit).expanduser().resolve()

    cwd = Path.cwd().resolve()
    for candidate in [cwd, *Path(__file__).resolve().parents]:
        if (candidate / "README.md").exists() and (
            (candidate / "outputs").exists() or (candidate / "api").exists()
        ):
            return candidate

    return cwd


def path_env(name: str, default: Path) -> Path:
    value = os.getenv(name)
    if value:
        return Path(value).expanduser().resolve()
    return default.resolve()


@dataclass(frozen=True)
class Settings:
    project_root: Path
    yolo_model_path: Path
    cnn_model_path: Path
    yolo_drive_source: str
    cnn_drive_source: str
    auto_download_models: bool
    load_models_on_startup: bool
    yolo_imgsz: int
    yolo_iou: float
    yolo_conf_start: float
    yolo_conf_min: float
    yolo_conf_step: float
    full_cnn_disease_min_prob: float
    bbox_expand_ratio: float
    min_crop_size: int
    cnn_img_size: int
    agg_method: str


def load_settings() -> Settings:
    project_root = resolve_project_root()
    return Settings(
        project_root=project_root,
        yolo_model_path=path_env(
            "YOLO_MODEL_PATH",
            project_root / "outputs" / "yolo" / "yolov11_m" / "weights" / "best.pt",
        ),
        cnn_model_path=path_env(
            "CNN_MODEL_PATH",
            project_root / "outputs" / "cnn" / "efficientnet_b2" / "best_model.keras",
        ),
        yolo_drive_source=os.getenv("YOLO_DRIVE_SOURCE", YOLO_DRIVE_ID),
        cnn_drive_source=os.getenv("CNN_DRIVE_SOURCE", CNN_DRIVE_ID),
        auto_download_models=bool_env("MODEL_AUTO_DOWNLOAD", True),
        load_models_on_startup=bool_env("LOAD_MODELS_ON_STARTUP", True),
        yolo_imgsz=int(os.getenv("YOLO_IMGSZ", "832")),
        yolo_iou=float(os.getenv("YOLO_IOU", "0.70")),
        yolo_conf_start=float(os.getenv("YOLO_CONF_START", "0.50")),
        yolo_conf_min=float(os.getenv("YOLO_CONF_MIN", "0.35")),
        yolo_conf_step=float(os.getenv("YOLO_CONF_STEP", "0.05")),
        full_cnn_disease_min_prob=float(os.getenv("FULL_CNN_DISEASE_MIN_PROB", "0.50")),
        bbox_expand_ratio=float(os.getenv("BBOX_EXPAND_RATIO", "0.10")),
        min_crop_size=int(os.getenv("MIN_CROP_SIZE", "8")),
        cnn_img_size=int(os.getenv("CNN_IMG_SIZE", "260")),
        agg_method=os.getenv("AGG_METHOD", "weighted").strip().lower(),
    )


settings = load_settings()


@dataclass
class ModelBundle:
    yolo: Any
    cnn: Any
    torch_device: int | str


model_lock = threading.Lock()
model_bundle: ModelBundle | None = None
model_error: str | None = None

app = FastAPI(
    title="Papaya Leaf Disease Classification API",
    version="1.0.0",
)


def extract_drive_id(source: str) -> str:
    source = source.strip()
    match = re.search(r"/d/([^/?#]+)", source)
    if match:
        return match.group(1)

    match = re.search(r"[?&]id=([^&#]+)", source)
    if match:
        return match.group(1)

    return source


def download_drive_file(source: str, output_path: Path) -> None:
    try:
        import gdown
    except ImportError as exc:
        raise RuntimeError("Install gdown or set MODEL_AUTO_DOWNLOAD=false.") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_name(f"{output_path.name}.download")
    if tmp_path.exists():
        tmp_path.unlink()

    logger.info("Downloading Google Drive file to %s", output_path)
    if "drive.google.com" in source:
        result = gdown.download(url=source, output=str(tmp_path), quiet=False, fuzzy=True)
    else:
        result = gdown.download(id=extract_drive_id(source), output=str(tmp_path), quiet=False)

    if result is None or not tmp_path.exists() or tmp_path.stat().st_size == 0:
        raise RuntimeError(
            "Google Drive download failed. Make sure the file sharing is set to anyone with the link."
        )

    tmp_path.replace(output_path)


def ensure_model_file(path: Path, drive_source: str, label: str) -> None:
    if path.exists() and path.stat().st_size > 0:
        return

    if not settings.auto_download_models:
        raise FileNotFoundError(
            f"{label} model not found at {path}. Set MODEL_AUTO_DOWNLOAD=true or provide the file."
        )

    download_drive_file(drive_source, path)


def ensure_model_files() -> None:
    ensure_model_file(settings.yolo_model_path, settings.yolo_drive_source, "YOLOv11m")
    ensure_model_file(settings.cnn_model_path, settings.cnn_drive_source, "EfficientNetB2")


def load_model_bundle() -> ModelBundle:
    ensure_model_files()

    import torch
    from tensorflow import keras
    from ultralytics import YOLO

    torch_device: int | str = 0 if torch.cuda.is_available() else "cpu"
    logger.info("Loading YOLO model from %s", settings.yolo_model_path)
    yolo_model = YOLO(str(settings.yolo_model_path))

    logger.info("Loading CNN model from %s", settings.cnn_model_path)
    cnn_model = keras.models.load_model(str(settings.cnn_model_path), compile=False)

    return ModelBundle(yolo=yolo_model, cnn=cnn_model, torch_device=torch_device)


def get_model_bundle() -> ModelBundle:
    global model_bundle, model_error

    if model_bundle is not None:
        return model_bundle

    with model_lock:
        if model_bundle is not None:
            return model_bundle

        try:
            model_bundle = load_model_bundle()
            model_error = None
            return model_bundle
        except Exception as exc:
            model_error = str(exc)
            logger.exception("Model load failed")
            raise


@app.on_event("startup")
def startup() -> None:
    if not settings.load_models_on_startup:
        return

    try:
        get_model_bundle()
    except Exception:
        logger.warning("Startup completed without loaded models. /predict will retry on request.")


def model_file_status() -> dict[str, Any]:
    return {
        "yolo": {
            "path": str(settings.yolo_model_path),
            "exists": settings.yolo_model_path.exists(),
            "size_bytes": settings.yolo_model_path.stat().st_size
            if settings.yolo_model_path.exists()
            else 0,
        },
        "cnn": {
            "path": str(settings.cnn_model_path),
            "exists": settings.cnn_model_path.exists(),
            "size_bytes": settings.cnn_model_path.stat().st_size
            if settings.cnn_model_path.exists()
            else 0,
        },
    }


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "Papaya Leaf Disease Classification API",
        "predict": "POST /predict with form-data field 'file'",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    loaded = model_bundle is not None
    return {
        "status": "ok" if loaded else "degraded",
        "loaded": loaded,
        "last_model_error": model_error,
        "models": model_file_status(),
    }


@app.get("/models")
def models() -> dict[str, Any]:
    return {
        "classes": ALL_CLASS_NAMES,
        "yolo_classes": YOLO_CLASS_NAMES,
        "cnn_classes": CNN_CLASS_NAMES,
        "settings": {
            "project_root": str(settings.project_root),
            "yolo_imgsz": settings.yolo_imgsz,
            "yolo_iou": settings.yolo_iou,
            "yolo_conf_start": settings.yolo_conf_start,
            "yolo_conf_min": settings.yolo_conf_min,
            "yolo_conf_step": settings.yolo_conf_step,
            "cnn_img_size": settings.cnn_img_size,
            "agg_method": settings.agg_method,
        },
        "files": model_file_status(),
    }


def load_pil_rgb(image_path: Path) -> Image.Image:
    return Image.open(image_path).convert("RGB")


def clamp_box(x1: float, y1: float, x2: float, y2: float, w: int, h: int) -> tuple[int, int, int, int]:
    x1 = max(0, min(int(round(x1)), w - 1))
    y1 = max(0, min(int(round(y1)), h - 1))
    x2 = max(1, min(int(round(x2)), w))
    y2 = max(1, min(int(round(y2)), h))

    if x2 <= x1:
        x2 = min(w, x1 + 1)
    if y2 <= y1:
        y2 = min(h, y1 + 1)

    return x1, y1, x2, y2


def expand_xyxy(
    box: list[float],
    image_w: int,
    image_h: int,
    expand_ratio: float,
) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    bw = x2 - x1
    bh = y2 - y1
    ex = bw * expand_ratio
    ey = bh * expand_ratio
    return clamp_box(x1 - ex, y1 - ey, x2 + ex, y2 + ey, image_w, image_h)


def crop_from_box(
    pil_img: Image.Image,
    box_xyxy: list[float],
    expand_ratio: float,
) -> tuple[Image.Image | None, tuple[int, int, int, int]]:
    w, h = pil_img.size
    x1, y1, x2, y2 = expand_xyxy(box_xyxy, w, h, expand_ratio)

    if (x2 - x1) < settings.min_crop_size or (y2 - y1) < settings.min_crop_size:
        return None, (x1, y1, x2, y2)

    return pil_img.crop((x1, y1, x2, y2)), (x1, y1, x2, y2)


def probs_to_named_list(probs: list[float]) -> list[dict[str, float | str]]:
    return [
        {"class": class_name, "probability": float(prob)}
        for class_name, prob in zip(CNN_CLASS_NAMES, probs, strict=True)
    ]


def cnn_predict_pil(cnn_model: Any, pil_img: Image.Image) -> tuple[str, float, list[float]]:
    img = pil_img.resize((settings.cnn_img_size, settings.cnn_img_size))
    arr = np.asarray(img).astype("float32")
    arr = np.expand_dims(arr, axis=0)

    probs = cnn_model.predict(arr, verbose=0)[0]
    probs = np.asarray(probs, dtype="float32")
    pred_id = int(np.argmax(probs))
    pred_class = CNN_ID_TO_CLASS[pred_id]
    pred_conf = float(probs[pred_id])

    return pred_class, pred_conf, probs.astype(float).tolist()


def yolo_detect_once(bundle: ModelBundle, image_path: Path, conf: float) -> list[dict[str, Any]]:
    results = bundle.yolo.predict(
        source=str(image_path),
        imgsz=settings.yolo_imgsz,
        conf=conf,
        iou=settings.yolo_iou,
        device=bundle.torch_device,
        verbose=False,
    )

    result = results[0]
    boxes: list[dict[str, Any]] = []

    if result.boxes is None or len(result.boxes) == 0:
        return boxes

    for box in result.boxes:
        xyxy = box.xyxy.detach().cpu().numpy()[0].tolist()
        cls_id = int(box.cls.detach().cpu().numpy()[0])
        yolo_conf = float(box.conf.detach().cpu().numpy()[0])

        if cls_id not in YOLO_ID_TO_CLASS:
            continue

        boxes.append(
            {
                "xyxy": [float(v) for v in xyxy],
                "yolo_class_id": cls_id,
                "yolo_class": YOLO_ID_TO_CLASS[cls_id],
                "yolo_conf": yolo_conf,
            }
        )

    return sorted(boxes, key=lambda item: item["yolo_conf"], reverse=True)


def conf_sequence(start: float, min_conf: float, step: float) -> list[float]:
    values = []
    conf = start
    while conf >= min_conf - 1e-9:
        values.append(round(conf, 3))
        conf -= step
    return values


def aggregate_crop_predictions(crop_preds: list[dict[str, Any]]) -> tuple[str, dict[str, float], list[dict[str, float | str]]]:
    if len(crop_preds) == 0:
        return "Healthy", {}, []

    scores = {class_name: 0.0 for class_name in ALL_CLASS_NAMES}

    if settings.agg_method == "majority":
        votes = Counter([pred["cnn_class"] for pred in crop_preds])
        max_vote = max(votes.values())
        candidates = [class_name for class_name, count in votes.items() if count == max_vote]

        weighted_scores: defaultdict[str, float] = defaultdict(float)
        for pred in crop_preds:
            weighted_scores[pred["cnn_class"]] += pred["cnn_conf"] * pred["yolo_conf"]

        pred_class = sorted(
            candidates,
            key=lambda class_name: weighted_scores.get(class_name, 0.0),
            reverse=True,
        )[0]

        for class_name, count in votes.items():
            scores[class_name] = float(count)
    else:
        for pred in crop_preds:
            scores[pred["cnn_class"]] += float(pred["cnn_conf"]) * float(pred["yolo_conf"])

        pred_class = max(scores, key=scores.get)

    disease_list = []
    for pred in crop_preds:
        if pred["cnn_class"] != "Healthy":
            disease_list.append(
                {
                    "class": pred["cnn_class"],
                    "cnn_conf": float(pred["cnn_conf"]),
                    "yolo_conf": float(pred["yolo_conf"]),
                    "score": float(pred["cnn_conf"]) * float(pred["yolo_conf"]),
                }
            )

    return pred_class, scores, sorted(disease_list, key=lambda item: item["score"], reverse=True)


def run_hybrid_on_image(image_path: Path, bundle: ModelBundle) -> dict[str, Any]:
    pil_img = load_pil_rgb(image_path)
    result: dict[str, Any] = {
        "pred_class": None,
        "reason": None,
        "num_boxes": 0,
        "conf_used": None,
        "full_cnn_class": None,
        "full_cnn_conf": None,
        "full_cnn_probs": None,
        "boxes": [],
        "crop_predictions": [],
        "final_scores": {},
        "disease_list": [],
    }

    boxes = yolo_detect_once(bundle, image_path, conf=settings.yolo_conf_start)
    conf_used = settings.yolo_conf_start

    if len(boxes) == 0:
        full_cls, full_conf, full_probs = cnn_predict_pil(bundle.cnn, pil_img)
        result["full_cnn_class"] = full_cls
        result["full_cnn_conf"] = full_conf
        result["full_cnn_probs"] = probs_to_named_list(full_probs)

        if full_cls == "Healthy" or full_conf < settings.full_cnn_disease_min_prob:
            result["pred_class"] = "Healthy"
            result["reason"] = "no_yolo_box_full_cnn_healthy_or_low_conf"
            result["conf_used"] = settings.yolo_conf_start
            return result

        retry_confs = conf_sequence(
            start=settings.yolo_conf_start - settings.yolo_conf_step,
            min_conf=settings.yolo_conf_min,
            step=settings.yolo_conf_step,
        )

        for conf in retry_confs:
            boxes = yolo_detect_once(bundle, image_path, conf=conf)
            if len(boxes) > 0:
                conf_used = conf
                break

        if len(boxes) == 0:
            result["pred_class"] = "Healthy"
            result["reason"] = "no_yolo_box_after_conf_retry"
            result["conf_used"] = settings.yolo_conf_min
            return result

    crop_preds = []
    for idx, box in enumerate(boxes):
        crop_img, expanded_box = crop_from_box(
            pil_img,
            box["xyxy"],
            expand_ratio=settings.bbox_expand_ratio,
        )

        if crop_img is None:
            continue

        cnn_cls, cnn_conf, cnn_probs = cnn_predict_pil(bundle.cnn, crop_img)
        crop_preds.append(
            {
                "box_index": idx,
                "xyxy": [float(v) for v in box["xyxy"]],
                "expanded_xyxy": [float(v) for v in expanded_box],
                "yolo_class": box["yolo_class"],
                "yolo_conf": float(box["yolo_conf"]),
                "cnn_class": cnn_cls,
                "cnn_conf": float(cnn_conf),
                "cnn_probs": probs_to_named_list(cnn_probs),
            }
        )

    if len(crop_preds) == 0:
        result["pred_class"] = "Healthy"
        result["reason"] = "boxes_exist_but_all_crops_invalid"
        result["num_boxes"] = len(boxes)
        result["conf_used"] = conf_used
        result["boxes"] = boxes
        return result

    final_cls, final_scores, disease_list = aggregate_crop_predictions(crop_preds)

    result["pred_class"] = final_cls
    result["reason"] = f"yolo_boxes_cnn_{settings.agg_method}_vote"
    result["num_boxes"] = len(boxes)
    result["conf_used"] = conf_used
    result["boxes"] = boxes
    result["crop_predictions"] = crop_preds
    result["final_scores"] = final_scores
    result["disease_list"] = disease_list

    return result


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict[str, Any]:
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in VALID_IMAGE_EXTS:
        suffix = ".jpg"

    try:
        bundle = get_model_bundle()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Models are not ready: {exc}") from exc

    with tempfile.TemporaryDirectory() as tmpdir:
        image_path = Path(tmpdir) / f"upload{suffix}"
        image_path.write_bytes(image_bytes)

        try:
            with Image.open(image_path) as img:
                img.verify()
        except (UnidentifiedImageError, OSError) as exc:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.") from exc

        result = run_hybrid_on_image(image_path, bundle)

    return {
        "filename": file.filename,
        "pred_class": result["pred_class"],
        "confidence": max(result.get("final_scores", {}).values(), default=result.get("full_cnn_conf") or 0.0),
        "result": result,
    }
