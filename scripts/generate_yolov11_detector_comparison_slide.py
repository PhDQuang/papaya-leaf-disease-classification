from __future__ import annotations

import csv
import html
import zipfile
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("outputs/conference_presentation")
PPTX_PATH = OUT_DIR / "yolov11_detector_comparison_slide.pptx"
NOTES_PATH = OUT_DIR / "yolov11_detector_comparison_notes.md"
CSV_PATH = Path("outputs/yolo/reports/final_yolo_comparison.csv")

SLIDE_W = 12_192_000
SLIDE_H = 6_858_000
EMU = 914_400

COLORS = {
    "bg": "F8FAF7",
    "dark": "17231A",
    "muted": "5B6B5F",
    "green": "2E7D55",
    "blue": "2F6FB6",
    "cyan": "39A6A3",
    "amber": "E8A13A",
    "red": "C94A45",
    "light_green": "E6F2EA",
    "light_blue": "E7F0FA",
    "light_amber": "FFF3DE",
    "line": "CAD7CC",
    "white": "FFFFFF",
    "gray": "EEF2EE",
}


def emu(value: float) -> int:
    return int(value * EMU)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def run_props(size: int, color: str, bold: bool = False, font: str = "Aptos") -> str:
    bold_attr = ' b="1"' if bold else ""
    return (
        f'<a:rPr lang="en-US" sz="{size * 100}"{bold_attr}>'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="{font}"/><a:ea typeface="{font}"/><a:cs typeface="{font}"/>'
        f"</a:rPr>"
    )


def text_body(
    text: str,
    size: int = 18,
    color: str = COLORS["dark"],
    bold: bool = False,
    align: str = "l",
    anchor: str = "t",
    font: str = "Aptos",
) -> str:
    para_xml = []
    for paragraph in text.split("\n"):
        para_xml.append(
            f'<a:p><a:pPr algn="{align}"/>'
            f"<a:r>{run_props(size, color, bold, font)}<a:t>{esc(paragraph)}</a:t></a:r>"
            f"</a:p>"
        )
    return (
        f'<p:txBody><a:bodyPr wrap="square" anchor="{anchor}" lIns="80000" '
        f'rIns="80000" tIns="50000" bIns="50000"><a:spAutoFit/></a:bodyPr>'
        f"<a:lstStyle/>{''.join(para_xml)}</p:txBody>"
    )


class Slide:
    def __init__(self) -> None:
        self.items: list[str] = []
        self.next_id = 2
        self.rect(0, 0, 13.333, 7.5, fill=COLORS["bg"], line=None)

    def _id(self) -> int:
        shape_id = self.next_id
        self.next_id += 1
        return shape_id

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str | None = COLORS["white"],
        line: str | None = COLORS["line"],
        preset: str = "rect",
    ) -> None:
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else "<a:noFill/>"
        line_xml = (
            f'<a:ln w="11000"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
            if line
            else "<a:ln><a:noFill/></a:ln>"
        )
        self.items.append(
            f"""
            <p:sp>
              <p:nvSpPr><p:cNvPr id="{self._id()}" name="Shape"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
                <a:prstGeom prst="{preset}"><a:avLst/></a:prstGeom>
                {fill_xml}
                {line_xml}
              </p:spPr>
            </p:sp>
            """
        )

    def text(
        self,
        text: str,
        x: float,
        y: float,
        w: float,
        h: float,
        size: int = 18,
        color: str = COLORS["dark"],
        bold: bool = False,
        align: str = "l",
        anchor: str = "t",
        font: str = "Aptos",
    ) -> None:
        self.items.append(
            f"""
            <p:sp>
              <p:nvSpPr><p:cNvPr id="{self._id()}" name="TextBox"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                <a:noFill/><a:ln><a:noFill/></a:ln>
              </p:spPr>
              {text_body(text, size=size, color=color, bold=bold, align=align, anchor=anchor, font=font)}
            </p:sp>
            """
        )

    def shape_text(
        self,
        text: str,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str,
        line: str | None = COLORS["line"],
        size: int = 12,
        color: str = COLORS["dark"],
        bold: bool = False,
        align: str = "ctr",
        anchor: str = "mid",
        preset: str = "roundRect",
    ) -> None:
        self.rect(x, y, w, h, fill=fill, line=line, preset=preset)
        self.text(text, x + 0.04, y + 0.03, w - 0.08, h - 0.06, size, color, bold, align, anchor)

    def metric(self, value: str, label: str, x: float, y: float, w: float, h: float, color: str) -> None:
        self.rect(x, y, w, h, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
        self.rect(x, y, 0.08, h, fill=color, line=None)
        self.text(value, x + 0.2, y + 0.12, w - 0.28, 0.42, size=21, color=color, bold=True, anchor="mid", font="Aptos Display")
        self.text(label, x + 0.2, y + 0.56, w - 0.28, h - 0.62, size=9, color=COLORS["muted"])

    def table_row(
        self,
        cells: list[str],
        x: float,
        y: float,
        widths: list[float],
        fill: str,
        color: str = COLORS["dark"],
        bold: bool = False,
        size: int = 10,
    ) -> None:
        cx = x
        for cell, width in zip(cells, widths, strict=True):
            self.rect(cx, y, width, 0.46, fill=fill, line=COLORS["line"])
            self.text(cell, cx + 0.03, y + 0.07, width - 0.06, 0.28, size=size, color=color, bold=bold, align="ctr", anchor="mid")
            cx += width

    def bar(self, label: str, value: float, max_value: float, x: float, y: float, w: float, color: str, suffix: str) -> None:
        self.text(label, x, y - 0.03, 1.28, 0.24, size=9, color=COLORS["dark"], align="r")
        self.rect(x + 1.42, y + 0.04, w, 0.17, fill=COLORS["gray"], line=None, preset="roundRect")
        self.rect(x + 1.42, y + 0.04, max(0.02, w * value / max_value), 0.17, fill=color, line=None, preset="roundRect")
        self.text(f"{value:.2f}{suffix}", x + 1.42 + w + 0.1, y - 0.03, 0.8, 0.24, size=9, color=COLORS["muted"])

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(self.items)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""


def load_rows() -> list[dict[str, float | str]]:
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    order = {"YOLOv11n": 0, "YOLOv11s": 1, "YOLOv11m": 2}
    rows.sort(key=lambda row: order.get(row["model_alias"], 99))
    parsed = []
    for row in rows:
        inference_ms = float(row["speed_inference_ms"])
        total_ms = (
            float(row["speed_preprocess_ms"])
            + inference_ms
            + float(row["speed_postprocess_ms"])
        )
        parsed.append(
            {
                "model": row["model_alias"],
                "precision": float(row["mp"]) * 100,
                "recall": float(row["mr"]) * 100,
                "map50": float(row["map50"]) * 100,
                "map5095": float(row["map50_95"]) * 100,
                "inference_ms": inference_ms,
                "total_ms": total_ms,
                "fps": 1000.0 / inference_ms,
            }
        )
    return parsed


def fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def build_slide(rows: list[dict[str, float | str]]) -> str:
    s = Slide()
    s.text("YOLOv11 Detector Comparison", 0.55, 0.28, 10.5, 0.48, size=26, color=COLORS["dark"], bold=True, font="Aptos Display")
    s.text("Test split evaluation for disease-region localization before EfficientNet classification", 0.58, 0.82, 11.4, 0.28, size=12, color=COLORS["muted"])
    s.rect(0.55, 1.12, 1.2, 0.05, fill=COLORS["green"], line=None)
    s.rect(1.78, 1.12, 0.55, 0.05, fill=COLORS["amber"], line=None)
    s.rect(2.36, 1.12, 0.55, 0.05, fill=COLORS["blue"], line=None)

    best_accuracy = max(rows, key=lambda r: float(r["map5095"]))
    fastest = min(rows, key=lambda r: float(r["inference_ms"]))
    balanced = next(row for row in rows if row["model"] == "YOLOv11s")
    s.metric(str(best_accuracy["model"]), "best mAP@0.5:0.95", 0.72, 1.45, 2.45, 1.0, COLORS["green"])
    s.metric(str(fastest["model"]), "fastest detector", 3.42, 1.45, 2.45, 1.0, COLORS["blue"])
    s.metric(str(balanced["model"]), "speed/accuracy middle ground", 6.12, 1.45, 2.72, 1.0, COLORS["amber"])
    s.metric("832 px", "YOLO input size", 9.1, 1.45, 2.45, 1.0, COLORS["cyan"])

    widths = [1.15, 1.1, 1.0, 1.08, 1.25, 1.18, 1.0]
    x0 = 0.72
    y0 = 2.78
    s.table_row(["Model", "Precision", "Recall", "mAP@0.5", "mAP@0.5:0.95", "Infer ms", "FPS"], x0, y0, widths, COLORS["light_blue"], bold=True, size=9)
    row_colors = {"YOLOv11n": COLORS["white"], "YOLOv11s": COLORS["white"], "YOLOv11m": COLORS["light_green"]}
    for idx, row in enumerate(rows):
        y = y0 + 0.46 * (idx + 1)
        s.table_row(
            [
                str(row["model"]),
                fmt_pct(float(row["precision"])),
                fmt_pct(float(row["recall"])),
                fmt_pct(float(row["map50"])),
                fmt_pct(float(row["map5095"])),
                f"{float(row['inference_ms']):.2f}",
                f"{float(row['fps']):.1f}",
            ],
            x0,
            y,
            widths,
            row_colors[str(row["model"])],
            bold=str(row["model"]) == "YOLOv11m",
            size=9,
        )

    s.text("Quality trend", 0.78, 4.62, 2.2, 0.25, size=13, color=COLORS["dark"], bold=True)
    for i, row in enumerate(rows):
        color = COLORS["green"] if row["model"] == "YOLOv11m" else COLORS["blue"] if row["model"] == "YOLOv11s" else COLORS["amber"]
        s.bar(str(row["model"]), float(row["map5095"]), 70.0, 0.78, 5.05 + i * 0.39, 1.6, color, "%")

    s.text("Runtime trend", 5.28, 4.62, 2.2, 0.25, size=13, color=COLORS["dark"], bold=True)
    for i, row in enumerate(rows):
        color = COLORS["green"] if row["model"] == "YOLOv11m" else COLORS["blue"] if row["model"] == "YOLOv11s" else COLORS["amber"]
        s.bar(str(row["model"]), float(row["inference_ms"]), 35.0, 5.28, 5.05 + i * 0.39, 1.6, color, " ms")

    s.rect(9.1, 4.5, 2.95, 1.55, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Takeaway", 9.32, 4.68, 2.45, 0.25, size=13, color=COLORS["dark"], bold=True)
    s.text("YOLOv11m was selected for the final cascade because it gives the highest mAP, while YOLOv11n is best when speed is the main constraint.", 9.32, 5.05, 2.45, 0.72, size=9, color=COLORS["muted"])

    s.text("Inference ms is the Ultralytics detector inference time only; total latency also includes preprocessing and postprocessing.", 0.72, 6.42, 10.8, 0.24, size=9, color=COLORS["muted"])
    s.rect(0.55, 7.18, 12.25, 0.01, fill=COLORS["line"], line=None)
    s.text("Papaya leaf disease detection and classification | YOLOv11 detector results", 0.58, 7.22, 7.5, 0.18, size=8, color=COLORS["muted"])
    return s.xml()


def rels_xml(rels: list[tuple[str, str, str]]) -> str:
    items = "\n".join(
        f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>' for rid, typ, target in rels
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f"{items}</Relationships>"
    )


def content_types() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
</Types>
"""


def presentation_xml() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle><a:defPPr><a:defRPr lang="en-US"/></a:defPPr></p:defaultTextStyle>
</p:presentation>
"""


def slide_master_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle><a:lvl1pPr algn="l"><a:defRPr sz="3200" b="1"/></a:lvl1pPr></p:titleStyle><p:bodyStyle><a:lvl1pPr marL="0" indent="0"><a:defRPr sz="1800"/></a:lvl1pPr></p:bodyStyle><p:otherStyle><a:lvl1pPr marL="0" indent="0"><a:defRPr sz="1800"/></a:lvl1pPr></p:otherStyle></p:txStyles>
</p:sldMaster>
"""


def slide_layout_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>
"""


def theme_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Papaya Theme">
  <a:themeElements>
    <a:clrScheme name="Papaya"><a:dk1><a:srgbClr val="17231A"/></a:dk1><a:lt1><a:srgbClr val="F8FAF7"/></a:lt1><a:dk2><a:srgbClr val="2E7D55"/></a:dk2><a:lt2><a:srgbClr val="FFFFFF"/></a:lt2><a:accent1><a:srgbClr val="2E7D55"/></a:accent1><a:accent2><a:srgbClr val="2F6FB6"/></a:accent2><a:accent3><a:srgbClr val="E8A13A"/></a:accent3><a:accent4><a:srgbClr val="C94A45"/></a:accent4><a:accent5><a:srgbClr val="39A6A3"/></a:accent5><a:accent6><a:srgbClr val="8BC34A"/></a:accent6><a:hlink><a:srgbClr val="2F6FB6"/></a:hlink><a:folHlink><a:srgbClr val="5B6B5F"/></a:folHlink></a:clrScheme>
    <a:fontScheme name="Aptos"><a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="Papaya"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements>
  <a:objectDefaults/><a:extraClrSchemeLst/>
</a:theme>
"""


def core_xml() -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>YOLOv11 Detector Comparison</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
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


def notes(rows: list[dict[str, float | str]]) -> str:
    row_lines = "\n".join(
        f"- {row['model']}: precision {float(row['precision']):.2f}%, recall {float(row['recall']):.2f}%, "
        f"mAP@0.5 {float(row['map50']):.2f}%, mAP@0.5:0.95 {float(row['map5095']):.2f}%, "
        f"inference {float(row['inference_ms']):.2f} ms/image."
        for row in rows
    )
    return f"""# YOLOv11 Detector Comparison - Speaker Notes

This slide compares the three YOLOv11 detector variants used in the first stage of the cascade.

{row_lines}

The main trade-off is speed versus localization quality. YOLOv11n is the fastest model and is suitable for edge devices or very large-scale screening. YOLOv11s provides a middle ground. YOLOv11m is slower, but it has the best mAP@0.5 and mAP@0.5:0.95, so it was selected for the final YOLOv11m plus EfficientNet-B2 cascade.

The inference time shown here is the detector inference time reported by Ultralytics. Total runtime in a deployed pipeline can also include preprocessing, postprocessing, crop extraction, and EfficientNet classification.
"""


def write_pptx() -> None:
    rows = load_rows()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PPTX_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types())
        z.writestr("_rels/.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties", "docProps/app.xml"),
        ]))
        z.writestr("docProps/core.xml", core_xml())
        z.writestr("docProps/app.xml", app_xml())
        z.writestr("ppt/presentation.xml", presentation_xml())
        z.writestr("ppt/_rels/presentation.xml.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml"),
            ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", "slides/slide1.xml"),
            ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "theme/theme1.xml"),
        ]))
        z.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml())
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        ]))
        z.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml())
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml"),
        ]))
        z.writestr("ppt/theme/theme1.xml", theme_xml())
        z.writestr("ppt/slides/slide1.xml", build_slide(rows))
        z.writestr("ppt/slides/_rels/slide1.xml.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
        ]))
    NOTES_PATH.write_text(notes(rows), encoding="utf-8")
    print(PPTX_PATH)
    print(NOTES_PATH)


if __name__ == "__main__":
    write_pptx()
