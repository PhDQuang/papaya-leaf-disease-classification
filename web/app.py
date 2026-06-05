from __future__ import annotations

import html
import mimetypes
import os
from pathlib import Path
from typing import Any

import gradio as gr
import requests


DEFAULT_API_URL = "http://127.0.0.1:8000"
API_URL = os.getenv("FASTAPI_URL", DEFAULT_API_URL).rstrip("/")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "180"))

CLASS_LABELS = {
    "Anthracnose": "Anthracnose",
    "BacterialSpot": "Bacterial Spot",
    "Curl": "Leaf Curl",
    "Healthy": "Healthy",
    "RingSpot": "Ring Spot",
}


def normalize_class_name(class_name: str | None) -> str:
    if not class_name:
        return "N/A"
    return CLASS_LABELS.get(class_name, class_name)


def format_percent(value: Any) -> str:
    try:
        return f"{float(value) * 100:.2f}%"
    except (TypeError, ValueError):
        return "N/A"


def probability_width(value: Any) -> float:
    try:
        return max(0.0, min(100.0, float(value) * 100.0))
    except (TypeError, ValueError):
        return 0.0


def clean_reason(reason: str | None) -> str:
    if not reason:
        return "N/A"
    return reason.replace("_", " ").strip().capitalize()


def disease_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for item in result.get("disease_list") or []:
        rows.append(
            [
                normalize_class_name(item.get("class")),
                format_percent(item.get("cnn_conf")),
                format_percent(item.get("yolo_conf")),
                f"{float(item.get('score', 0.0)):.4f}",
            ]
        )

    return rows


def crop_rows(result: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for item in result.get("crop_predictions") or []:
        rows.append(
            [
                int(item.get("box_index", 0)) + 1,
                normalize_class_name(item.get("yolo_class")),
                format_percent(item.get("yolo_conf")),
                normalize_class_name(item.get("cnn_class")),
                format_percent(item.get("cnn_conf")),
            ]
        )

    return rows


def status_html(message: str, tone: str = "neutral") -> str:
    return f"""
    <div class="status-card status-{tone}">
        <span class="status-dot"></span>
        <span>{html.escape(message)}</span>
    </div>
    """


def api_status_html(payload: dict[str, Any] | None = None, error: str | None = None) -> str:
    if error:
        return status_html(f"API offline - {error}", "danger")

    if not payload:
        return status_html(f"API endpoint: {API_URL}", "neutral")

    status = str(payload.get("status", "unknown"))
    loaded = bool(payload.get("loaded", False))
    tone = "success" if status == "ok" and loaded else "warning"
    loaded_text = "models loaded" if loaded else "models lazy loaded"
    return status_html(f"API {status} - {loaded_text} - {API_URL}", tone)


def result_html(
    class_name: str | None = None,
    confidence: Any = None,
    reason: str | None = None,
    result: dict[str, Any] | None = None,
) -> str:
    display_class = normalize_class_name(class_name)
    escaped_class = html.escape(display_class)
    escaped_reason = html.escape(clean_reason(reason))
    confidence_text = format_percent(confidence)
    width = probability_width(confidence)
    result = result or {}
    num_boxes = result.get("num_boxes", 0)
    conf_used = result.get("conf_used")
    full_cnn = normalize_class_name(result.get("full_cnn_class"))

    if class_name is None:
        tone = "idle"
        confidence_text = "N/A"
    elif display_class == "Healthy":
        tone = "healthy"
    else:
        tone = "disease"

    return f"""
    <section class="prediction-shell prediction-{tone}">
        <div class="prediction-topline">
            <span class="eyebrow">Prediction</span>
            <span class="result-pill">{escaped_class}</span>
        </div>
        <div class="prediction-main">
            <div>
                <div class="prediction-label">{escaped_class}</div>
                <div class="prediction-reason">{escaped_reason}</div>
            </div>
            <div class="confidence-value">{html.escape(confidence_text)}</div>
        </div>
        <div class="confidence-track">
            <span style="width: {width:.1f}%"></span>
        </div>
        <div class="summary-grid">
            <div>
                <span>Boxes</span>
                <strong>{html.escape(str(num_boxes))}</strong>
            </div>
            <div>
                <span>YOLO conf</span>
                <strong>{format_percent(conf_used)}</strong>
            </div>
            <div>
                <span>Full CNN</span>
                <strong>{html.escape(full_cnn)}</strong>
            </div>
        </div>
    </section>
    """


def check_api() -> tuple[str, dict[str, Any]]:
    try:
        response = requests.get(f"{API_URL}/health", timeout=20)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return api_status_html(error=str(exc)), {}

    return api_status_html(payload), payload


def predict(image_path: str | None) -> tuple[str, list[list[Any]], list[list[Any]], dict[str, Any]]:
    if not image_path:
        raise gr.Error("Please choose an image first.")

    path = Path(image_path)
    if not path.exists():
        raise gr.Error("Uploaded image file was not found.")

    mime_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    try:
        with path.open("rb") as image_file:
            response = requests.post(
                f"{API_URL}/predict",
                files={"file": (path.name, image_file, mime_type)},
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
    except requests.RequestException as exc:
        raise gr.Error(f"Cannot reach FastAPI at {API_URL}: {exc}") from exc

    if response.status_code != 200:
        detail: Any
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise gr.Error(f"FastAPI returned {response.status_code}: {detail}")

    payload = response.json()
    result = payload.get("result") or {}
    pred_class = payload.get("pred_class") or result.get("pred_class")
    confidence = payload.get("confidence")

    return (
        result_html(
            class_name=pred_class,
            confidence=confidence,
            reason=result.get("reason"),
            result=result,
        ),
        disease_rows(result),
        crop_rows(result),
        payload,
    )


CSS = """
:root {
    --leaf: #15803d;
    --leaf-dark: #14532d;
    --leaf-soft: #dcfce7;
    --sky: #2563eb;
    --ink: #172033;
    --muted: #64748b;
    --line: #dbe5ee;
    --surface: #ffffff;
    --canvas: #f5f8fb;
    --warning: #b7791f;
    --danger: #b42318;
}

body,
.gradio-container {
    background: var(--canvas) !important;
    color: var(--ink) !important;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

.gradio-container {
    max-width: 1240px !important;
    padding: 24px 28px 30px !important;
}

.app-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
    padding: 8px 0 22px;
    border-bottom: 1px solid var(--line);
}

.brand-mark {
    width: 42px;
    height: 42px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, var(--leaf), #84cc16);
    color: #ffffff;
    font-weight: 800;
    letter-spacing: 0;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 14px;
}

.app-title {
    margin: 0;
    font-size: 30px;
    line-height: 1.1;
    letter-spacing: 0;
    color: var(--ink);
}

.app-subtitle {
    margin: 6px 0 0;
    color: var(--muted);
    font-size: 14px;
}

.model-stack {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 8px;
}

.chip {
    display: inline-flex;
    align-items: center;
    min-height: 30px;
    padding: 0 11px;
    border: 1px solid var(--line);
    border-radius: 999px;
    background: #ffffff;
    color: #334155;
    font-size: 13px;
    font-weight: 650;
}

.workspace-row {
    margin-top: 22px;
    align-items: stretch;
}

.surface {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.07);
    padding: 18px !important;
}

.surface-title {
    margin: 0 0 14px;
    color: var(--muted);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.upload-surface .image-container,
.upload-surface [data-testid="image"] {
    border-radius: 8px !important;
}

.upload-surface .wrap {
    border-color: var(--line) !important;
}

.actions-row {
    margin-top: 14px;
}

.primary-action,
.secondary-action {
    min-height: 48px !important;
    border-radius: 8px !important;
    font-weight: 750 !important;
}

.primary-action {
    background: var(--leaf) !important;
    border-color: var(--leaf) !important;
}

.secondary-action {
    background: #eef4fb !important;
    border-color: #cddbea !important;
    color: #1f2937 !important;
}

.status-card {
    display: flex;
    align-items: center;
    gap: 10px;
    min-height: 44px;
    padding: 10px 12px;
    border-radius: 8px;
    background: #f8fafc;
    border: 1px solid var(--line);
    color: #334155;
    font-size: 14px;
    font-weight: 650;
    overflow-wrap: anywhere;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    flex: 0 0 auto;
    background: #94a3b8;
}

.status-success .status-dot { background: var(--leaf); }
.status-warning .status-dot { background: var(--warning); }
.status-danger .status-dot { background: var(--danger); }

.prediction-shell {
    margin-top: 16px;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 18px;
    background: #ffffff;
}

.prediction-healthy {
    border-color: #bbf7d0;
    background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 74%);
}

.prediction-disease {
    border-color: #fed7aa;
    background: linear-gradient(180deg, #fff7ed 0%, #ffffff 74%);
}

.prediction-topline,
.prediction-main {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
}

.eyebrow {
    color: var(--muted);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.result-pill {
    padding: 5px 10px;
    border-radius: 999px;
    background: var(--leaf-soft);
    color: var(--leaf-dark);
    font-size: 12px;
    font-weight: 800;
}

.prediction-disease .result-pill {
    background: #ffedd5;
    color: #9a3412;
}

.prediction-main {
    margin-top: 18px;
}

.prediction-label {
    font-size: 32px;
    line-height: 1;
    font-weight: 850;
    color: var(--ink);
    letter-spacing: 0;
}

.prediction-reason {
    margin-top: 8px;
    color: var(--muted);
    font-size: 14px;
}

.confidence-value {
    min-width: 104px;
    text-align: right;
    color: var(--leaf-dark);
    font-size: 28px;
    font-weight: 850;
}

.prediction-disease .confidence-value {
    color: #9a3412;
}

.confidence-track {
    height: 9px;
    margin-top: 18px;
    overflow: hidden;
    border-radius: 999px;
    background: #e2e8f0;
}

.confidence-track span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, var(--leaf), #65a30d);
}

.prediction-disease .confidence-track span {
    background: linear-gradient(90deg, #f97316, #dc2626);
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin-top: 16px;
}

.summary-grid div {
    min-height: 70px;
    padding: 11px 12px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: #f8fafc;
}

.summary-grid span {
    display: block;
    color: var(--muted);
    font-size: 12px;
    font-weight: 750;
}

.summary-grid strong {
    display: block;
    margin-top: 7px;
    color: var(--ink);
    font-size: 15px;
    overflow-wrap: anywhere;
}

.table-surface {
    margin-top: 18px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: 0 14px 40px rgba(15, 23, 42, 0.05);
    padding: 10px 14px 16px !important;
}

.table-surface table {
    font-size: 14px !important;
}

.table-surface th {
    background: #f8fafc !important;
    color: #334155 !important;
    font-weight: 800 !important;
}

.footer {
    display: none !important;
}

@media (max-width: 900px) {
    .app-header,
    .prediction-main {
        align-items: flex-start;
        flex-direction: column;
    }

    .model-stack {
        justify-content: flex-start;
    }

    .confidence-value {
        min-width: 0;
        text-align: left;
    }

    .summary-grid {
        grid-template-columns: 1fr;
    }
}
"""


HEADER_HTML = """
<header class="app-header">
    <div class="brand-row">
        <div class="brand-mark">PL</div>
        <div>
            <h1 class="app-title">Papaya Leaf Disease Classification</h1>
            <p class="app-subtitle">YOLOv11m detection and EfficientNetB2 classification</p>
        </div>
    </div>
    <div class="model-stack">
        <span class="chip">YOLOv11m</span>
        <span class="chip">EfficientNetB2</span>
        <span class="chip">FastAPI</span>
    </div>
</header>
"""


with gr.Blocks(
    title="Papaya Leaf Disease Classification",
    theme=gr.themes.Soft(primary_hue="green", neutral_hue="slate"),
    css=CSS,
) as demo:
    gr.HTML(HEADER_HTML)

    with gr.Row(equal_height=True, elem_classes=["workspace-row"]):
        with gr.Column(scale=7, elem_classes=["surface", "upload-surface"]):
            gr.HTML('<p class="surface-title">Input image</p>')
            image_input = gr.Image(
                label="Leaf image",
                type="filepath",
                sources=["upload"],
                height=440,
            )
            with gr.Row(elem_classes=["actions-row"]):
                predict_button = gr.Button("Predict", variant="primary", elem_classes=["primary-action"])
                health_button = gr.Button("Check API", elem_classes=["secondary-action"])

        with gr.Column(scale=5, elem_classes=["surface", "result-surface"]):
            gr.HTML('<p class="surface-title">Model output</p>')
            api_status = gr.HTML(api_status_html())
            result_output = gr.HTML(result_html())

    with gr.Group(elem_classes=["table-surface"]):
        with gr.Tabs():
            with gr.Tab("Disease scores"):
                disease_table = gr.Dataframe(
                    headers=["Class", "CNN confidence", "YOLO confidence", "Score"],
                    datatype=["str", "str", "str", "str"],
                    interactive=False,
                    wrap=True,
                )
            with gr.Tab("Crop predictions"):
                crop_table = gr.Dataframe(
                    headers=["Box", "YOLO class", "YOLO confidence", "CNN class", "CNN confidence"],
                    datatype=["number", "str", "str", "str", "str"],
                    interactive=False,
                    wrap=True,
                )
            with gr.Tab("Raw response"):
                raw_output = gr.JSON(label="FastAPI response")

    predict_button.click(
        fn=predict,
        inputs=image_input,
        outputs=[
            result_output,
            disease_table,
            crop_table,
            raw_output,
        ],
    )
    health_button.click(fn=check_api, inputs=None, outputs=[api_status, raw_output])


if __name__ == "__main__":
    host = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    print(f"Open the Gradio UI at http://localhost:{port} or http://127.0.0.1:{port}")
    demo.launch(server_name=host, server_port=port)
