from __future__ import annotations

import html
import zipfile
from datetime import datetime, timezone
from pathlib import Path


OUT_DIR = Path("outputs/conference_presentation")
PPTX_PATH = OUT_DIR / "experimental_results_runtime_slide.pptx"
NOTES_PATH = OUT_DIR / "experimental_results_runtime_notes.md"

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
        line: str | None = COLORS["line"],
        size: int = 14,
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
        self.text(value, x + 0.2, y + 0.14, w - 0.28, 0.42, size=23, color=color, bold=True, anchor="mid", font="Aptos Display")
        self.text(label, x + 0.2, y + 0.58, w - 0.28, h - 0.62, size=10, color=COLORS["muted"])

    def bar(self, label: str, value: float, x: float, y: float, w: float, color: str) -> None:
        self.text(label, x, y - 0.02, 1.62, 0.22, size=9, color=COLORS["dark"], align="r")
        self.rect(x + 1.75, y + 0.03, w, 0.16, fill=COLORS["gray"], line=None, preset="roundRect")
        self.rect(x + 1.75, y + 0.03, w * value / 96.0, 0.16, fill=color, line=None, preset="roundRect")
        self.text(f"{value:.2f}%", x + 1.75 + w + 0.1, y - 0.03, 0.6, 0.24, size=9, color=COLORS["muted"])

    def table_row(self, cells: list[str], x: float, y: float, widths: list[float], fill: str, bold: bool = False) -> None:
        cx = x
        for cell, width in zip(cells, widths, strict=True):
            self.rect(cx, y, width, 0.36, fill=fill, line=COLORS["line"])
            self.text(cell, cx + 0.03, y + 0.06, width - 0.06, 0.22, size=8, color=COLORS["dark"], bold=bold, align="ctr", anchor="mid")
            cx += width

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>
      </p:grpSpPr>
      {''.join(self.items)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""


def build_slide() -> str:
    s = Slide()
    s.text("Experimental Results and Farm-Scale Runtime", 0.55, 0.28, 10.4, 0.48, size=25, color=COLORS["dark"], bold=True, font="Aptos Display")
    s.text("Best cascade: YOLOv11m + EfficientNet-B2 on the 291-image end-to-end test set", 0.58, 0.82, 10.8, 0.28, size=12, color=COLORS["muted"])
    s.rect(0.55, 1.12, 1.2, 0.05, fill=COLORS["green"], line=None)
    s.rect(1.78, 1.12, 0.55, 0.05, fill=COLORS["amber"], line=None)
    s.rect(2.36, 1.12, 0.55, 0.05, fill=COLORS["blue"], line=None)

    s.metric("94.85%", "accuracy", 0.7, 1.45, 2.0, 1.02, COLORS["green"])
    s.metric("94.92%", "macro F1", 2.95, 1.45, 2.0, 1.02, COLORS["blue"])
    s.metric("276/291", "correct predictions", 0.7, 2.7, 2.0, 1.02, COLORS["amber"])
    s.metric("1.03 img/s", "measured throughput", 2.95, 2.7, 2.0, 1.02, COLORS["cyan"])

    s.rect(0.7, 4.08, 4.25, 1.62, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Detector result", 0.92, 4.24, 3.7, 0.24, size=13, color=COLORS["dark"], bold=True)
    s.text("YOLOv11m reached 80.24% precision, 81.62% recall, 77.67% mAP@0.5, and 65.20% mAP@0.5:0.95.", 0.92, 4.62, 3.78, 0.65, size=10, color=COLORS["muted"])

    s.rect(5.35, 1.45, 3.0, 4.25, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Pipeline comparison", 5.55, 1.65, 2.55, 0.25, size=13, color=COLORS["dark"], bold=True)
    s.bar("Full-image B2", 92.78, 5.55, 2.25, 1.0, COLORS["muted"])
    s.bar("YOLOm + VGG16", 93.47, 5.55, 2.73, 1.0, COLORS["amber"])
    s.bar("YOLOm + DenseNet", 94.16, 5.55, 3.21, 1.0, COLORS["cyan"])
    s.bar("YOLOm + ResNet", 94.50, 5.55, 3.69, 1.0, COLORS["blue"])
    s.bar("YOLOm + B2", 94.85, 5.55, 4.17, 1.0, COLORS["green"])
    s.shape_text("+2.07 percentage points over full-image EfficientNet-B2", 5.62, 4.92, 2.45, 0.45, COLORS["light_green"], line=COLORS["green"], size=9, color=COLORS["green"], bold=True)

    s.rect(8.75, 1.45, 3.72, 4.25, fill=COLORS["white"], line=COLORS["line"], preset="roundRect")
    s.text("Farm-scale estimate", 8.98, 1.65, 3.25, 0.25, size=13, color=COLORS["dark"], bold=True)
    s.text("Assumption: one tree = one captured image; sequential processing; model loading excluded.", 8.98, 1.98, 3.08, 0.42, size=8, color=COLORS["muted"])
    widths = [0.76, 0.92, 0.92, 0.92]
    s.table_row(["Trees", "1 img/tree", "3 imgs/tree", "Use case"], 8.98, 2.57, widths, COLORS["light_blue"], bold=True)
    s.table_row(["1,000", "16.2 min", "48.7 min", "small"], 8.98, 2.93, widths, COLORS["white"])
    s.table_row(["1,500", "24.3 min", "73.0 min", "medium"], 8.98, 3.29, widths, COLORS["white"])
    s.table_row(["1,999", "32.4 min", "97.3 min", "large"], 8.98, 3.65, widths, COLORS["white"])
    s.shape_text("Operational takeaway: the system can screen a 1xxx-tree farm in under 35 minutes with one image per tree, or under 100 minutes with three angles per tree.", 8.98, 4.35, 3.06, 0.85, COLORS["light_amber"], line=COLORS["amber"], size=9, color=COLORS["dark"], bold=True, align="l")

    s.text("Implications: ROI cropping improves accuracy; batched GPU inference or parallel devices can reduce survey time further.", 0.7, 6.15, 10.8, 0.3, size=12, color=COLORS["dark"], bold=True)
    s.text("Runtime source: throughput benchmark on 291-image notebook-06 test set, YOLOv11m + EfficientNet-B2 = 973 ms/image.", 0.7, 6.56, 10.8, 0.25, size=9, color=COLORS["muted"])
    s.rect(0.55, 7.18, 12.25, 0.01, fill=COLORS["line"], line=None)
    s.text("Papaya leaf disease detection and classification | Experimental Results", 0.58, 7.22, 7.5, 0.18, size=8, color=COLORS["muted"])
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
  <dc:title>Experimental Results and Farm-Scale Runtime</dc:title>
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


NOTES = """# Experimental Results and Runtime Scalability - Speaker Notes

This slide summarizes both model quality and practical runtime.

The best result is the YOLOv11m plus EfficientNet-B2 cascade. On the end-to-end 291-image test set, it reached 94.85 percent accuracy and 94.92 percent macro F1, correctly predicting 276 out of 291 images. This result is higher than the full-image EfficientNet-B2 baseline, which reached 92.78 percent accuracy, showing that localizing the disease region before classification helps remove background noise.

For runtime, the benchmark measured about 973 milliseconds per image, or roughly 1.03 images per second, for YOLOv11m plus EfficientNet-B2. If a farm has around 1,000 to 1,999 papaya trees and we capture one image per tree, sequential analysis would take about 16 to 32 minutes. If we capture three angles per tree for better coverage, the analysis would take about 49 to 97 minutes.

The key practical message is that the method is not only accurate, but also scalable for medium-sized farms. In real deployment, batching on GPU, using multiple devices, or processing images in parallel can reduce the total survey time further.
"""


def write_pptx() -> None:
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
        z.writestr("ppt/slides/slide1.xml", build_slide())
        z.writestr("ppt/slides/_rels/slide1.xml.rels", rels_xml([
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
        ]))
    NOTES_PATH.write_text(NOTES, encoding="utf-8")
    print(PPTX_PATH)
    print(NOTES_PATH)


if __name__ == "__main__":
    write_pptx()
