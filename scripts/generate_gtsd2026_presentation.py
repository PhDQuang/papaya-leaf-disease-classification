from __future__ import annotations

import html
import zipfile
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("outputs/gtsd2026_presentation")
PPTX_PATH = OUT_DIR / "GTSD2026_Papaya_Cascade_Slides.pptx"
SCRIPT_PATH = OUT_DIR / "gtsd2026_speaker_script.md"
OUTLINE_PATH = OUT_DIR / "gtsd2026_slide_outline.md"

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
            "IEEE GTSD 2026 | Papaya Leaf Disease Detection & Classification Cascade",
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
        self.text(number, x + 0.23, y + 0.15, w - 0.35, 0.45, size=24, color=color, bold=True, align="l", anchor="mid", font="Aptos Display")
        self.text(label, x + 0.23, y + 0.65, w - 0.35, h - 0.7, size=11, color=COLORS["muted"], align="l")

    def bullet_list(self, lines: list[str], x: float, y: float, w: float, gap: float = 0.48, size: int = 14) -> None:
        for idx, line in enumerate(lines):
            yy = y + idx * gap
            self.rect(x, yy + 0.08, 0.09, 0.09, fill=COLORS["green"], line=None, preset="ellipse")
            self.text(line, x + 0.22, yy, w - 0.22, 0.38, size=size, color=COLORS["dark"])

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
        label_w = min(w * 0.36, 2.3)
        bar_w = w - label_w - 0.85
        for i, (label, value, color) in enumerate(data):
            yy = y + i * row_h
            self.text(label, x, yy + 0.02, label_w - 0.05, row_h * 0.8, size=label_size, color=COLORS["dark"], align="r")
            self.rect(x + label_w, yy + 0.12, bar_w, row_h * 0.35, fill=COLORS["gray"], line=None, preset="roundRect")
            fill_w = max(0.02, bar_w * value / max_value)
            self.rect(x + label_w, yy + 0.12, fill_w, row_h * 0.35, fill=color, line=None, preset="roundRect")
            value_text = f"{value:.2f}{value_suffix}" if max_value == 100 else f"{value:.3f}"
            self.text(value_text, x + label_w + bar_w + 0.1, yy + 0.02, 0.75, row_h * 0.8, size=label_size, color=COLORS["muted"])

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

    # SLIDE 1: Title
    s = SlideBuilder(1)
    s.text(
        "A Two-Stage Deep Learning Cascade Framework\nfor Robust Papaya Leaf Disease Detection\nand Classification",
        0.65, 0.65, 11.5, 1.4,
        size=26, color=COLORS["dark"], bold=True, font="Aptos Display"
    )
    s.rect(0.68, 2.2, 1.5, 0.06, fill=COLORS["green"], line=None)
    s.rect(2.28, 2.2, 0.7, 0.06, fill=COLORS["amber"], line=None)
    s.rect(3.08, 2.2, 0.7, 0.06, fill=COLORS["blue"], line=None)
    s.text(
        "IEEE GTSD 2026 | International Conference on Green Technology and Sustainable Development",
        0.65, 2.45, 11.0, 0.4, size=16, color=COLORS["green"], bold=True
    )
    s.text(
        "Dang Quang Pham | Quang Sang Le | Manh Quan Bui | Minh Hieu Vu\nFaculty of Information Technology, Ho Chi Minh City University of Technology and Engineering (HCMUTE), Vietnam",
        0.65, 3.0, 11.0, 0.65, size=13, color=COLORS["muted"]
    )
    # Pipeline box illustration
    s.shape_text("Input Field Image\n(Cluttered)", 0.75, 4.8, 2.2, 1.0, COLORS["light_green"], line=COLORS["line"], size=13, bold=True)
    s.shape_text("Stage 1: YOLOv11m\nLesion Localization", 3.45, 4.8, 2.4, 1.0, COLORS["light_blue"], line=COLORS["blue"], size=13, color=COLORS["blue"], bold=True)
    s.shape_text("Stage 2: EfficientNet-B2\nROI Classification", 6.35, 4.8, 2.4, 1.0, COLORS["light_amber"], line=COLORS["amber"], size=13, color=COLORS["amber"], bold=True)
    s.shape_text("Robust 5-Class\nDiagnosis", 9.25, 4.8, 2.2, 1.0, COLORS["white"], line=COLORS["green"], size=13, bold=True)
    s.shape_text("->", 3.03, 5.1, 0.35, 0.4, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.shape_text("->", 5.93, 5.1, 0.35, 0.4, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.shape_text("->", 8.83, 5.1, 0.35, 0.4, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.footer()
    slides.append(s)

    # SLIDE 2: Background & Challenge
    s = SlideBuilder(2, "I. Motivations: Agricultural Background & The Challenge")
    s.text("Papaya diseases cause severe yield loss, but early symptoms closely resemble nutrient stress.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    cards = [
        ("Economic Impact", "Widely cultivated tropical fruit rich in antioxidants and vitamins; vital for agricultural economies.", COLORS["light_green"], COLORS["green"]),
        ("Foliar Threats", "Anthracnose, Bacterial Spot, Curl, and Ring Spot cause severe leaf damage and fruit degradation.", COLORS["light_red"], COLORS["red"]),
        ("Diagnostic Dilemma", "Early disease spots mimic nutrient deficiency. Visual observation alone is subjective and error-prone.", COLORS["light_amber"], COLORS["amber"]),
        ("Pesticide Risk", "Misdiagnosis leads to excessive chemical spraying—polluting soil & water and raising farm costs.", COLORS["light_blue"], COLORS["blue"]),
    ]
    for i, (head, body, fill, color) in enumerate(cards):
        x = 0.75 + (i % 2) * 5.8
        y = 1.85 + (i // 2) * 1.6
        s.rect(x, y, 5.5, 1.35, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
        s.rect(x, y, 0.12, 1.35, fill=color, line=None)
        s.text(head, x + 0.3, y + 0.15, 5.0, 0.3, size=15, color=color, bold=True)
        s.text(body, x + 0.3, y + 0.5, 5.0, 0.75, size=13, color=COLORS["muted"])
    s.shape_text("Core Requirement: An automated vision system that isolates true disease lesions from environmental clutter.", 0.75, 5.35, 11.3, 0.9, COLORS["dark"], line=None, size=16, color=COLORS["white"], bold=True)
    slides.append(s)

    # SLIDE 3: Limitations of Existing Approaches
    s = SlideBuilder(3, "I. Motivations: Limitations of Existing AI Approaches")
    s.text("Why standard single-stage models struggle in complex, real-world field conditions:", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    # Left Box: Whole-Image CNN
    s.rect(0.75, 1.85, 5.5, 4.6, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(0.75, 1.85, 5.5, 0.6, fill=COLORS["light_red"], line=COLORS["red"], preset="roundRect")
    s.text("Why NOT Whole-Image CNN?", 1.0, 2.0, 5.0, 0.4, size=16, color=COLORS["red"], bold=True)
    s.bullet_list([
        "Background Interference: Real orchard images contain soil, stones, weeds, insects, and harsh lighting.",
        "Multi-Leaf & Occlusion: Multiple overlapping leaves confuse global feature extractors.",
        "Result: Irrelevant background noise dominates, drastically degrading classification accuracy."
    ], 1.0, 2.7, 5.0, gap=0.75, size=13)

    # Right Box: Standalone YOLO
    s.rect(6.5, 1.85, 5.5, 4.6, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(6.5, 1.85, 5.5, 0.6, fill=COLORS["light_amber"], line=COLORS["amber"], preset="roundRect")
    s.text("Why NOT Standalone YOLO?", 6.75, 2.0, 5.0, 0.4, size=16, color=COLORS["amber"], bold=True)
    s.bullet_list([
        "The Confidence Threshold Dilemma in end-to-end 5-class detection:",
        "High Threshold -> Misses early, subtle disease spots (False Negatives / Low Recall).",
        "Low Threshold -> Misclassifies soil, stones, or nutrient stress as diseases (False Positives).",
        "Result: Object detectors alone struggle with fine-grained morphological classification."
    ], 6.75, 2.7, 5.0, gap=0.75, size=13)
    slides.append(s)

    # SLIDE 4: Research Objectives & Solution
    s = SlideBuilder(4, "I. Motivations: Research Objectives & Proposed Solution")
    s.text("Our Philosophy: Localize first, classify second — combining detection robustness with CNN precision.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    s.shape_text("Stage 1: Lesion Localization (YOLOv11m)\nDetects and crops suspicious Regions of Interest (ROIs), overcoming occlusion and removing background noise.", 0.75, 1.9, 11.3, 1.1, COLORS["light_blue"], line=COLORS["blue"], size=15, color=COLORS["blue"], bold=True, align="l")
    s.shape_text("Stage 2: ROI-Based Classification (EfficientNet-B2)\nFocuses 100% of network capacity on fine-grained lesion morphology without environmental interference.", 0.75, 3.2, 11.3, 1.1, COLORS["light_green"], line=COLORS["green"], size=15, color=COLORS["green"], bold=True, align="l")
    
    s.metric("+2.07%", "Accuracy boost over whole-image", 0.75, 4.65, 3.5, 1.4, COLORS["green"])
    s.metric("100%", "Background clutter stripped", 4.65, 4.65, 3.5, 1.4, COLORS["blue"])
    s.metric("~30 ms", "Real-time cascade latency", 8.55, 4.65, 3.5, 1.4, COLORS["amber"])
    slides.append(s)

    # SLIDE 5: Dataset Preparation & Data Cleaning
    s = SlideBuilder(5, "II. Dataset Preparation & Rigorous Data Hygiene")
    s.text("We evaluated on BDPapayaLeaf, implementing strict auditing to resolve a major public dataset anomaly.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    s.metric("1,707", "Detection images (4 disease classes)", 0.75, 1.85, 3.5, 1.2, COLORS["blue"])
    s.metric("11,111", "Classification ROIs / images", 0.75, 3.25, 3.5, 1.2, COLORS["green"])
    s.metric("291", "Final cascade test set images", 0.75, 4.65, 3.5, 1.2, COLORS["amber"])
    
    # Right Box: Critical Discovery
    s.rect(4.6, 1.85, 7.45, 4.0, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(4.6, 1.85, 7.45, 0.6, fill=COLORS["light_red"], line=COLORS["red"], preset="roundRect")
    s.text("🚨 Critical Data Hygiene & Scientific Integrity", 4.85, 2.0, 7.0, 0.4, size=16, color=COLORS["red"], bold=True)
    s.bullet_list([
        "Discovery: Uncovered ~200 images labeled as 'Bacterial Spot' that were 100% identical duplicates of 'Leaf Curl' in the public dataset.",
        "Action: We rigorously purged all duplicated/mislabeled images to prevent data leakage and artificial accuracy inflation.",
        "Impact: While we share the BDPapayaLeaf origin with prior studies [21-23], our models are evaluated on a cleaner, more rigorous subset.",
        "Split Ratio: Standardized 70 : 15 : 15 (Train : Val : Test) across both stages."
    ], 4.85, 2.65, 6.9, gap=0.7, size=13)
    slides.append(s)

    # SLIDE 6: Roboflow Annotation & ROI Strategy
    s = SlideBuilder(6, "II. Roboflow Annotation & ROI Extraction Strategy")
    s.text("Why healthy leaves have no bounding boxes, and how they flow through our diagnostic pipeline:", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    # Left Card
    s.rect(0.75, 1.85, 5.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(0.75, 1.85, 5.6, 0.6, fill=COLORS["light_blue"], line=COLORS["blue"], preset="roundRect")
    s.text("Precision Annotation on Roboflow", 1.0, 2.0, 5.1, 0.4, size=16, color=COLORS["blue"], bold=True)
    s.bullet_list([
        "Our team manually curated and re-annotated bounding boxes on Roboflow for all 4 disease classes.",
        "Normalized bounding box coordinates (x, y, w, h) capture lesions across varying scales, orientations, and lighting.",
        "Cropped ROIs are resized to 260x260 to match EfficientNet-B2 input specifications."
    ], 1.0, 2.7, 5.1, gap=0.8, size=13)

    # Right Card
    s.rect(6.65, 1.85, 5.4, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(6.65, 1.85, 5.4, 0.6, fill=COLORS["light_green"], line=COLORS["green"], preset="roundRect")
    s.text("Why NO Bounding Boxes for Healthy?", 6.9, 2.0, 4.9, 0.4, size=16, color=COLORS["green"], bold=True)
    s.bullet_list([
        "Scientific Rationale: Healthy leaves contain no disease lesions or visual abnormalities to bind.",
        "Cost Optimization: Eliminates redundant manual annotation effort and time.",
        "Workflow Logic: If Stage 1 detects 0 lesion boxes -> automatically route to Healthy / Background state.",
        "Farm Scalability: In real orchards, non-lesion detections naturally filter out soil, stones, and weeds!"
    ], 6.9, 2.7, 4.9, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 7: Addressing Class Imbalance & Augmentation
    s = SlideBuilder(7, "II. Addressing Class Imbalance & Data Augmentation")
    s.text("Class-weighted loss weights and spatial augmentations prevent majority-class bias during training.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    # Left Box: Loss weights
    s.rect(0.75, 1.85, 5.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Class-Weighted Loss Weights (wc = N / K*nc)", 1.0, 2.1, 5.1, 0.4, size=15, color=COLORS["dark"], bold=True)
    weights_data = [
        ("Healthy", 94.5, COLORS["red"]),
        ("Curl", 59.5, COLORS["amber"]),
        ("Bacterial Spot", 47.3, COLORS["blue"]),
        ("Ring Spot", 6.3, COLORS["cyan"]),
        ("Anthracnose", 3.4, COLORS["green"]),
    ]
    s.bar_chart(weights_data, 1.0, 2.6, 5.1, 3.2, max_value=100.0, value_suffix="x weight", label_size=11)

    # Right Box: Augmentations
    s.rect(6.65, 1.85, 5.4, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Oversampling & Data Augmentation", 6.9, 2.1, 4.9, 0.4, size=15, color=COLORS["dark"], bold=True)
    s.bullet_list([
        "Oversampling: Applied to minority classes (Healthy, Curl, Bacterial Spot) to balance batch distribution.",
        "Spatial Augmentations: Random rotations, horizontal/vertical flips, and spatial scaling.",
        "Color & Illumination: Brightness and contrast adjustments simulate variable orchard sunlight and shadows.",
        "Result: Highly balanced classification F1-scores exceeding 94% across all classes."
    ], 6.9, 2.7, 4.9, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 8: Overall System Architecture
    s = SlideBuilder(8, "III. Proposed Two-Stage Cascade Framework")
    s.text("A modular architecture decoupling lesion localization from fine-grained disease classification.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    # Diagram blocks
    s.shape_text("1. Input Field Image\n(Full Resolution)", 0.75, 2.2, 2.5, 1.2, COLORS["white"], line=COLORS["line"], size=14, bold=True)
    s.shape_text("2. Stage 1: YOLOv11m\nLesion Detector\n(mAP@0.5 = 77.7%)", 3.75, 2.2, 2.6, 1.2, COLORS["light_blue"], line=COLORS["blue"], size=14, color=COLORS["blue"], bold=True)
    s.shape_text("3. ROI Extraction\nCrop & Resize to\n260 x 260 x 3", 6.85, 2.2, 2.4, 1.2, COLORS["light_amber"], line=COLORS["amber"], size=14, color=COLORS["amber"], bold=True)
    s.shape_text("4. Stage 2: EfficientNet-B2\nROI Classifier\n(9.2M Params)", 9.75, 2.2, 2.3, 1.2, COLORS["light_green"], line=COLORS["green"], size=14, color=COLORS["green"], bold=True)
    
    s.shape_text("->", 3.32, 2.6, 0.35, 0.4, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.shape_text("->", 6.42, 2.6, 0.35, 0.4, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)
    s.shape_text("->", 9.32, 2.6, 0.35, 0.4, COLORS["bg"], line=None, size=18, color=COLORS["green"], bold=True)

    # Routing logic below
    s.rect(0.75, 3.8, 11.3, 2.6, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Intelligent Global Routing Logic:", 1.0, 4.0, 10.0, 0.35, size=16, color=COLORS["dark"], bold=True)
    s.bullet_list([
        "If Lesion Bounding Box Detected (Conf >= Threshold) -> Dynamic ROI Crop -> EfficientNet-B2 Disease Classifier.",
        "If NO Lesion Bounding Box Detected -> Automatically route to Healthy / Background diagnosis.",
        "Multi-Lesion Handling -> If multiple spots exist on one leaf, each ROI is classified independently and aggregated.",
        "End-to-End Speed -> Total latency is ~30 to 45 ms per image, fully enabling real-time video processing (>20 FPS)."
    ], 1.0, 4.5, 10.8, gap=0.5, size=13)
    slides.append(s)

    # SLIDE 9: YOLOv11m Architecture
    s = SlideBuilder(9, "III. Stage 1 – YOLOv11m Detector Architecture")
    s.text("Why YOLOv11m? Incorporates C3k2 blocks and C2PSA attention for superior multi-scale detection.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    s.rect(0.75, 1.85, 3.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(0.75, 1.85, 3.6, 0.6, fill=COLORS["light_blue"], line=COLORS["blue"], preset="roundRect")
    s.text("Why YOLOv11m?", 0.95, 2.0, 3.2, 0.4, size=16, color=COLORS["blue"], bold=True)
    s.bullet_list([
        "Latest advancement in the Ultralytics YOLO family.",
        "Achieves superior balance between accuracy, efficiency, and real-time speed.",
        "Inference time: only 29.66 ms per image."
    ], 0.95, 2.7, 3.2, gap=0.8, size=13)

    s.rect(4.6, 1.85, 3.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(4.6, 1.85, 3.6, 0.6, fill=COLORS["light_green"], line=COLORS["green"], preset="roundRect")
    s.text("C3k2 Block Innovation", 4.8, 2.0, 3.2, 0.4, size=16, color=COLORS["green"], bold=True)
    s.bullet_list([
        "Enhanced feature extraction capability with variable kernel sizes.",
        "Captures discriminative spatial features across scales.",
        "Effective for both tiny early-stage spots and large blight lesions."
    ], 4.8, 2.7, 3.2, gap=0.8, size=13)

    s.rect(8.45, 1.85, 3.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(8.45, 1.85, 3.6, 0.6, fill=COLORS["light_amber"], line=COLORS["amber"], preset="roundRect")
    s.text("C2PSA Spatial Attention", 8.65, 2.0, 3.2, 0.4, size=16, color=COLORS["amber"], bold=True)
    s.bullet_list([
        "Cross-Stage Partial Spatial Attention mechanism.",
        "Forces model to focus sharply on disease lesion boundaries.",
        "Actively suppresses background noise, leaf veins, and overlapping foliage."
    ], 8.65, 2.7, 3.2, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 10: EfficientNet-B2 Architecture
    s = SlideBuilder(10, "III. Stage 2 – EfficientNet-B2 Classifier Architecture")
    s.text("Lightweight, farm-ready scalability: achieving 80.1% ImageNet accuracy with only 9.2M parameters.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    s.metric("80.1%", "ImageNet Top-1 accuracy", 0.75, 1.85, 3.5, 1.2, COLORS["green"])
    s.metric("9.2M", "Parameters (5-6x smaller than ResNet)", 0.75, 3.25, 3.5, 1.2, COLORS["blue"])
    s.metric("1.0B", "FLOPs (13x faster than Inception)", 0.75, 4.65, 3.5, 1.2, COLORS["amber"])
    
    s.rect(4.6, 1.85, 7.45, 4.0, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(4.6, 1.85, 7.45, 0.6, fill=COLORS["light_green"], line=COLORS["green"], preset="roundRect")
    s.text("Core Technological Pillars for Farm Scalability", 4.85, 2.0, 7.0, 0.4, size=16, color=COLORS["green"], bold=True)
    s.bullet_list([
        "Compound Scaling: Principled scaling of network depth (d = a^phi), width (w = b^phi), and resolution (r = g^phi) simultaneously.",
        "MBConv Blocks: Mobile Inverted Bottleneck Convolutions with depthwise separable convolutions — reducing computation by k^2 times.",
        "Why EfficientNet-B2?: Orchards contain thousands of trees. This compact footprint enables high-speed deployment on agricultural drones, mobile phones, and edge IoT devices without heavy hardware costs."
    ], 4.85, 2.65, 6.9, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 11: End-to-End Inference Logic
    s = SlideBuilder(11, "III. End-to-End Inference & Multi-Lesion Logic")
    s.text("Robust decision rules handle variable lesion counts and environmental background seamlessly.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    s.rect(0.75, 1.85, 3.6, 4.3, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(0.75, 1.85, 3.6, 0.6, fill=COLORS["light_green"], line=COLORS["green"], preset="roundRect")
    s.text("0 Lesions Detected", 0.95, 2.0, 3.2, 0.4, size=16, color=COLORS["green"], bold=True)
    s.bullet_list([
        "Condition: YOLO detects no boxes above threshold.",
        "Diagnosis: Healthy / Background.",
        "Benefit: Automatically filters out soil, stones, and healthy leaves without false alarms."
    ], 0.95, 2.7, 3.2, gap=0.8, size=13)

    s.rect(4.6, 1.85, 3.6, 4.3, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(4.6, 1.85, 3.6, 0.6, fill=COLORS["light_blue"], line=COLORS["blue"], preset="roundRect")
    s.text("1 Lesion Detected", 4.8, 2.0, 3.2, 0.4, size=16, color=COLORS["blue"], bold=True)
    s.bullet_list([
        "Condition: Single lesion localized on leaf.",
        "Diagnosis: EfficientNet-B2 classifies cropped ROI.",
        "Benefit: Isolates lesion from leaf veins and background clutter."
    ], 4.8, 2.7, 3.2, gap=0.8, size=13)

    s.rect(8.45, 1.85, 3.6, 4.3, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(8.45, 1.85, 3.6, 0.6, fill=COLORS["light_amber"], line=COLORS["amber"], preset="roundRect")
    s.text(">1 Lesions Detected", 8.65, 2.0, 3.2, 0.4, size=16, color=COLORS["amber"], bold=True)
    s.bullet_list([
        "Condition: Co-infection or multiple spots on one leaf.",
        "Diagnosis: Crop all N ROIs -> Classify independently.",
        "Aggregation: Output highest confidence or highest clinical severity."
    ], 8.65, 2.7, 3.2, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 12: Stage 1 Detector Evaluation
    s = SlideBuilder(12, "IV. Experimental Results: Stage 1 Detector Evaluation")
    s.text("YOLOv11m achieved the best mAP@0.5 (77.67%), providing reliable localized ROIs for Stage 2.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    det_chart = [
        ("YOLOv11m (Selected)", 77.67, COLORS["green"]),
        ("YOLOv11s", 76.57, COLORS["blue"]),
        ("YOLOv11n", 74.71, COLORS["amber"]),
    ]
    s.bar_chart(det_chart, 0.75, 1.85, 6.5, 2.2, max_value=100.0, label_size=11)
    
    s.metric("0.802", "Precision (YOLOv11m)", 7.6, 1.85, 4.45, 1.0, COLORS["blue"])
    s.metric("0.816", "Recall (YOLOv11m)", 7.6, 3.05, 4.45, 1.0, COLORS["green"])
    
    s.rect(0.75, 4.3, 11.3, 2.1, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Analysis of Detection Performance across Disease Classes:", 1.0, 4.5, 10.0, 0.35, size=15, color=COLORS["dark"], bold=True)
    s.bullet_list([
        "Near-Perfect Localization: Bacterial Spot (99.3% mAP@0.5) and Leaf Curl (99.5% mAP@0.5) exhibit distinct visual features.",
        "Challenging Classes: Anthracnose (51.5%) and Ring Spot (60.4%) showed lower detection scores due to small lesion size and irregular distribution.",
        "Cascade Advantage: Even if Stage 1 localization is imperfect, cropping the ROI successfully removes enough background to let Stage 2 classify with >93% accuracy!"
    ], 1.0, 5.0, 10.8, gap=0.45, size=13)
    slides.append(s)

    # SLIDE 13: Stage 2 Full Cascade vs Baselines
    s = SlideBuilder(13, "IV. Experimental Results: Full Cascade vs. Baselines")
    s.text("Conclusively proving the ROI cropping advantage: +2.07% accuracy boost over full-image baseline!", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    casc_chart = [
        ("Whole-Image Baseline", 92.78, COLORS["muted"]),
        ("YOLOv11m + VGG16", 93.47, COLORS["red"]),
        ("YOLOv11m + DenseNet121", 94.16, COLORS["amber"]),
        ("YOLOv11m + ResNet50", 94.50, COLORS["blue"]),
        ("YOLOv11m + EfficientNetB2", 94.85, COLORS["green"]),
    ]
    s.bar_chart(casc_chart, 0.75, 1.85, 6.8, 4.4, max_value=100.0, label_size=11)
    
    s.rect(7.8, 1.85, 4.25, 4.4, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(7.8, 1.85, 4.25, 0.8, fill=COLORS["light_green"], line=COLORS["green"], preset="roundRect")
    s.text("🏆 Scientific Proof of Concept", 8.05, 2.05, 3.8, 0.4, size=16, color=COLORS["green"], bold=True)
    s.bullet_list([
        "Why did Accuracy jump from 92.78% to 94.85%?",
        "Using the exact same EfficientNet-B2 backbone, cropping ROIs stripped away soil, stones, and background clutter.",
        "This allowed the classifier to focus 100% on lesion morphology.",
        "EfficientNet-B2 outperformed VGG16, DenseNet121, and ResNet50 inside the cascade due to MBConv representations."
    ], 8.05, 2.85, 3.8, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 14: Class-Wise Performance & Confusion Matrix
    s = SlideBuilder(14, "IV. Class-Wise Performance & Confusion Matrix")
    s.text("276 correct predictions out of 291 test images — achieving strong diagonal stability across all classes.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    class_f1 = [
        ("Leaf Curl", 98.15, COLORS["cyan"]),
        ("Bacterial Spot", 95.59, COLORS["blue"]),
        ("Healthy", 94.12, COLORS["green"]),
        ("Anthracnose", 93.58, COLORS["red"]),
        ("Ring Spot", 93.17, COLORS["amber"]),
    ]
    s.bar_chart(class_f1, 0.75, 1.85, 6.2, 4.4, max_value=100.0, value_suffix="% F1", label_size=11)
    
    s.rect(7.2, 1.85, 4.85, 4.4, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Analysis of Confusion Matrix (Only 15 Errors):", 7.45, 2.1, 4.3, 0.35, size=15, color=COLORS["dark"], bold=True)
    s.bullet_list([
        "Highest Accuracy: Leaf Curl (98.15% F1) due to distinctive structural leaf deformation.",
        "Minority Class Success: Despite having fewer training samples, Healthy (94.12%) and Bacterial Spot (95.59%) performed exceptionally well due to class-weighted loss.",
        "Minor Misclassifications: Slight confusion between Anthracnose and Ring Spot (share visually similar early-stage brown/yellow ring spots).",
        "Overall: High diagonal concentration confirms diagnostic reliability."
    ], 7.45, 2.7, 4.4, gap=0.75, size=13)
    slides.append(s)

    # SLIDE 15: Comparison with Existing Literature
    s = SlideBuilder(15, "IV. Benchmarking Against Published Studies")
    s.text("Our model achieves competitive superiority on a strictly audited, cleaner dataset without duplicate leakage.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    lit_chart = [
        ("Darknet53 [23]", 84.78, COLORS["red"]),
        ("ResNet50 [21]", 87.95, COLORS["amber"]),
        ("HASPNet [22]", 93.87, COLORS["blue"]),
        ("Proposed Cascade", 94.85, COLORS["green"]),
    ]
    s.bar_chart(lit_chart, 0.75, 1.85, 6.2, 4.4, max_value=100.0, label_size=11)
    
    s.rect(7.2, 1.85, 4.85, 4.4, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(7.2, 1.85, 4.85, 0.6, fill=COLORS["light_blue"], line=COLORS["blue"], preset="roundRect")
    s.text("Why Our Benchmark is Highly Meaningful", 7.45, 2.0, 4.3, 0.4, size=15, color=COLORS["blue"], bold=True)
    s.bullet_list([
        "Cleaner Benchmark: Unlike prior studies on BDPapayaLeaf that may have trained on noisy data, our results were achieved after purging ~200 identical duplicates.",
        "Balanced Superiority: Prior Darknet studies [23] suffered from low F1-scores on Bacterial Spot (0.721) and Curl (0.765). Our model exceeds 95% and 98% on these exact classes!",
        "Contextual Reference: Proves that combining detection with lightweight CNNs outperforms heavy standalone architectures."
    ], 7.45, 2.7, 4.4, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 16: Summary of Key Contributions
    s = SlideBuilder(16, "V. Conclusion: Summary of Key Contributions")
    s.text("A robust, lightweight, and farm-ready computer vision framework for smart agriculture.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    contribs = [
        ("1. Background Suppression", "Decoupling localization (YOLOv11m) from classification (EfficientNet-B2) boosts accuracy by +2.07% over whole-image baselines.", COLORS["light_green"], COLORS["green"]),
        ("2. Field Robustness", "Accurately isolates lesions on occluded, overlapping, and awkwardly angled leaves without triggering false alarms on healthy foliage.", COLORS["light_blue"], COLORS["blue"]),
        ("3. Farm Scalability", "Achieves 94.85% accuracy with ~30-45 ms latency and only 9.2M params — optimized for edge devices and agricultural drones.", COLORS["light_amber"], COLORS["amber"]),
        ("4. Scientific Integrity", "Identified and resolved public dataset anomalies (purging ~200 duplicate images), establishing a reliable benchmark.", COLORS["light_red"], COLORS["red"]),
    ]
    for i, (head, body, fill, color) in enumerate(contribs):
        x = 0.75 + (i % 2) * 5.8
        y = 1.85 + (i // 2) * 2.2
        s.rect(x, y, 5.5, 1.95, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
        s.rect(x, y, 0.12, 1.95, fill=color, line=None)
        s.text(head, x + 0.3, y + 0.2, 5.0, 0.35, size=16, color=color, bold=True)
        s.text(body, x + 0.3, y + 0.65, 5.0, 1.1, size=13, color=COLORS["muted"])
    slides.append(s)

    # SLIDE 17: Future Work & Real-World Deployment
    s = SlideBuilder(17, "V. Conclusion: Future Work & Real-World Deployment")
    s.text("Moving from controlled evaluation toward reliable field decision support for agricultural robotics.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    s.rect(0.75, 1.85, 3.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(0.75, 1.85, 3.6, 0.6, fill=COLORS["light_green"], line=COLORS["green"], preset="roundRect")
    s.text("1. Dataset Expansion", 0.95, 2.0, 3.2, 0.4, size=16, color=COLORS["green"], bold=True)
    s.bullet_list([
        "Collect multi-environmental datasets across diverse farming regions.",
        "Explicitly incorporate environmental background flora (soil, stones, weeds) into background-rejection filters.",
        "Enhance robustness against varying orchard illumination."
    ], 0.95, 2.7, 3.2, gap=0.8, size=13)

    s.rect(4.6, 1.85, 3.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(4.6, 1.85, 3.6, 0.6, fill=COLORS["light_blue"], line=COLORS["blue"], preset="roundRect")
    s.text("2. Advanced Architectures", 4.8, 2.0, 3.2, 0.4, size=16, color=COLORS["blue"], bold=True)
    s.bullet_list([
        "Explore Vision Transformers (ViTs) and hybrid attention networks.",
        "Integrate self-supervised learning for subtle early-stage lesion recognition.",
        "Investigate ensemble learning methods for uncertainty estimation."
    ], 4.8, 2.7, 3.2, gap=0.8, size=13)

    s.rect(8.45, 1.85, 3.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.rect(8.45, 1.85, 3.6, 0.6, fill=COLORS["light_amber"], line=COLORS["amber"], preset="roundRect")
    s.text("3. Edge & Drone AI", 8.65, 2.0, 3.2, 0.4, size=16, color=COLORS["amber"], bold=True)
    s.bullet_list([
        "Port lightweight pipeline onto embedded IoT hardware (NVIDIA Jetson, Raspberry Pi).",
        "Deploy on agricultural drones for automated orchard monitoring.",
        "Support precision pesticide spraying to minimize chemical usage."
    ], 8.65, 2.7, 3.2, gap=0.8, size=13)
    slides.append(s)

    # SLIDE 18: Thank You & Q&A
    s = SlideBuilder(18, "Thank You for Your Attention! Questions & Discussion")
    s.text("We sincerely appreciate the opportunity to present our research at IEEE GTSD 2026.", 0.72, 1.25, 11.5, 0.4, size=16, color=COLORS["dark"], bold=True)
    
    # Left Card: Contact
    s.rect(0.75, 1.85, 5.6, 4.5, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Research Team & Contact Information:", 1.0, 2.1, 5.1, 0.4, size=16, color=COLORS["green"], bold=True)
    s.bullet_list([
        "Presenter: Dang Quang Pham (quang.wthz@gmail.com)",
        "Co-authors: Quang Sang Le | Manh Quan Bui | Minh Hieu Vu",
        "Affiliation: Faculty of Information Technology, Ho Chi Minh City University of Technology and Engineering (HCMUTE), Vietnam",
        "Acknowledgment: This research was funded by Ho Chi Minh City University of Technology and Engineering under Grant No. SV2026-08."
    ], 1.0, 2.7, 5.1, gap=0.8, size=13)

    # Right Card: Take-home
    s.rect(6.65, 1.85, 5.4, 4.5, fill=COLORS["dark"], line=None, preset="roundRect")
    s.text("Take-Home Message", 6.9, 2.1, 4.9, 0.4, size=18, color=COLORS["white"], bold=True, font="Aptos Display")
    s.rect(6.9, 2.6, 4.9, 0.04, fill=COLORS["green"], line=None)
    
    s.text("1. Localize First, Classify Second", 6.9, 2.8, 4.9, 0.35, size=15, color=COLORS["light_green"], bold=True)
    s.text("Cropping ROIs strips away soil, stones, and overlapping foliage.", 6.9, 3.15, 4.9, 0.4, size=12, color=COLORS["white"])
    
    s.text("2. 94.85% Cascade Accuracy", 6.9, 3.7, 4.9, 0.35, size=15, color=COLORS["light_blue"], bold=True)
    s.text("Outperformed whole-image EfficientNet-B2 baseline by +2.07%.", 6.9, 4.05, 4.9, 0.4, size=12, color=COLORS["white"])
    
    s.text("3. Farm-Ready Scalability", 6.9, 4.6, 4.9, 0.35, size=15, color=COLORS["light_amber"], bold=True)
    s.text("~30 ms latency and 9.2M params — ready for drones and IoT devices.", 6.9, 4.95, 4.9, 0.4, size=12, color=COLORS["white"])
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
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Papaya GTSD Conference Theme">
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
  <dc:title>IEEE GTSD 2026 Presentation: Papaya Leaf Disease Detection Cascade</dc:title>
  <dc:subject>Two-stage deep learning cascade framework</dc:subject>
  <dc:creator>HCMUTE Research Team</dc:creator>
  <cp:lastModifiedBy>HCMUTE Research Team</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


def app_xml(num_slides: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>GTSD 2026 PPTX Generator</Application>
  <PresentationFormat>On-screen Show (16:9)</PresentationFormat>
  <Slides>{num_slides}</Slides>
  <Company>Ho Chi Minh City University of Technology and Engineering (HCMUTE)</Company>
</Properties>
"""


SCRIPT_MD = """# IEEE GTSD 2026 Speaker Script and Notes
**Title**: A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification  
**Conference**: IEEE International Conference on Green Technology and Sustainable Development (GTSD 2026)  
**Authors**: Dang Quang Pham, Quang Sang Le, Manh Quan Bui, Minh Hieu Vu  
**Affiliation**: Faculty of Information Technology, Ho Chi Minh City University of Technology and Engineering (HCMUTE), Vietnam  

---

## Slide 1 - Title Slide
"Good morning, respected session chairs, professors, and fellow researchers. My name is [Your Name], representing our research team from Ho Chi Minh City University of Technology and Engineering. Today, I am honored to present our research titled: *'A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification'* accepted at GTSD 2026."

## Slide 2 - Agricultural Background & The Challenge
"To understand our motivation, let us look at the current challenges in papaya cultivation. Papaya is an economically vital crop, yet it is highly susceptible to foliar diseases like Anthracnose, Leaf Curl, and Ring Spot. A major problem farmers face in the field is that early disease symptoms look almost identical to nutrient deficiency. Currently, farmers rely on subjective visual inspection. When unsure, they often overuse chemical pesticides as a precaution, which leads to severe environmental pollution and increased farming costs. Therefore, an automated, highly accurate early detection system is urgently needed."

## Slide 3 - Limitations of Existing AI Approaches
"While deep learning has entered agriculture, existing single-stage methods face critical limitations in real-world orchards. First, why not just use a standard whole-image CNN? In real field conditions, leaves overlap, sit at awkward angles, or are occluded. Furthermore, background clutter—such as soil, stones, insects, and harsh lighting—severely confuses global CNN classifiers. Second, why not rely solely on a standalone object detector like YOLO for 5-class classification? In practice, this creates a confidence threshold dilemma: if we set a high threshold, YOLO misses subtle, early lesions; if we lower the threshold to catch everything, it triggers numerous false positives on background artifacts. This motivated us to design a hybrid approach."

## Slide 4 - Research Objectives & Proposed Solution
"To resolve these limitations, we propose a Two-Stage Deep Learning Cascade Framework combining YOLOv11m and EfficientNet-B2. Our core philosophy is simple yet powerful: *localize first, classify second*. In Stage 1, YOLOv11m acts as an attention filter, detecting and cropping diseased leaf regions—even if the leaf is partially hidden by other leaves or positioned at an awkward angle. In Stage 2, EfficientNet-B2 classifies these cleaned Regions of Interest without background noise. This approach combines the spatial robustness of object detection with the fine-grained discrimination of CNNs."

## Slide 5 - The BDPapayaLeaf Dataset & Rigorous Data Cleaning
"Our experiments utilize the BDPapayaLeaf dataset. However, during our initial preprocessing and exploratory data analysis, we made a critical discovery: approximately 200 images in the original public dataset labeled as 'Bacterial Spot' were actually 100% identical duplicates of images in the 'Leaf Curl' class. If left unaddressed, this data leakage would artificially inflate model performance. Our team rigorously audited and deleted these duplicated images. Therefore, while we compare our results with other published papers using BDPapayaLeaf, we emphasize that our evaluation is conducted on a much cleaner and more challenging dataset."

## Slide 6 - Roboflow Annotation & ROI Extraction Strategy
"To prepare the detection dataset, our team manually re-annotated and verified all disease bounding boxes using Roboflow. A key architectural decision in our workflow is how we handle the 'Healthy' class. We do not assign bounding boxes to healthy leaves. Why? Scientifically, healthy leaves have no disease spots to localize; practically, avoiding bounding box annotation on healthy leaves drastically reduces annotation costs. In our inference workflow, if YOLO scans a leaf and detects no lesions above the threshold, the image is classified as 'Healthy' or Background. In our experimental benchmark, Background corresponds to Healthy leaves to align with reference literature, but in real farm deployment, this exact logic seamlessly filters out soil, stones, and surrounding weeds."

## Slide 7 - Addressing Class Imbalance & Data Augmentation
"After cropping the ROIs, we faced a severe class imbalance problem. For instance, Anthracnose had over 6,500 training samples, while Healthy and Leaf Curl had fewer than 400. To prevent the classifier from biasing toward majority classes, we implemented Class-Weighted Sparse Categorical Cross-Entropy. As shown in the table, minority classes like Healthy and Leaf Curl were assigned high loss weights of 9.45 and 5.95, forcing the network to pay greater attention to them during gradient descent. Combined with oversampling and spatial augmentations, our model achieves exceptional balance across all classes."

## Slide 8 - Overall System Architecture & Workflow
"This diagram illustrates our complete Two-Stage Cascade workflow. When an image is captured in the orchard, it first enters the YOLOv11m detector. YOLO scans the image and identifies localized bounding boxes around suspicious disease spots. These regions are dynamically cropped, resized, and fed into the EfficientNet-B2 classifier to determine the specific disease. If an image passes through YOLO without any bounding box triggering above our minimum threshold, the system intelligently categorizes the leaf as Healthy. This modular architecture completely decouples lesion localization from disease classification."

## Slide 9 - Stage 1 – YOLOv11m Detector Architecture
"For our first stage, we selected YOLOv11m—the latest architecture in the YOLO family. Why YOLOv11? Because agricultural leaf lesions vary dramatically in size and shape. YOLOv11 incorporates newly introduced C3k2 blocks and the C2PSA spatial attention mechanism. The C2PSA attention module is particularly critical: it allows the network to focus sharply on discriminative lesion boundaries while actively suppressing visual noise from leaf veins, soil, and overlapping foliage. YOLOv11m provided the optimal balance between high localization accuracy and real-time inference speed."

## Slide 10 - Stage 2 – EfficientNet-B2 Classifier Architecture
"For our second stage, we chose EfficientNet-B2. This directly addresses our design goal of deploying to large-scale papaya farms with thousands of trees, where computational efficiency is paramount. Why EfficientNet-B2? As shown in our comparison, it achieves an 80.1% ImageNet baseline accuracy with only 9.2 million parameters and 1.0 billion FLOPs. Compared to traditional models like Inception-v4 or ResNet, EfficientNet-B2 delivers the exact same predictive power while reducing parameter size by 6 times and computational FLOPs by 13 times! It achieves this through principled Compound Scaling and lightweight MBConv blocks with depthwise separable convolutions."

## Slide 11 - End-to-End Inference & Multi-Lesion Logic
"In real-world farm conditions, a single leaf might have multiple disease spots, or no spots at all. Our inference logic handles all scenarios seamlessly. If zero bounding boxes are detected, the leaf is instantly diagnosed as Healthy. If multiple bounding boxes are found on a single leaf, our pipeline crops and classifies each lesion independently. The final system prediction can then be aggregated based on the highest confidence score or the most severe disease priority. Remarkably, the entire two-stage cascade executes in just 30 to 45 milliseconds per image, making it fully capable of real-time video processing on agricultural robotics."

## Slide 12 - Stage 1 – YOLOv11 Detector Evaluation
"Let us now examine our experimental results, starting with Stage 1 lesion localization. We evaluated three YOLOv11 variants: nano, small, and medium. As shown in the table, YOLOv11m achieved the best overall performance, reaching an mAP@0.5 of 77.67% and a recall of 81.62% with an inference time of just 29.66 milliseconds. Notice that localization was near-perfect for Bacterial Spot and Leaf Curl, exceeding 99% mAP. While Anthracnose and Ring Spot exhibited lower detection scores due to subtle, tiny spots, our second-stage classifier effectively compensates for these challenging visual boundaries."

## Slide 13 - Stage 2 – Full Cascade vs. Baselines
"This slide presents the most critical finding of our study: proving the superiority of our Two-Stage Cascade over traditional whole-image classification. When we trained a baseline EfficientNet-B2 directly on full images, it achieved an accuracy of 92.78%. However, when we integrated YOLOv11m ROI cropping with the exact same EfficientNet-B2 backbone, accuracy jumped to 94.85%, with a Macro F1-score of 94.92%! We also tested other backbones like VGG16, DenseNet121, and ResNet50 within our cascade, but EfficientNet-B2 outperformed them all. This conclusively proves our hypothesis: cropping disease regions and stripping away background noise is vital for agricultural AI."

## Slide 14 - Class-Wise Performance & Confusion Matrix
"Analyzing our class-wise performance and confusion matrix, we see that out of 291 test images, our model correctly predicted 276, making only 15 errors across all five classes. Notice the strong concentration along the diagonal of the confusion matrix. Leaf Curl achieved the highest F1-score at 98.15% due to its distinctive physical leaf curling. Even for challenging minority classes like Healthy and Bacterial Spot, our class-weighted loss ensured high F1-scores exceeding 94% and 95%. The few misclassifications occurred mainly between Anthracnose and Ring Spot, which share visually similar early-stage brown lesions."

## Slide 15 - Comparison with Existing Literature
"Finally, we benchmarked our proposed model against existing papaya leaf disease studies in the literature. As shown in Table VI, our YOLOv11m–EfficientNet-B2 cascade outperforms previous transfer learning approaches like ResNet50 (87.95%), optimized Darknet architectures (84.78%), and even attention-based HASPNet (93.87%). More importantly, remember that we achieved this 94.85% accuracy on a strictly audited dataset where ~200 duplicated images were removed. Furthermore, while previous studies struggled with severe class imbalances—scoring low on Bacterial Spot and Curl—our model demonstrates exceptional balance across all five categories."

## Slide 16 - Summary of Key Contributions
"In conclusion, this study makes four key contributions to smart agriculture. First, we demonstrated that our two-stage cascade effectively eliminates background clutter, increasing accuracy by over 2% compared to full-image baselines. Second, our system proves highly robust against real-world field conditions, successfully cropping lesions from occluded or angled leaves while intelligently handling healthy foliage. Third, with an inference speed of under 45 milliseconds and a lightweight parameter footprint, our framework is ready for real-time edge deployment. And fourth, our rigorous dataset cleaning establishes a reliable benchmark for future papaya disease research."

## Slide 17 - Future Work & Real-World Farm Deployment
"Looking ahead, we are expanding our research in three exciting directions. First, we plan to collect a larger, multi-environmental dataset from diverse orchards, explicitly incorporating field backgrounds like soil, stones, and weeds into our background-rejection logic. Second, we are exploring Vision Transformers and advanced attention mechanisms to further enhance early-stage lesion recognition. Finally, we are actively porting this lightweight pipeline onto embedded edge devices and agricultural drones to enable real-time orchard monitoring and targeted, precision pesticide spraying."

## Slide 18 - Thank You & Q&A
"This concludes my presentation. We would like to express our sincere gratitude to Ho Chi Minh City University of Technology and Engineering for funding this research under Grant SV2026-08. Thank you very much for your attention. I am now open to any questions, comments, or feedback."
"""

OUTLINE_MD = """# IEEE GTSD 2026 Presentation Outline
1. Title: A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification
2. Motivations: Agricultural Background & The Challenge
3. Motivations: Limitations of Existing AI Approaches (Whole-Image CNN vs Standalone YOLO)
4. Motivations: Research Objectives & Proposed Solution (Localize First, Classify Second)
5. Dataset Preparation: The BDPapayaLeaf Dataset & Rigorous Data Hygiene (~200 duplicates removed)
6. Dataset Preparation: Roboflow Annotation & ROI Extraction Strategy (Why NO boxes for Healthy)
7. Dataset Preparation: Addressing Class Imbalance & Data Augmentation (Class-weighted loss)
8. Framework: Overall System Architecture & Intelligent Routing Workflow
9. Framework: Stage 1 – YOLOv11m Detector Architecture (C3k2 Block & C2PSA Attention)
10. Framework: Stage 2 – EfficientNet-B2 Classifier Architecture (Compound Scaling & MBConv)
11. Framework: End-to-End Inference & Multi-Lesion Logic (~30-45ms latency)
12. Results: Stage 1 Detector Evaluation (YOLOv11m mAP@0.5 = 77.67%)
13. Results: Full Cascade vs. Baselines (+2.07% accuracy boost over whole-image baseline)
14. Results: Class-Wise Performance & Confusion Matrix (276/291 correct)
15. Results: Benchmarking Against Published Studies (Outperforming ResNet50, HASPNet, Darknet53)
16. Conclusion: Summary of Key Contributions
17. Conclusion: Future Work & Real-World Farm Deployment (Edge & Drone AI)
18. Conclusion: Thank You & Q&A
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
    print(f"Generated PPTX: {PPTX_PATH.resolve()}")
    print(f"Generated Script: {SCRIPT_PATH.resolve()}")
    print(f"Generated Outline: {OUTLINE_PATH.resolve()}")


if __name__ == "__main__":
    write_pptx()
