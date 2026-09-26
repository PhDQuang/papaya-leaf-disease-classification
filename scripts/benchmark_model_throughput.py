from __future__ import annotations

import argparse
import csv
import json
import shutil
import statistics
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


VALID_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

CNN_IMAGE_SIZES = {
    "efficientnet_b0": 224,
    "efficientnet_b1": 240,
    "efficientnet_b2": 260,
    "EfficientNetB0": 224,
    "EfficientNetB1": 240,
    "EfficientNetB2": 260,
}

CNN_CLASS_NAMES = ["Anthracnose", "BacterialSpot", "Curl", "Healthy", "RingSpot"]

PROJECT_NAME = "Papaya_Leaf_Disease_Classification"


@dataclass(frozen=True)
class ModelSpec:
    kind: str
    alias: str
    path: Path


def looks_like_project_root(path: Path) -> bool:
    return (
        (path / "prepared_data_v1").exists()
        or (path / "outputs").exists()
        or (path / "Model").exists()
    ) and (
        (path / "prepared_data_v1").exists()
        or (path / "README.md").exists()
        or (path / "Code").exists()
    )


def find_project_root(manual_root: Path | None = None) -> Path:
    if manual_root is not None:
        root = manual_root.expanduser().resolve()
        if root.exists():
            return root
        raise FileNotFoundError(f"Project root does not exist: {root}")

    # Xử lý an toàn cho môi trường Colab/Jupyter (nơi không có __file__)
    try:
        script_path = Path(__file__).resolve()
        base_parents = list(script_path.parents)
        default_return = base_parents[1] if len(base_parents) > 1 else script_path
    except NameError:
        script_path = Path.cwd().resolve()
        base_parents = [script_path]
        default_return = script_path

    candidates = [
        *base_parents,
        Path.cwd().resolve(),
        *Path.cwd().resolve().parents,
        Path("/content/drive/MyDrive") / PROJECT_NAME,
    ]

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists() and looks_like_project_root(candidate):
            return candidate

    shortcut_root = Path("/content/drive/.shortcut-targets-by-id")
    if shortcut_root.exists():
        for candidate in shortcut_root.rglob(PROJECT_NAME):
            if candidate.is_dir() and looks_like_project_root(candidate):
                return candidate

    return default_return


def is_image(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in VALID_IMAGE_EXTS


def list_images(folder: Path) -> list[Path]:
    return sorted(path for path in folder.rglob("*") if is_image(path))


def load_images_from_csv(csv_path: Path) -> list[Path]:
    rows: list[Path] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return rows

        path_columns = ["image_path", "path", "filepath", "file", "filename"]
        column = next((name for name in path_columns if name in reader.fieldnames), None)
        if column is None:
            raise ValueError(
                f"CSV must contain one of these image path columns: {', '.join(path_columns)}"
            )

        for row in reader:
            value = (row.get(column) or "").strip()
            if not value:
                continue
            path = Path(value)
            if not path.is_absolute():
                path = (csv_path.parent / path).resolve()
            if is_image(path):
                rows.append(path)
    return rows


def default_images(root: Path) -> list[Path]:
    manifest_candidates = [
        root / "Model" / "Pipeline_Evaluation" / "pipeline_test_manifest.csv",
        root / "outputs" / "pipeline_evaluation" / "pipeline_test_manifest.csv",
    ]
    for manifest_path in manifest_candidates:
        if manifest_path.exists():
            images = load_images_from_csv(manifest_path)
            if images:
                print(f"Using default image manifest: {manifest_path}")
                return images

    yolo_test = root / "prepared_data_v1" / "yolo_dataset" / "images" / "test"
    healthy_test = root / "prepared_data_v1" / "cnn_dataset" / "test" / "Healthy"
    combined = []
    if yolo_test.exists():
        combined.extend(list_images(yolo_test))
    if healthy_test.exists():
        combined.extend(list_images(healthy_test))
    if combined:
        print(f"Using default Colab test folders under: {root / 'prepared_data_v1'}")
        return sorted(combined)

    folder_candidates = [
        root / "prepared_data_v1" / "cnn_dataset" / "test",
        root / "data" / "processed",
        root / "readme",
    ]
    for folder in folder_candidates:
        if folder.exists():
            images = list_images(folder)
            if images:
                print(f"Using default image source: {folder}")
                return images

    return []


def resolve_images(source: Path | None, limit: int | None, root: Path) -> list[Path]:
    if source is not None:
        source = source.expanduser()
        if not source.is_absolute():
            source = (root / source).resolve()
        else:
            source = source.resolve()
        if source.is_dir():
            images = list_images(source)
        elif source.is_file() and source.suffix.lower() == ".csv":
            images = load_images_from_csv(source)
        elif is_image(source):
            images = [source]
        else:
            raise FileNotFoundError(f"No readable images found at: {source}")
    else:
        images = default_images(root)

    if limit is not None and limit > 0:
        images = images[:limit]

    if not images:
        raise FileNotFoundError(
            "No images found. Pass --images with a folder, an image file, or a CSV containing image_path."
        )

    return images


def should_use_local_image_cache(root: Path, value: str) -> bool:
    if value == "always":
        return True
    if value == "never":
        return False
    return root.as_posix().startswith("/content/drive")


def copy_images_to_local_cache(images: list[Path], cache_dir: Path) -> list[Path]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached_images = []
    start = time.perf_counter()

    for index, image_path in enumerate(images):
        safe_stem = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in image_path.stem)
        dst = cache_dir / f"{index:06d}_{safe_stem}{image_path.suffix.lower()}"
        shutil.copy2(image_path, dst)
        cached_images.append(dst)

    elapsed = time.perf_counter() - start
    print(f"Copied {len(cached_images)} images to local cache: {cache_dir}")
    print(f"Image copy time, not counted in benchmark: {elapsed:.3f}s")
    return cached_images


def parse_model_arg(value: str, kind: str) -> ModelSpec:
    if "=" in value:
        alias, raw_path = value.split("=", 1)
        alias = alias.strip()
        path = Path(raw_path.strip()).expanduser().resolve()
    else:
        path = Path(value).expanduser().resolve()
        alias = path.parent.parent.name if kind == "yolo" else path.parent.name

    if not alias:
        raise ValueError(f"Missing alias in model argument: {value}")
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    return ModelSpec(kind=kind, alias=alias, path=path)


def discover_yolo_models(root: Path) -> list[ModelSpec]:
    specs = []
    seen_aliases: set[str] = set()

    search_roots = [
        root / "Model" / "YOLOv11",
        root / "outputs" / "yolo",
    ]
    for search_root in search_roots:
        for pattern in ["*/weights/best.pt", "*/weights/last.pt"]:
            for weights_path in sorted(search_root.glob(pattern)):
                alias = weights_path.parents[1].name
                if alias in seen_aliases:
                    continue
                seen_aliases.add(alias)
                specs.append(ModelSpec(kind="yolo", alias=alias, path=weights_path))
    return specs


def discover_cnn_models(root: Path) -> list[ModelSpec]:
    specs = []
    seen_aliases: set[str] = set()

    search_roots = [
        root / "Model" / "CNN",
        root / "outputs" / "cnn",
    ]
    priority_names = [
        "best_model.keras",
        "best_stage2.keras",
        "last_stage2.keras",
        "best_stage1.keras",
        "last_stage1.keras",
    ]
    for search_root in search_roots:
        for run_dir in sorted(path for path in search_root.glob("*") if path.is_dir()):
            if run_dir.name in {"reports", "__pycache__"} or run_dir.name in seen_aliases:
                continue
            for filename in priority_names:
                model_path = run_dir / filename
                if model_path.exists():
                    specs.append(ModelSpec(kind="cnn", alias=run_dir.name, path=model_path))
                    seen_aliases.add(run_dir.name)
                    break
    return specs


def batches(items: list[Path], batch_size: int) -> list[list[Path]]:
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def sync_torch_if_needed(device: int | str) -> None:
    try:
        import torch

        if device != "cpu" and torch.cuda.is_available():
            torch.cuda.synchronize()
    except Exception:
        pass


def auto_torch_device(device_arg: str) -> int | str:
    if device_arg != "auto":
        return device_arg

    import torch

    return 0 if torch.cuda.is_available() else "cpu"


def summarize_timings(
    *,
    kind: str,
    alias: str,
    model_path: Path,
    num_images: int,
    elapsed_seconds: float,
    load_seconds: float,
    extra: dict[str, Any] | None = None,
    timed_units: list[float] | None = None,
) -> dict[str, Any]:
    images_per_second = num_images / elapsed_seconds if elapsed_seconds > 0 else 0.0
    row = {
        "kind": kind,
        "alias": alias,
        "model_path": str(model_path),
        "num_images": num_images,
        "elapsed_seconds": elapsed_seconds,
        "images_per_second": images_per_second,
        "milliseconds_per_image": (elapsed_seconds / num_images) * 1000.0,
        "model_load_seconds": load_seconds,
    }
    if extra:
        row.update(extra)
    if timed_units:
        unit_ms = [value * 1000.0 for value in timed_units]
        row.update(
            {
                "timed_units": len(unit_ms),
                "min_unit_ms": min(unit_ms),
                "median_unit_ms": statistics.median(unit_ms),
                "max_unit_ms": max(unit_ms),
                "p90_unit_ms": statistics.quantiles(unit_ms, n=10)[8]
                if len(unit_ms) >= 10
                else max(unit_ms),
                "p95_unit_ms": statistics.quantiles(unit_ms, n=20)[18]
                if len(unit_ms) >= 20
                else max(unit_ms),
            }
        )
    return row


def benchmark_yolo(spec: ModelSpec, images: list[Path], args: argparse.Namespace) -> dict[str, Any]:
    from ultralytics import YOLO

    device = auto_torch_device(args.device)
    load_start = time.perf_counter()
    model = YOLO(str(spec.path))
    load_seconds = time.perf_counter() - load_start

    warmup_images = images[: max(0, min(args.warmup, len(images)))]
    for image_path in warmup_images:
        model.predict(
            source=str(image_path),
            imgsz=args.yolo_imgsz,
            conf=args.yolo_conf,
            iou=args.yolo_iou,
            device=device,
            verbose=False,
        )
    sync_torch_if_needed(device)

    start = time.perf_counter()
    total_boxes = 0
    per_image_seconds = []
    for image_path in images:
        image_start = time.perf_counter()
        results = model.predict(
            source=str(image_path),
            imgsz=args.yolo_imgsz,
            conf=args.yolo_conf,
            iou=args.yolo_iou,
            device=device,
            verbose=False,
        )
        per_image_seconds.append(time.perf_counter() - image_start)
        if results and results[0].boxes is not None:
            total_boxes += len(results[0].boxes)
    sync_torch_if_needed(device)
    elapsed = time.perf_counter() - start

    return summarize_timings(
        kind="yolo",
        alias=spec.alias,
        model_path=spec.path,
        num_images=len(images),
        elapsed_seconds=elapsed,
        load_seconds=load_seconds,
        extra={
            "device": str(device),
            "batch_size": 1,
            "imgsz": args.yolo_imgsz,
            "total_boxes": total_boxes,
            "average_boxes_per_image": total_boxes / len(images),
        },
        timed_units=per_image_seconds,
    )


def load_cnn_batch(image_paths: list[Path], image_size: int) -> Any:
    import numpy as np
    from PIL import Image

    arrays = []
    for image_path in image_paths:
        with Image.open(image_path) as image:
            image = image.convert("RGB").resize((image_size, image_size))
            arrays.append(np.asarray(image, dtype="float32"))
    return np.stack(arrays, axis=0)


def benchmark_cnn(spec: ModelSpec, images: list[Path], args: argparse.Namespace) -> dict[str, Any]:
    from tensorflow import keras

    image_size = args.cnn_img_size or CNN_IMAGE_SIZES.get(spec.alias, 260)

    load_start = time.perf_counter()
    model = keras.models.load_model(str(spec.path), compile=False)
    load_seconds = time.perf_counter() - load_start

    image_batches = batches(images, max(1, args.cnn_batch_size))
    warmup_batches = image_batches[: max(0, min(args.warmup, len(image_batches)))]
    for batch_paths in warmup_batches:
        batch = load_cnn_batch(batch_paths, image_size)
        model.predict(batch, verbose=0)

    start = time.perf_counter()
    per_batch_seconds = []
    for batch_paths in image_batches:
        batch_start = time.perf_counter()
        batch = load_cnn_batch(batch_paths, image_size)
        model.predict(batch, verbose=0)
        per_batch_seconds.append(time.perf_counter() - batch_start)
    elapsed = time.perf_counter() - start

    return summarize_timings(
        kind="cnn",
        alias=spec.alias,
        model_path=spec.path,
        num_images=len(images),
        elapsed_seconds=elapsed,
        load_seconds=load_seconds,
        extra={
            "device": "tensorflow-default",
            "batch_size": args.cnn_batch_size,
            "imgsz": image_size,
        },
        timed_units=[
            seconds / len(batch_paths)
            for seconds, batch_paths in zip(per_batch_seconds, image_batches, strict=True)
        ],
    )


def benchmark_cascade(
    yolo_spec: ModelSpec,
    cnn_spec: ModelSpec,
    images: list[Path],
    args: argparse.Namespace,
) -> dict[str, Any]:
    import numpy as np
    from PIL import Image
    from tensorflow import keras
    from ultralytics import YOLO

    device = auto_torch_device(args.device)
    image_size = args.cnn_img_size or CNN_IMAGE_SIZES.get(cnn_spec.alias, 260)

    load_start = time.perf_counter()
    yolo_model = YOLO(str(yolo_spec.path))
    cnn_model = keras.models.load_model(str(cnn_spec.path), compile=False)
    load_seconds = time.perf_counter() - load_start

    def predict_yolo_boxes(image_path: Path, conf: float) -> list[list[float]]:
        results = yolo_model.predict(
            source=str(image_path),
            imgsz=args.yolo_imgsz,
            conf=conf,
            iou=args.yolo_iou,
            device=device,
            verbose=False,
        )
        if results and results[0].boxes is not None:
            return results[0].boxes.xyxy.detach().cpu().numpy().tolist()
        return []

    def run_cnn_on_full_image(image: Image.Image) -> tuple[str, float]:
        full_image = image.resize((image_size, image_size))
        batch = np.expand_dims(np.asarray(full_image, dtype="float32"), axis=0)
        probs = cnn_model.predict(batch, verbose=0)[0]
        pred_id = int(np.argmax(probs))
        return CNN_CLASS_NAMES[pred_id], float(probs[pred_id])

    def expanded_box(
        box: list[float],
        image_width: int,
        image_height: int,
        expand_ratio: float,
    ) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = box
        bw = x2 - x1
        bh = y2 - y1
        ex = bw * expand_ratio
        ey = bh * expand_ratio

        x1 = max(0, min(int(round(x1 - ex)), image_width - 1))
        y1 = max(0, min(int(round(y1 - ey)), image_height - 1))
        x2 = max(1, min(int(round(x2 + ex)), image_width))
        y2 = max(1, min(int(round(y2 + ey)), image_height))
        if x2 <= x1:
            x2 = min(image_width, x1 + 1)
        if y2 <= y1:
            y2 = min(image_height, y1 + 1)
        return x1, y1, x2, y2

    def run_one(image_path: Path) -> tuple[int, int]:
        boxes = predict_yolo_boxes(image_path, args.yolo_conf)
        conf_retries = 0

        with Image.open(image_path) as image:
            image = image.convert("RGB")

            if not boxes:
                full_cls, full_conf = run_cnn_on_full_image(image)
                should_retry = (
                    full_cls != "Healthy"
                    and full_conf >= args.full_cnn_disease_min_prob
                    and args.yolo_conf_min < args.yolo_conf
                    and args.yolo_conf_step > 0
                )
                if should_retry:
                    conf = args.yolo_conf - args.yolo_conf_step
                    while conf >= args.yolo_conf_min - 1e-9:
                        conf_retries += 1
                        boxes = predict_yolo_boxes(image_path, round(conf, 3))
                        if boxes:
                            break
                        conf -= args.yolo_conf_step

                if not boxes:
                    return 0, conf_retries

            if boxes:
                crops = []
                width, height = image.size
                for box in boxes:
                    x1, y1, x2, y2 = expanded_box(box, width, height, args.bbox_expand_ratio)
                    if (x2 - x1) < args.min_crop_size or (y2 - y1) < args.min_crop_size:
                        continue
                    crop = image.crop((x1, y1, x2, y2)).resize((image_size, image_size))
                    crops.append(np.asarray(crop, dtype="float32"))
                if crops:
                    cnn_model.predict(np.stack(crops, axis=0), verbose=0)

        return len(boxes), conf_retries

    for image_path in images[: max(0, min(args.warmup, len(images)))]:
        run_one(image_path)
    sync_torch_if_needed(device)

    start = time.perf_counter()
    total_boxes = 0
    total_conf_retries = 0
    per_image_seconds = []
    for image_path in images:
        image_start = time.perf_counter()
        box_count, conf_retries = run_one(image_path)
        per_image_seconds.append(time.perf_counter() - image_start)
        total_boxes += box_count
        total_conf_retries += conf_retries
    sync_torch_if_needed(device)
    elapsed = time.perf_counter() - start

    return summarize_timings(
        kind="cascade",
        alias=f"{yolo_spec.alias}__{cnn_spec.alias}",
        model_path=yolo_spec.path,
        num_images=len(images),
        elapsed_seconds=elapsed,
        load_seconds=load_seconds,
        extra={
            "cnn_model_path": str(cnn_spec.path),
            "device": str(device),
            "batch_size": 1,
            "imgsz": f"yolo={args.yolo_imgsz};cnn={image_size}",
            "total_boxes": total_boxes,
            "average_boxes_per_image": total_boxes / len(images),
            "total_conf_retries": total_conf_retries,
            "bbox_expand_ratio": args.bbox_expand_ratio,
        },
        timed_units=per_image_seconds,
    )


def write_outputs(rows: list[dict[str, Any]], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = output_dir / f"model_throughput_{stamp}.csv"
    json_path = output_dir / f"model_throughput_{stamp}.json"

    fieldnames = sorted({key for row in rows for key in row.keys()})
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2, ensure_ascii=False)

    return csv_path, json_path


def print_table(rows: list[dict[str, Any]]) -> None:
    print("\nThroughput summary")
    print("-" * 96)
    print(
        f"{'kind':<10} {'alias':<34} {'images':>8} {'img/s':>12} "
        f"{'ms/img':>12} {'median':>10} {'p95':>10} {'load s':>10}"
    )
    print("-" * 96)
    for row in rows:
        print(
            f"{row['kind']:<10} "
            f"{row['alias']:<34} "
            f"{row['num_images']:>8} "
            f"{row['images_per_second']:>12.3f} "
            f"{row['milliseconds_per_image']:>12.3f} "
            f"{float(row.get('median_unit_ms', 0.0)):>10.3f} "
            f"{float(row.get('p95_unit_ms', 0.0)):>10.3f} "
            f"{row['model_load_seconds']:>10.3f}"
        )
    print("-" * 96)

    speeds = [float(row["images_per_second"]) for row in rows]
    if len(speeds) > 1:
        print(f"Mean img/s across rows: {statistics.mean(speeds):.3f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark image throughput for local YOLO, CNN, and optional cascade models."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Project root. On Colab this is usually /content/drive/MyDrive/Papaya_Leaf_Disease_Classification.",
    )
    parser.add_argument(
        "--images",
        type=Path,
        default=None,
        help="Folder, image file, or CSV with image_path column. Defaults to prepared_data_v1 or readme images.",
    )
    parser.add_argument("--limit", type=int, default=100, help="Maximum images to benchmark. Use 0 for all.")
    parser.add_argument("--warmup", type=int, default=3, help="Warmup images/batches before timing.")
    parser.add_argument(
        "--local-image-cache",
        choices=["auto", "always", "never"],
        default="auto",
        help="Copy benchmark images to local runtime storage before timing. Auto enables this on Colab Drive.",
    )
    parser.add_argument(
        "--local-image-cache-dir",
        type=Path,
        default=Path("/content/papaya_benchmark_images"),
        help="Local image cache folder used when --local-image-cache is enabled.",
    )
    parser.add_argument(
        "--benchmarks",
        nargs="+",
        choices=["yolo", "cnn", "cascade", "all"],
        default=["yolo", "cnn"],
        help="Which benchmarks to run. Cascade tests every discovered YOLO x CNN pair.",
    )
    parser.add_argument(
        "--yolo-model",
        action="append",
        default=[],
        help="YOLO model path, or alias=path. Can be repeated. Defaults to Model/YOLOv11 or outputs/yolo checkpoints.",
    )
    parser.add_argument(
        "--cnn-model",
        action="append",
        default=[],
        help="CNN model path, or alias=path. Can be repeated. Defaults to Model/CNN or outputs/cnn checkpoints.",
    )
    parser.add_argument("--device", default="auto", help="YOLO device: auto, cpu, 0, 1, etc.")
    parser.add_argument("--yolo-imgsz", type=int, default=832)
    parser.add_argument("--yolo-conf", type=float, default=0.50)
    parser.add_argument("--yolo-conf-min", type=float, default=0.35)
    parser.add_argument("--yolo-conf-step", type=float, default=0.05)
    parser.add_argument("--yolo-iou", type=float, default=0.70)
    parser.add_argument("--full-cnn-disease-min-prob", type=float, default=0.50)
    parser.add_argument("--bbox-expand-ratio", type=float, default=0.10)
    parser.add_argument("--min-crop-size", type=int, default=8)
    parser.add_argument("--cnn-img-size", type=int, default=None, help="Override CNN input size.")
    parser.add_argument("--cnn-batch-size", type=int, default=16)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Where to write CSV/JSON benchmark results. Defaults to FinalOutput/Performance_Benchmark under the project root.",
    )
    parser.add_argument("--no-write", action="store_true", help="Print results only; do not write files.")

    # Bỏ qua tham số `-f` (hoặc các tham số hệ thống khác của Colab/Jupyter)
    args, unknown = parser.parse_known_args()
    return args


def main() -> None:
    args = parse_args()
    root = find_project_root(args.project_root)
    selected = set(args.benchmarks)
    if "all" in selected:
        selected = {"yolo", "cnn", "cascade"}

    limit = None if args.limit == 0 else args.limit
    images = resolve_images(args.images, limit=limit, root=root)
    if should_use_local_image_cache(root, args.local_image_cache):
        images = copy_images_to_local_cache(images, args.local_image_cache_dir.expanduser())

    yolo_specs = (
        [parse_model_arg(value, "yolo") for value in args.yolo_model]
        if args.yolo_model
        else discover_yolo_models(root)
    )
    cnn_specs = (
        [parse_model_arg(value, "cnn") for value in args.cnn_model]
        if args.cnn_model
        else discover_cnn_models(root)
    )

    rows: list[dict[str, Any]] = []
    print(f"Project root     : {root}")
    print(f"Benchmark images: {len(images)}")

    if "yolo" in selected:
        if not yolo_specs:
            print("No YOLO models found. Skipping YOLO benchmark.")
        for spec in yolo_specs:
            print(f"Benchmarking YOLO: {spec.alias}")
            rows.append(benchmark_yolo(spec, images, args))

    if "cnn" in selected:
        if not cnn_specs:
            print("No CNN models found. Skipping CNN benchmark.")
        for spec in cnn_specs:
            print(f"Benchmarking CNN: {spec.alias}")
            rows.append(benchmark_cnn(spec, images, args))

    if "cascade" in selected:
        if not yolo_specs or not cnn_specs:
            print("Need both YOLO and CNN models for cascade benchmark. Skipping cascade.")
        for yolo_spec in yolo_specs:
            for cnn_spec in cnn_specs:
                print(f"Benchmarking cascade: {yolo_spec.alias} + {cnn_spec.alias}")
                rows.append(benchmark_cascade(yolo_spec, cnn_spec, images, args))

    if not rows:
        raise RuntimeError("No benchmark rows were produced.")

    print_table(rows)
    if not args.no_write:
        if args.output_dir is not None:
            output_dir = args.output_dir.expanduser()
            if not output_dir.is_absolute():
                output_dir = (root / output_dir).resolve()
            else:
                output_dir = output_dir.resolve()
        elif (root / "FinalOutput").exists() or root.as_posix().startswith("/content/drive"):
            output_dir = root / "FinalOutput" / "Performance_Benchmark"
        else:
            output_dir = root / "outputs" / "performance_benchmark"

        csv_path, json_path = write_outputs(rows, output_dir)
        print(f"\nSaved CSV : {csv_path}")
        print(f"Saved JSON: {json_path}")


if __name__ == "__main__":
    main()