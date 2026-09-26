from __future__ import annotations

import csv
import html
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from generate_experimental_results_runtime_slide import (
    COLORS,
    SLIDE_H,
    SLIDE_W,
    Slide,
    content_types,
    presentation_xml,
    rels_xml,
    slide_layout_xml,
    slide_master_xml,
    theme_xml,
)


OUT_DIR = Path("outputs/conference_presentation")
PPTX_PATH = OUT_DIR / "per_class_results_slide.pptx"
NOTES_PATH = OUT_DIR / "per_class_results_notes_vi.md"
DATA_PATH = Path(
    "outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/accuracy_by_class.csv"
)

CLASS_COLORS = {
    "Anthracnose": COLORS["green"],
    "BacterialSpot": COLORS["blue"],
    "Curl": COLORS["amber"],
    "Healthy": COLORS["cyan"],
    "RingSpot": COLORS["red"],
}

DISPLAY_NAMES = {
    "Anthracnose": "Anthracnose",
    "BacterialSpot": "Bacterial Spot",
    "Curl": "Curl",
    "Healthy": "Healthy",
    "RingSpot": "Ring Spot",
}


def load_rows() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    with DATA_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "class_name": row["true_class"],
                    "support": int(row["num_samples"]),
                    "correct": int(row["num_correct"]),
                    "recall": float(row["accuracy"]) * 100.0,
                }
            )

    expected = list(DISPLAY_NAMES)
    actual = [str(row["class_name"]) for row in rows]
    if actual != expected:
        raise ValueError(f"Unexpected class order: {actual}; expected {expected}")
    return rows


def build_slide(rows: list[dict[str, float | int | str]]) -> str:
    slide = Slide()

    slide.rect(0, 0, 4.45, 0.66, fill=COLORS["muted"], line=None)
    slide.text(
        "IV. Experimental Results",
        0.78,
        0.12,
        3.25,
        0.34,
        size=20,
        color=COLORS["white"],
        bold=True,
        anchor="mid",
        font="Aptos Display",
    )

    slide.text(
        "Performance remains balanced across all five classes",
        0.72,
        0.92,
        11.7,
        0.48,
        size=25,
        color=COLORS["dark"],
        bold=True,
        font="Aptos Display",
    )
    slide.text(
        "Best end-to-end cascade: YOLOv11m + EfficientNet-B2 | Image-level test set: n = 291",
        0.75,
        1.39,
        11.4,
        0.28,
        size=11,
        color=COLORS["muted"],
    )

    slide.rect(0.72, 1.82, 7.55, 4.87, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    slide.text("Class recall", 1.0, 2.03, 2.2, 0.25, size=14, color=COLORS["dark"], bold=True)
    slide.text("Correct / support", 6.92, 2.03, 1.05, 0.25, size=10, color=COLORS["muted"], bold=True, align="ctr")
    slide.text("90%", 2.58, 2.31, 0.45, 0.22, size=8, color=COLORS["muted"])
    slide.text("95%", 4.53, 2.31, 0.45, 0.22, size=8, color=COLORS["muted"], align="ctr")
    slide.text("100%", 6.43, 2.31, 0.45, 0.22, size=8, color=COLORS["muted"], align="r")

    row_y = 2.67
    row_gap = 0.71
    track_x = 2.62
    track_w = 3.82
    for index, row in enumerate(rows):
        class_name = str(row["class_name"])
        recall = float(row["recall"])
        correct = int(row["correct"])
        support = int(row["support"])
        color = CLASS_COLORS[class_name]
        y = row_y + index * row_gap

        slide.text(
            DISPLAY_NAMES[class_name],
            1.0,
            y - 0.03,
            1.45,
            0.28,
            size=11,
            color=COLORS["dark"],
            bold=class_name == "Curl",
            anchor="mid",
        )
        slide.rect(track_x, y + 0.04, track_w, 0.18, fill=COLORS["gray"], line=None, preset="roundRect")
        bar_w = track_w * max(0.0, min(1.0, (recall - 90.0) / 10.0))
        slide.rect(track_x, y + 0.04, bar_w, 0.18, fill=color, line=None, preset="roundRect")
        slide.text(
            f"{recall:.2f}%",
            6.52,
            y - 0.04,
            0.65,
            0.3,
            size=11,
            color=color,
            bold=True,
            align="r",
            anchor="mid",
        )
        slide.text(
            f"{correct}/{support}",
            7.22,
            y - 0.04,
            0.72,
            0.3,
            size=11,
            color=COLORS["dark"],
            bold=True,
            align="ctr",
            anchor="mid",
        )

    slide.text(
        "Axis shown from 90% to 100% to make the small between-class differences visible.",
        1.0,
        6.30,
        6.9,
        0.22,
        size=8,
        color=COLORS["muted"],
    )

    slide.rect(8.62, 1.82, 3.98, 4.87, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    slide.text("Balanced, despite unequal support", 8.94, 2.06, 3.34, 0.36, size=15, color=COLORS["dark"], bold=True, font="Aptos Display")

    slide.shape_text(
        "ALL FIVE CLASSES\n>= 93.75% recall",
        8.96,
        2.64,
        3.20,
        0.86,
        COLORS["light_green"],
        line=COLORS["green"],
        size=15,
        color=COLORS["green"],
        bold=True,
        align="ctr",
    )
    slide.shape_text(
        "Macro F1\n94.92%",
        8.96,
        3.75,
        1.48,
        0.86,
        COLORS["light_blue"],
        line=COLORS["blue"],
        size=13,
        color=COLORS["blue"],
        bold=True,
    )
    slide.shape_text(
        "Support range\n34-80 images",
        10.68,
        3.75,
        1.48,
        0.86,
        COLORS["light_amber"],
        line=COLORS["amber"],
        size=13,
        color=COLORS["dark"],
        bold=True,
    )
    slide.text(
        "The strongest class is Curl (98.15%). The lowest is Ring Spot (93.75%), leaving only a 4.40-point spread.",
        8.96,
        4.92,
        3.20,
        0.88,
        size=11,
        color=COLORS["muted"],
    )
    slide.text(
        "Takeaway: the aggregate score is not driven by one majority class.",
        8.96,
        5.92,
        3.20,
        0.50,
        size=12,
        color=COLORS["green"],
        bold=True,
    )

    slide.rect(0.55, 7.18, 12.25, 0.01, fill=COLORS["line"], line=None)
    slide.text(
        "Papaya leaf disease detection and classification | Per-class results",
        0.58,
        7.22,
        8.0,
        0.18,
        size=8,
        color=COLORS["muted"],
    )
    return slide.xml()


def core_xml() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Per-Class Results</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{html.escape(now)}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{html.escape(now)}</dcterms:modified>
</cp:coreProperties>
"""


def app_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex PPTX Generator</Application>
  <PresentationFormat>On-screen Show (16:9)</PresentationFormat>
  <Slides>1</Slides>
</Properties>
"""


def notes(rows: list[dict[str, float | int | str]]) -> str:
    details = "\n".join(
        f"- {DISPLAY_NAMES[str(row['class_name'])]}: {int(row['correct'])}/{int(row['support'])}, "
        f"recall {float(row['recall']):.2f}%."
        for row in rows
    )
    return f"""# Slide 24 - Per-Class Results

## Lời trình bày đề xuất

Ở slide này, chúng tôi kiểm tra kết quả theo từng lớp để bảo đảm rằng độ chính xác tổng thể không chỉ đến từ một lớp có nhiều mẫu. Vì mẫu số là số ảnh thật của từng lớp, chỉ số ở đây được gọi chính xác là class recall.

{details}

Tất cả năm lớp đều đạt recall ít nhất 93.75 phần trăm, mặc dù số mẫu hỗ trợ dao động từ 34 đến 80 ảnh. Curl đạt cao nhất với 98.15 phần trăm, trong khi Ring Spot thấp nhất với 93.75 phần trăm. Khoảng cách giữa lớp cao nhất và thấp nhất chỉ là 4.40 điểm phần trăm. Kết hợp với macro F1 bằng 94.92 phần trăm, kết quả này cho thấy mô hình duy trì hiệu năng tương đối cân bằng giữa các lớp, thay vì chỉ tối ưu cho lớp chiếm ưu thế.

## Câu chuyển slide

Từ kết quả tổng thể và kết quả theo lớp, chúng tôi rút ra các kết luận chính và định hướng phát triển tiếp theo.
"""


def write_pptx() -> None:
    rows = load_rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PPTX_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types())
        archive.writestr(
            "_rels/.rels",
            rels_xml(
                [
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
                    ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
                    ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties", "docProps/app.xml"),
                ]
            ),
        )
        archive.writestr("docProps/core.xml", core_xml())
        archive.writestr("docProps/app.xml", app_xml())
        archive.writestr("ppt/presentation.xml", presentation_xml())
        archive.writestr(
            "ppt/_rels/presentation.xml.rels",
            rels_xml(
                [
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml"),
                    ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", "slides/slide1.xml"),
                    ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "theme/theme1.xml"),
                ]
            ),
        )
        archive.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml())
        archive.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            rels_xml(
                [
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
                    ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
                ]
            ),
        )
        archive.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml())
        archive.writestr(
            "ppt/slideLayouts/_rels/slideLayout1.xml.rels",
            rels_xml(
                [
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml"),
                ]
            ),
        )
        archive.writestr("ppt/theme/theme1.xml", theme_xml())
        archive.writestr("ppt/slides/slide1.xml", build_slide(rows))
        archive.writestr(
            "ppt/slides/_rels/slide1.xml.rels",
            rels_xml(
                [
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
                ]
            ),
        )

    NOTES_PATH.write_text(notes(rows), encoding="utf-8")
    print(PPTX_PATH)
    print(NOTES_PATH)


if __name__ == "__main__":
    write_pptx()
