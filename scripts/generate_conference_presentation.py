from __future__ import annotations

import html
import zipfile
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("outputs/conference_presentation")
PPTX_PATH = OUT_DIR / "papaya_leaf_cascade_conference_slides.pptx"
SCRIPT_PATH = OUT_DIR / "presentation_script_and_notes.md"
OUTLINE_PATH = OUT_DIR / "slide_outline.md"

SLIDE_W = 12_192_000
SLIDE_H = 6_858_000
EMU = 914_400

COLORS = {
    "bg": "F8FAF7",
    "dark": "17231A",
    "muted": "5B6B5F",
    "green": "2E7D55",
    "green2": "8BC34A",
    "blue": "2F6FB6",
    "cyan": "39A6A3",
    "amber": "E8A13A",
    "red": "C94A45",
    "light_green": "E6F2EA",
    "light_blue": "E7F0FA",
    "light_amber": "FFF3DE",
    "light_red": "FCEAE8",
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
        f'<a:latin typeface="{font}"/>'
        f'<a:ea typeface="{font}"/>'
        f'<a:cs typeface="{font}"/>'
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
    paragraphs = text.split("\n")
    para_xml = []
    for para in paragraphs:
        para_xml.append(
            f'<a:p><a:pPr algn="{align}"/>'
            f"<a:r>{run_props(size, color, bold, font)}<a:t>{esc(para)}</a:t></a:r>"
            f"</a:p>"
        )
    return (
        f'<p:txBody><a:bodyPr wrap="square" anchor="{anchor}" lIns="80000" '
        f'rIns="80000" tIns="50000" bIns="50000"><a:spAutoFit/></a:bodyPr>'
        f"<a:lstStyle/>{''.join(para_xml)}</p:txBody>"
    )


class SlideBuilder:
    def __init__(self, slide_no: int, title: str | None = None):
        self.slide_no = slide_no
        self.title = title
        self.items: list[str] = []
        self.next_id = 2
        self.background(COLORS["bg"])
        if title:
            self.text(
                title,
                0.55,
                0.33,
                12.15,
                0.58,
                size=25,
                color=COLORS["dark"],
                bold=True,
                font="Aptos Display",
            )
            self.rect(0.55, 0.98, 1.2, 0.05, fill=COLORS["green"], line=None)
            self.rect(1.78, 0.98, 0.55, 0.05, fill=COLORS["amber"], line=None)
            self.rect(2.36, 0.98, 0.55, 0.05, fill=COLORS["blue"], line=None)
            self.footer()

    def _id(self) -> int:
        shape_id = self.next_id
        self.next_id += 1
        return shape_id

    def background(self, color: str) -> None:
        self.items.append(
            f"""
            <p:sp>
              <p:nvSpPr><p:cNvPr id="{self._id()}" name="Background"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_W}" cy="{SLIDE_H}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
                <a:ln><a:noFill/></a:ln>
              </p:spPr>
            </p:sp>
            """
        )

    def footer(self) -> None:
        self.rect(0.55, 7.18, 12.25, 0.01, fill=COLORS["line"], line=None)
        self.text(
            "GTSD 2026 | Papaya leaf disease detection and classification",
            0.58,
            7.22,
            7.5,
            0.18,
            size=8,
            color=COLORS["muted"],
        )
        self.text(
            str(self.slide_no),
            12.25,
            7.22,
            0.45,
            0.18,
            size=8,
            color=COLORS["muted"],
            align="r",
        )

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
        fill_xml = (
            f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
            if fill
            else "<a:noFill/>"
        )
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
        line: str | None = None,
        size: int = 18,
        color: str = COLORS["dark"],
        bold: bool = False,
        align: str = "ctr",
        anchor: str = "mid",
        preset: str = "roundRect",
    ) -> None:
        self.rect(x, y, w, h, fill=fill, line=line, preset=preset)
        self.text(text, x + 0.04, y + 0.03, w - 0.08, h - 0.06, size=size, color=color, bold=bold, align=align, anchor=anchor)

    def metric(self, number: str, label: str, x: float, y: float, w: float, h: float, color: str) -> None:
        self.rect(x, y, w, h, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
        self.rect(x, y, 0.09, h, fill=color, line=None)
        self.text(number, x + 0.23, y + 0.2, w - 0.35, 0.45, size=26, color=color, bold=True, align="l", anchor="mid", font="Aptos Display")
        self.text(label, x + 0.23, y + 0.76, w - 0.35, 0.34, size=11, color=COLORS["muted"], align="l")

    def bullet_list(self, lines: list[str], x: float, y: float, w: float, gap: float = 0.48, size: int = 15) -> None:
        for idx, line in enumerate(lines):
            yy = y + idx * gap
            self.rect(x, yy + 0.09, 0.09, 0.09, fill=COLORS["green"], line=None, preset="ellipse")
            self.text(line, x + 0.22, yy, w - 0.22, 0.32, size=size, color=COLORS["dark"])

    def bar_chart(
        self,
        data: list[tuple[str, float, str]],
        x: float,
        y: float,
        w: float,
        h: float,
        max_value: float = 100.0,
        value_suffix: str = "%",
        label_size: int = 11,
    ) -> None:
        row_h = h / len(data)
        label_w = min(w * 0.34, 2.1)
        bar_w = w - label_w - 0.82
        for i, (label, value, color) in enumerate(data):
            yy = y + i * row_h
            self.text(label, x, yy + 0.02, label_w - 0.05, row_h * 0.75, size=label_size, color=COLORS["dark"], align="r")
            self.rect(x + label_w, yy + 0.13, bar_w, row_h * 0.35, fill=COLORS["gray"], line=None, preset="roundRect")
            fill_w = max(0.02, bar_w * value / max_value)
            self.rect(x + label_w, yy + 0.13, fill_w, row_h * 0.35, fill=color, line=None, preset="roundRect")
            value_text = f"{value:.2f}{value_suffix}" if max_value == 100 else f"{value:.3f}"
            self.text(value_text, x + label_w + bar_w + 0.12, yy + 0.02, 0.72, row_h * 0.75, size=label_size, color=COLORS["muted"])

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {''.join(self.items)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""


def make_slides() -> list[str]:
    slides: list[SlideBuilder] = []

    s = SlideBuilder(1)
    s.text(
        "A Two-Stage Deep Learning Cascade Framework\nfor Robust Papaya Leaf Disease Detection\nand Classification",
        0.65,
        0.72,
        9.0,
        1.5,
        size=27,
        color=COLORS["dark"],
        bold=True,
        font="Aptos Display",
    )
    s.rect(0.68, 2.42, 1.35, 0.06, fill=COLORS["green"], line=None)
    s.rect(2.08, 2.42, 0.62, 0.06, fill=COLORS["amber"], line=None)
    s.text(
        "YOLOv11m disease-region localization + EfficientNet-B2 ROI classification",
        0.65,
        2.72,
        8.8,
        0.42,
        size=17,
        color=COLORS["green"],
        bold=True,
    )
    s.text(
        "Dang Quang Pham | Quang Sang Le | Manh Quan Bui | Minh Hieu Vu\nHo Chi Minh City University of Technology and Engineering, Vietnam",
        0.65,
        3.35,
        8.8,
        0.65,
        size=13,
        color=COLORS["muted"],
    )
    s.shape_text("Input leaf\nimage", 0.75, 5.05, 1.75, 0.75, COLORS["light_green"], line=COLORS["line"], size=13, bold=True)
    s.shape_text("Detect disease\nregions", 2.95, 5.05, 1.85, 0.75, COLORS["light_blue"], line=COLORS["line"], size=13, bold=True)
    s.shape_text("Classify\nROI", 5.25, 5.05, 1.5, 0.75, COLORS["light_amber"], line=COLORS["line"], size=13, bold=True)
    s.shape_text("Five-class\ndiagnosis", 7.2, 5.05, 1.85, 0.75, COLORS["white"], line=COLORS["green"], size=13, bold=True)
    s.shape_text("->", 2.52, 5.20, 0.32, 0.36, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.shape_text("->", 4.88, 5.20, 0.32, 0.36, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.shape_text("->", 6.84, 5.20, 0.32, 0.36, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.footer()
    slides.append(s)

    s = SlideBuilder(2, "Early diagnosis is difficult in real field conditions")
    s.text(
        "Papaya leaf diseases reduce yield and quality, but early symptoms can be subtle and visually similar.",
        0.72,
        1.35,
        6.05,
        0.55,
        size=18,
        color=COLORS["dark"],
        bold=True,
    )
    cards = [
        ("Similar symptoms", "Disease marks can resemble nutrient stress.", COLORS["light_red"], COLORS["red"]),
        ("Noisy background", "Soil, branches, other leaves, and lighting enter the image.", COLORS["light_amber"], COLORS["amber"]),
        ("Manual inspection", "Diagnosis is slow, subjective, and hard to scale.", COLORS["light_blue"], COLORS["blue"]),
        ("Pesticide risk", "Wrong decisions may increase chemical use and cost.", COLORS["light_green"], COLORS["green"]),
    ]
    for i, (head, body, fill, color) in enumerate(cards):
        x = 0.78 + (i % 2) * 3.15
        y = 2.25 + (i // 2) * 1.45
        s.rect(x, y, 2.82, 1.05, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
        s.rect(x, y, 0.1, 1.05, fill=color, line=None)
        s.text(head, x + 0.25, y + 0.17, 2.3, 0.25, size=14, color=color, bold=True)
        s.text(body, x + 0.25, y + 0.48, 2.35, 0.42, size=10, color=COLORS["muted"])
    s.shape_text(
        "Core requirement:\nmake the model focus on the diseased region, not the whole scene.",
        7.28,
        2.05,
        4.55,
        2.2,
        COLORS["dark"],
        line=None,
        size=19,
        color=COLORS["white"],
        bold=True,
        align="l",
    )
    s.text("Target classes: Healthy, Ring Spot, Curl, Bacterial Spot, Anthracnose", 7.36, 4.55, 4.4, 0.4, size=13, color=COLORS["green"], bold=True)
    slides.append(s)

    s = SlideBuilder(3, "The proposed idea is localization before classification")
    s.text(
        "Most whole-image classifiers must learn disease features together with background variation.",
        0.72,
        1.27,
        11.2,
        0.4,
        size=17,
        color=COLORS["dark"],
        bold=True,
    )
    s.shape_text("Single-stage CNN", 0.9, 2.05, 3.3, 0.52, COLORS["light_red"], line=COLORS["line"], size=16, color=COLORS["red"], bold=True)
    s.shape_text("leaf + soil + branches + lighting", 0.95, 2.9, 3.2, 0.72, COLORS["white"], line=COLORS["line"], size=14, color=COLORS["muted"])
    s.shape_text("classification decision", 0.95, 4.0, 3.2, 0.7, COLORS["white"], line=COLORS["line"], size=14, color=COLORS["muted"])
    s.shape_text("->", 2.35, 3.65, 0.45, 0.32, COLORS["bg"], line=None, size=19, color=COLORS["red"], bold=True)
    s.shape_text("Two-stage cascade", 5.15, 2.05, 5.9, 0.52, COLORS["light_green"], line=COLORS["line"], size=16, color=COLORS["green"], bold=True)
    s.shape_text("YOLOv11m\nlocalizes disease ROI", 5.2, 3.02, 2.1, 0.8, COLORS["white"], line=COLORS["line"], size=14, color=COLORS["dark"], bold=True)
    s.shape_text("EfficientNet-B2\nclassifies ROI", 8.05, 3.02, 2.1, 0.8, COLORS["white"], line=COLORS["line"], size=14, color=COLORS["dark"], bold=True)
    s.shape_text("->", 7.45, 3.23, 0.38, 0.3, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.text(
        "Expected benefit: less background interference and stronger attention to visible disease symptoms.",
        5.25,
        4.35,
        5.75,
        0.65,
        size=15,
        color=COLORS["green"],
        bold=True,
    )
    slides.append(s)

    s = SlideBuilder(4, "The cascade turns a field image into a focused ROI diagnosis")
    s.shape_text("Input\nleaf image", 0.75, 2.48, 1.65, 0.8, COLORS["white"], line=COLORS["line"], size=14, bold=True)
    s.shape_text("YOLOv11m\nDetector", 2.95, 2.36, 1.75, 1.05, COLORS["light_blue"], line=COLORS["blue"], size=14, color=COLORS["blue"], bold=True)
    s.shape_text("ROI crop", 5.25, 2.48, 1.55, 0.8, COLORS["light_amber"], line=COLORS["amber"], size=14, color=COLORS["amber"], bold=True)
    s.shape_text("EfficientNet-B2\nClassifier", 7.3, 2.36, 2.0, 1.05, COLORS["light_green"], line=COLORS["green"], size=14, color=COLORS["green"], bold=True)
    s.shape_text("Five-class\nprediction", 9.9, 2.48, 1.8, 0.8, COLORS["white"], line=COLORS["green"], size=14, bold=True)
    for x in [2.5, 4.85, 6.92, 9.5]:
        s.shape_text("->", x, 2.67, 0.35, 0.28, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.rect(2.95, 4.23, 6.35, 0.06, fill=COLORS["line"], line=None)
    s.text("Healthy images use the full image because no disease bounding box is available.", 2.95, 4.45, 6.8, 0.36, size=13, color=COLORS["muted"])
    s.text("Disease images are cropped into regions of interest before classification.", 2.95, 4.9, 6.7, 0.36, size=13, color=COLORS["muted"])
    s.metric("5", "output classes", 0.82, 5.25, 2.3, 1.08, COLORS["green"])
    s.metric("2", "learning stages", 3.55, 5.25, 2.3, 1.08, COLORS["blue"])
    s.metric("ROI", "background reduction", 6.28, 5.25, 2.3, 1.08, COLORS["amber"])
    slides.append(s)

    s = SlideBuilder(5, "BDPapayaLeaf was prepared for detection and ROI classification")
    s.metric("1,707", "disease images for YOLO detection", 0.75, 1.35, 3.0, 1.08, COLORS["blue"])
    s.metric("11,111", "images/ROIs for EfficientNet-B2", 4.05, 1.35, 3.0, 1.08, COLORS["green"])
    s.metric("291", "final cascade test images", 7.35, 1.35, 3.0, 1.08, COLORS["amber"])
    s.shape_text("70%", 1.15, 3.14, 1.2, 0.5, COLORS["green"], line=None, color=COLORS["white"], size=17, bold=True)
    s.shape_text("15%", 2.42, 3.14, 0.9, 0.5, COLORS["blue"], line=None, color=COLORS["white"], size=17, bold=True)
    s.shape_text("15%", 3.38, 3.14, 0.9, 0.5, COLORS["amber"], line=None, color=COLORS["white"], size=17, bold=True)
    s.text("Train / validation / test split", 1.13, 3.78, 3.6, 0.3, size=12, color=COLORS["muted"])
    s.bullet_list(
        [
            "YOLO annotations: bounding boxes for four disease classes.",
            "Healthy class: no disease region, so no bounding boxes.",
            "Class imbalance handled with weighted loss, oversampling, and augmentation.",
            "Final test combines 257 disease images and 34 healthy images.",
        ],
        5.2,
        3.05,
        6.2,
        gap=0.55,
        size=13,
    )
    s.text("Classes", 0.9, 4.82, 1.0, 0.32, size=14, bold=True, color=COLORS["dark"])
    class_items = [
        ("Healthy", COLORS["green"]),
        ("Ring Spot", COLORS["amber"]),
        ("Curl", COLORS["cyan"]),
        ("Bacterial Spot", COLORS["blue"]),
        ("Anthracnose", COLORS["red"]),
    ]
    for i, (label, color) in enumerate(class_items):
        s.shape_text(label, 0.9 + i * 2.15, 5.35, 1.72, 0.48, color, line=None, size=11, color=COLORS["white"], bold=True)
    slides.append(s)

    s = SlideBuilder(6, "YOLOv11m and EfficientNet-B2 balance accuracy with deployability")
    s.shape_text("Stage 1: YOLOv11m", 0.85, 1.42, 4.8, 0.58, COLORS["light_blue"], line=COLORS["blue"], size=17, color=COLORS["blue"], bold=True)
    s.bullet_list(
        [
            "Single-pass disease-region localization.",
            "Useful for small and irregular lesion patterns.",
            "Multi-scale features support varied disease sizes.",
        ],
        1.0,
        2.25,
        4.25,
        size=13,
    )
    s.shape_text("Stage 2: EfficientNet-B2", 6.35, 1.42, 4.8, 0.58, COLORS["light_green"], line=COLORS["green"], size=17, color=COLORS["green"], bold=True)
    s.bullet_list(
        [
            "Compound scaling balances depth, width, and resolution.",
            "MBConv blocks keep computation efficient.",
            "9.2M parameters and 1.0B FLOPs on ImageNet baseline.",
        ],
        6.5,
        2.25,
        4.35,
        size=13,
    )
    s.rect(0.85, 4.85, 10.3, 0.85, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Design choice: use detection to decide where to look, then use a compact classifier to decide what disease it is.", 1.12, 5.08, 9.7, 0.35, size=16, color=COLORS["dark"], bold=True, align="ctr")
    slides.append(s)

    s = SlideBuilder(7, "YOLOv11m provides useful disease-region localization")
    s.text("Detection performance on the four disease classes", 0.82, 1.28, 5.2, 0.34, size=15, color=COLORS["dark"], bold=True)
    detection = [
        ("Anthracnose", 0.515, COLORS["red"]),
        ("Bacterial Spot", 0.993, COLORS["blue"]),
        ("Curl", 0.995, COLORS["cyan"]),
        ("Ring Spot", 0.604, COLORS["amber"]),
        ("All classes", 0.777, COLORS["green"]),
    ]
    s.bar_chart(detection, 0.78, 1.85, 5.55, 2.8, max_value=1.0, value_suffix="", label_size=10)
    s.metric("0.802", "precision, all classes", 7.0, 1.72, 2.2, 1.0, COLORS["blue"])
    s.metric("0.816", "recall, all classes", 9.45, 1.72, 2.2, 1.0, COLORS["green"])
    s.metric("0.777", "mAP@0.5, all classes", 7.0, 3.15, 2.2, 1.0, COLORS["amber"])
    s.metric("0.652", "mAP@0.5:0.95", 9.45, 3.15, 2.2, 1.0, COLORS["red"])
    s.text(
        "Strongest: Bacterial Spot and Curl.\nHarder: Anthracnose and Ring Spot, likely due to irregular lesions and visual similarity.",
        7.0,
        4.75,
        4.65,
        0.8,
        size=13,
        color=COLORS["muted"],
    )
    slides.append(s)

    s = SlideBuilder(8, "The complete cascade reached 94.85% accuracy")
    s.metric("94.85%", "overall accuracy", 0.8, 1.33, 2.55, 1.08, COLORS["green"])
    s.metric("94.92%", "macro precision", 3.65, 1.33, 2.55, 1.08, COLORS["blue"])
    s.metric("94.93%", "macro recall", 6.5, 1.33, 2.55, 1.08, COLORS["amber"])
    s.metric("94.92%", "macro F1-score", 9.35, 1.33, 2.55, 1.08, COLORS["red"])
    s.text("276 correct predictions out of 291 final test images", 0.9, 2.82, 4.5, 0.35, size=16, color=COLORS["dark"], bold=True)
    class_acc = [
        ("Anthracnose", 94.44, COLORS["red"]),
        ("Bacterial Spot", 94.20, COLORS["blue"]),
        ("Curl", 98.15, COLORS["cyan"]),
        ("Healthy", 94.12, COLORS["green"]),
        ("Ring Spot", 93.75, COLORS["amber"]),
    ]
    s.bar_chart(class_acc, 0.9, 3.35, 6.05, 2.6, max_value=100.0, label_size=10)
    s.shape_text(
        "Interpretation\nMost errors occur among visually similar disease classes, but the diagonal-dominant confusion matrix indicates stable classification.",
        7.45,
        3.45,
        3.95,
        1.7,
        COLORS["white"],
        line=COLORS["line"],
        size=14,
        align="l",
    )
    slides.append(s)

    s = SlideBuilder(9, "ROI localization improved the EfficientNet-B2 baseline")
    s.text("Single-stage vs. cascade classification accuracy", 0.82, 1.35, 5.1, 0.35, size=15, color=COLORS["dark"], bold=True)
    s.bar_chart(
        [("Whole-image\nEfficientNet-B2", 92.78, COLORS["muted"]), ("YOLOv11m +\nEfficientNet-B2", 94.85, COLORS["green"])],
        0.9,
        2.0,
        5.0,
        1.25,
        max_value=100,
        label_size=10,
    )
    s.shape_text("+2.07 percentage points", 1.2, 3.58, 3.9, 0.55, COLORS["light_green"], line=COLORS["green"], size=17, color=COLORS["green"], bold=True)
    s.text("Backbone comparison inside the same YOLOv11m cascade", 6.55, 1.35, 5.2, 0.35, size=15, color=COLORS["dark"], bold=True)
    s.bar_chart(
        [
            ("VGG16", 93.47, COLORS["red"]),
            ("DenseNet121", 94.16, COLORS["amber"]),
            ("ResNet50", 94.50, COLORS["blue"]),
            ("EfficientNet-B2", 94.85, COLORS["green"]),
        ],
        6.55,
        2.0,
        5.25,
        2.3,
        max_value=100,
        label_size=10,
    )
    s.text(
        "Takeaway: the improvement comes from both the two-stage structure and the efficient second-stage backbone.",
        1.0,
        5.25,
        10.5,
        0.38,
        size=16,
        color=COLORS["dark"],
        bold=True,
        align="ctr",
    )
    slides.append(s)

    s = SlideBuilder(10, "The proposed model is competitive with reported papaya studies")
    s.text("Accuracy comparison with existing studies", 0.82, 1.33, 5.0, 0.35, size=15, color=COLORS["dark"], bold=True)
    s.bar_chart(
        [
            ("Darknet53", 84.78, COLORS["red"]),
            ("ResNet50", 87.95, COLORS["amber"]),
            ("HASPNet", 93.87, COLORS["blue"]),
            ("Proposed", 94.85, COLORS["green"]),
        ],
        0.9,
        1.95,
        5.9,
        2.45,
        max_value=100,
        label_size=11,
    )
    s.shape_text("94.92%", 7.45, 1.78, 1.7, 0.58, COLORS["light_blue"], line=COLORS["blue"], size=19, color=COLORS["blue"], bold=True)
    s.text("precision", 9.35, 1.9, 1.3, 0.3, size=13, color=COLORS["muted"])
    s.shape_text("94.93%", 7.45, 2.65, 1.7, 0.58, COLORS["light_green"], line=COLORS["green"], size=19, color=COLORS["green"], bold=True)
    s.text("recall", 9.35, 2.77, 1.3, 0.3, size=13, color=COLORS["muted"])
    s.shape_text("94.92%", 7.45, 3.52, 1.7, 0.58, COLORS["light_amber"], line=COLORS["amber"], size=19, color=COLORS["amber"], bold=True)
    s.text("F1-score", 9.35, 3.64, 1.3, 0.3, size=13, color=COLORS["muted"])
    s.text(
        "Note: datasets and protocols differ across papers, so this is a contextual comparison rather than a strict identical benchmark.",
        7.25,
        4.75,
        4.3,
        0.75,
        size=12,
        color=COLORS["muted"],
    )
    slides.append(s)

    s = SlideBuilder(11, "Remaining challenges guide the next research steps")
    s.shape_text("Current limitations", 0.9, 1.45, 4.7, 0.55, COLORS["light_red"], line=COLORS["red"], size=17, color=COLORS["red"], bold=True)
    s.bullet_list(
        [
            "Similar visual symptoms across some disease classes.",
            "Sensitivity to lighting, image quality, and leaf orientation.",
            "Need for broader field data from diverse environments.",
        ],
        1.05,
        2.28,
        4.2,
        size=13,
    )
    s.shape_text("Future work", 6.45, 1.45, 4.7, 0.55, COLORS["light_green"], line=COLORS["green"], size=17, color=COLORS["green"], bold=True)
    s.bullet_list(
        [
            "Collect larger multi-environment datasets.",
            "Integrate stronger attention mechanisms.",
            "Evaluate robust architectures, ensembles, and deployment.",
        ],
        6.6,
        2.28,
        4.25,
        size=13,
    )
    s.rect(1.05, 5.15, 9.95, 0.75, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Goal: move from controlled evaluation toward reliable field decision support for smart agriculture.", 1.25, 5.38, 9.55, 0.3, size=15, color=COLORS["dark"], bold=True, align="ctr")
    slides.append(s)

    s = SlideBuilder(12, "Take-home message")
    s.shape_text("1", 1.0, 1.55, 0.62, 0.62, COLORS["green"], line=None, size=22, color=COLORS["white"], bold=True, preset="ellipse")
    s.text("Detect first, classify second", 1.85, 1.62, 4.7, 0.35, size=18, color=COLORS["dark"], bold=True)
    s.text("Localization reduces background interference before disease classification.", 1.85, 2.0, 5.6, 0.3, size=12, color=COLORS["muted"])
    s.shape_text("2", 1.0, 3.0, 0.62, 0.62, COLORS["blue"], line=None, size=22, color=COLORS["white"], bold=True, preset="ellipse")
    s.text("YOLOv11m + EfficientNet-B2 achieved 94.85% accuracy", 1.85, 3.07, 7.4, 0.35, size=18, color=COLORS["dark"], bold=True)
    s.text("The cascade outperformed the whole-image EfficientNet-B2 baseline.", 1.85, 3.45, 5.6, 0.3, size=12, color=COLORS["muted"])
    s.shape_text("3", 1.0, 4.45, 0.62, 0.62, COLORS["amber"], line=None, size=22, color=COLORS["white"], bold=True, preset="ellipse")
    s.text("The framework is practical for smart agriculture support", 1.85, 4.52, 7.4, 0.35, size=18, color=COLORS["dark"], bold=True)
    s.text("Future work will focus on field robustness and broader dataset coverage.", 1.85, 4.9, 5.9, 0.3, size=12, color=COLORS["muted"])
    s.shape_text("Thank you\nQuestions?", 8.55, 2.05, 2.65, 1.55, COLORS["dark"], line=None, size=24, color=COLORS["white"], bold=True)
    slides.append(s)

    return [s.xml() for s in slides]


def rels_xml(relationships: list[tuple[str, str, str]]) -> str:
    body = "\n".join(
        f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>' for rid, typ, target in relationships
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{body}
</Relationships>
"""


def content_types(num_slides: int) -> str:
    slide_overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, num_slides + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {slide_overrides}
</Types>
"""


def presentation_xml(num_slides: int) -> str:
    slide_ids = "\n".join(
        f'<p:sldId id="{255 + i}" r:id="rId{i + 1}"/>' for i in range(1, num_slides + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
    {slide_ids}
  </p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle>
    <a:defPPr><a:defRPr lang="en-US"/></a:defPPr>
  </p:defaultTextStyle>
</p:presentation>
"""


def slide_master_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>
      </p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles>
    <p:titleStyle><a:lvl1pPr algn="l"><a:defRPr sz="3200" b="1"/></a:lvl1pPr></p:titleStyle>
    <p:bodyStyle><a:lvl1pPr marL="0" indent="0"><a:defRPr sz="1800"/></a:lvl1pPr></p:bodyStyle>
    <p:otherStyle><a:lvl1pPr marL="0" indent="0"><a:defRPr sz="1800"/></a:lvl1pPr></p:otherStyle>
  </p:txStyles>
</p:sldMaster>
"""


def slide_layout_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             type="blank" preserve="1">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>
      </p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>
"""


def theme_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Papaya Conference Theme">
  <a:themeElements>
    <a:clrScheme name="Papaya">
      <a:dk1><a:srgbClr val="17231A"/></a:dk1>
      <a:lt1><a:srgbClr val="F8FAF7"/></a:lt1>
      <a:dk2><a:srgbClr val="2E7D55"/></a:dk2>
      <a:lt2><a:srgbClr val="FFFFFF"/></a:lt2>
      <a:accent1><a:srgbClr val="2E7D55"/></a:accent1>
      <a:accent2><a:srgbClr val="2F6FB6"/></a:accent2>
      <a:accent3><a:srgbClr val="E8A13A"/></a:accent3>
      <a:accent4><a:srgbClr val="C94A45"/></a:accent4>
      <a:accent5><a:srgbClr val="39A6A3"/></a:accent5>
      <a:accent6><a:srgbClr val="8BC34A"/></a:accent6>
      <a:hlink><a:srgbClr val="2F6FB6"/></a:hlink>
      <a:folHlink><a:srgbClr val="5B6B5F"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Aptos">
      <a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Aptos"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Papaya">
      <a:fillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:schemeClr val="phClr"/></a:gs><a:gs pos="100000"><a:schemeClr val="phClr"/></a:gs></a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:fillStyleLst>
      <a:lnStyleLst>
        <a:ln w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
        <a:ln w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
        <a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>
      </a:lnStyleLst>
      <a:effectStyleLst>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
        <a:effectStyle><a:effectLst/></a:effectStyle>
      </a:effectStyleLst>
      <a:bgFillStyleLst>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
        <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      </a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
  <a:objectDefaults/>
  <a:extraClrSchemeLst/>
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
  <dc:title>Papaya Leaf Disease Detection Conference Slides</dc:title>
  <dc:subject>Two-stage deep learning cascade framework</dc:subject>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


def app_xml(num_slides: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex PPTX Generator</Application>
  <PresentationFormat>On-screen Show (16:9)</PresentationFormat>
  <Slides>{num_slides}</Slides>
  <Company>Ho Chi Minh City University of Technology and Engineering</Company>
</Properties>
"""


SCRIPT_MD = """# Presentation Script and Speaker Notes

Title: A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification

Suggested length: 10-12 minutes, excluding Q&A.

## Slide 1 - Title

Good morning, distinguished chairs, respected professors, and fellow researchers. Thank you for the opportunity to present our work, titled "A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification." In this study, we combine YOLOv11m for disease-region localization with EfficientNet-B2 for region-based classification. The main idea is simple: before asking a classifier what disease is present, we first ask the system where the relevant disease symptoms are located.

## Slide 2 - Motivation

Papaya is an important tropical crop, but leaf diseases can reduce both yield and fruit quality. In real farming conditions, early diagnosis is not straightforward. Some disease symptoms look similar to nutrient deficiency, and images often contain soil, branches, other leaves, and uncontrolled lighting. Manual inspection is slow and subjective, and incorrect decisions may lead to unnecessary pesticide use. Therefore, an automatic system should not only classify the image, but also focus on the visual evidence that actually supports the diagnosis.

## Slide 3 - Research Gap and Main Idea

Many deep-learning approaches for plant disease recognition use whole-image classification. This can work well in controlled datasets, but it also forces the model to learn from both disease regions and irrelevant background. Our proposed solution is a two-stage cascade. First, YOLOv11m detects suspicious disease regions. Then, EfficientNet-B2 classifies the cropped region of interest. This structure is designed to reduce background interference and allow the classifier to focus on localized disease symptoms.

## Slide 4 - Proposed Framework

The complete pipeline starts from an input papaya leaf image. YOLOv11m predicts bounding boxes around suspicious disease regions. These bounding boxes are then used to crop regions of interest from the original image. The cropped ROIs are resized and passed to EfficientNet-B2 for final classification. The system predicts one of five categories: Healthy, Ring Spot, Curl, Bacterial Spot, or Anthracnose. For healthy images, because there is no disease bounding box, the full image is used for classification.

## Slide 5 - Dataset and Preparation

We used the BDPapayaLeaf dataset. For the detection stage, the dataset contains 1,707 disease images across four disease classes, prepared in YOLO annotation format. For the classification stage, the dataset contains 11,111 images or ROIs organized by class. We used a 70:15:15 train, validation, and test split. Because the class distribution is imbalanced, we applied class-weighted loss, oversampling, and data augmentation. The final cascade evaluation used 291 images: 257 disease images and 34 healthy images.

## Slide 6 - Model Choice

YOLOv11m was selected because it provides a good balance between localization accuracy and efficiency. Its multi-scale feature representation is helpful because disease regions can vary in size, shape, and visual clarity. EfficientNet-B2 was selected as the classifier because it offers strong accuracy with relatively low computational cost. Its compound scaling strategy balances depth, width, and input resolution, while MBConv blocks support efficient feature extraction. This combination fits the goal of a practical smart-agriculture diagnostic system.

## Slide 7 - Detection Results

Before evaluating the full cascade, we evaluated YOLOv11m on the disease-region detection task. Across all disease classes, the model achieved 0.802 precision, 0.816 recall, 0.777 mAP at IoU 0.5, and 0.652 mAP from IoU 0.5 to 0.95. Bacterial Spot and Curl were detected very strongly, with mAP at 0.5 close to 0.99. Anthracnose and Ring Spot were more difficult, likely because their symptoms are more irregular and visually similar to other leaf patterns.

## Slide 8 - Classification Results

For the complete YOLOv11m and EfficientNet-B2 cascade, the system achieved 94.85 percent accuracy on the final test set. This corresponds to 276 correct predictions out of 291 images. The macro precision, recall, and F1-score were all approximately 94.9 percent, which indicates balanced performance across classes. The class-wise results were also stable, with Curl reaching the highest accuracy at 98.15 percent and the other four categories remaining above 93 percent.

## Slide 9 - Ablation and Backbone Comparison

To understand the benefit of the cascade, we compared it with a single-stage EfficientNet-B2 classifier using whole images. The whole-image baseline achieved 92.78 percent accuracy, while the proposed cascade achieved 94.85 percent. This is an improvement of 2.07 percentage points. We also compared different CNN backbones inside the same YOLOv11m-based cascade. VGG16, DenseNet121, and ResNet50 all performed well, but EfficientNet-B2 achieved the best overall result.

## Slide 10 - Comparison with Existing Studies

We also compared the proposed model with several reported papaya leaf disease studies. The proposed model achieved 94.85 percent accuracy, which is higher than the reported results for ResNet50, HASPNet, and Darknet53 in the referenced studies. However, this comparison should be interpreted carefully because datasets, disease categories, and evaluation protocols are not identical. The value of this result is that it suggests the two-stage localization-plus-classification strategy is competitive and promising.

## Slide 11 - Limitations and Future Work

Although the results are encouraging, some challenges remain. Several papaya leaf diseases share similar visual symptoms, including color changes, spots, and irregular leaf patterns. Image quality, lighting conditions, background complexity, and leaf orientation can also affect performance. In future work, we plan to use a larger and more diverse dataset collected from different environments. We also plan to explore stronger attention mechanisms, ensemble learning, and deployment-oriented evaluation for practical field use.

## Slide 12 - Closing

To conclude, this study shows that detecting disease regions before classification can improve papaya leaf disease recognition. The proposed YOLOv11m and EfficientNet-B2 cascade achieved 94.85 percent accuracy and outperformed the whole-image EfficientNet-B2 baseline. More broadly, the framework provides a practical direction for smart-agriculture decision support, where the model not only predicts a disease label but also focuses on the visual region that supports that prediction. Thank you for your attention. I welcome your questions.

# Possible Q&A Preparation

## Why use a two-stage model instead of a single classifier?

Because whole-image classifiers may learn from irrelevant background regions. The two-stage model first localizes disease symptoms and then classifies the cropped ROI, which reduces background interference.

## Why was the Healthy class not included in YOLO detection?

Healthy leaves do not contain visible disease regions, so there are no disease bounding boxes to annotate. For healthy samples, the full image is passed to the classifier.

## Why choose EfficientNet-B2 instead of a larger model?

EfficientNet-B2 provides a strong accuracy-efficiency trade-off. It is compact compared with heavier CNNs, while still learning discriminative disease features from the cropped ROIs.

## Why are Anthracnose and Ring Spot harder in detection?

Their symptoms can be irregular, small, or visually similar to other leaf patterns. This makes precise localization more difficult than for diseases with clearer spot or curl patterns.

## Is the comparison with previous studies completely fair?

Not completely. The referenced studies may use different datasets, categories, and evaluation protocols. The comparison is useful for context, but the strongest evidence in this paper is the controlled comparison between the whole-image baseline and the proposed cascade.

## What is the next practical step?

The next step is to evaluate the system on more diverse field images and study deployment scenarios, such as mobile or edge-based diagnosis for farmers.

# Slide Design References Used

- Assertion-Evidence approach: use a full-sentence message as the slide headline and support it with visual evidence rather than bullet-heavy slides. https://www.assertion-evidence.com/
- Jose Nelson Amaral, "Effective Communication of Scientific Results": focus on the audience, use images and clear visual information, and avoid overwhelming listeners. https://arxiv.org/abs/2401.10205
- WIRED, "The Steve Jobs MBA Unit 108": create clear headline messages, use visual slides, and organize around a small number of key points. https://www.wired.com/story/unit-108/
"""


OUTLINE_MD = """# Slide Outline

1. Title: A Two-Stage Deep Learning Cascade Framework
2. Motivation: Early diagnosis is difficult in real field conditions
3. Research gap: Whole-image classification leaves too much background in the decision
4. Proposed framework: YOLOv11m -> ROI crop -> EfficientNet-B2 -> five-class prediction
5. Dataset and preparation: BDPapayaLeaf, 70:15:15 split, imbalance handling
6. Model choice: why YOLOv11m and EfficientNet-B2
7. Detection results: YOLOv11m mAP@0.5 = 0.777
8. Classification results: cascade accuracy = 94.85%
9. Ablation: +2.07 percentage points over whole-image EfficientNet-B2
10. Comparison: competitive with reported papaya studies
11. Limitations and future work
12. Take-home message and Q&A
"""


def write_pptx() -> None:
    slide_xmls = make_slides()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    num_slides = len(slide_xmls)

    presentation_rels = [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml")]
    for i in range(1, num_slides + 1):
        presentation_rels.append((f"rId{i + 1}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"slides/slide{i}.xml"))
    presentation_rels.append((f"rId{num_slides + 2}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "theme/theme1.xml"))

    with zipfile.ZipFile(PPTX_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types(num_slides))
        z.writestr("_rels/.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties", "docProps/app.xml"),
        ]))
        z.writestr("docProps/core.xml", core_xml())
        z.writestr("docProps/app.xml", app_xml(num_slides))
        z.writestr("ppt/presentation.xml", presentation_xml(num_slides))
        z.writestr("ppt/_rels/presentation.xml.rels", rels_xml(presentation_rels))
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
        for i, xml in enumerate(slide_xmls, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", xml)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", rels_xml([
                ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ]))

    SCRIPT_PATH.write_text(SCRIPT_MD, encoding="utf-8")
    OUTLINE_PATH.write_text(OUTLINE_MD, encoding="utf-8")
    print(PPTX_PATH)
    print(SCRIPT_PATH)
    print(OUTLINE_PATH)


if __name__ == "__main__":
    write_pptx()
