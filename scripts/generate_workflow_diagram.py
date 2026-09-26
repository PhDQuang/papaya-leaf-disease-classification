from __future__ import annotations
from pathlib import Path

OUT_DIR = Path("outputs/gtsd2026_presentation/diagrams")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SVG_PATH = OUT_DIR / "dataset_workflow_ieee_clean.svg"
HTML_PATH = OUT_DIR / "dataset_workflow_preview.html"

# We will generate a crisp, publication-quality vector SVG diagram 
# that eliminates overlapping arrows, clarifies the exact data splits, and separates YOLO vs CNN vs Final Test.

SVG_CONTENT = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="920" viewBox="0 0 1000 920" font-family="Arial, Helvetica, sans-serif">
  <defs>
    <!-- Arrow marker -->
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#333333"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#2E7D55"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#2F6FB6"/>
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#D38B1C"/>
    </marker>
    
    <!-- Drop shadows for boxes -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="1" dy="3" stdDeviation="3" flood-opacity="0.12"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1000" height="920" fill="#F8FAF7" rx="12"/>

  <!-- Title Section -->
  <text x="500" y="42" font-size="22" font-weight="bold" fill="#17231A" text-anchor="middle">
    BDPapayaLeaf Dataset Preparation &amp; Two-Stage Cascade Split Workflow
  </text>
  <text x="500" y="65" font-size="13" fill="#5B6B5F" text-anchor="middle">
    Rigorous 70 : 15 : 15 separation across Localization (YOLOv11m), Classification (EfficientNet-B2), and Final Benchmark
  </text>
  <line x1="50" y1="80" x2="950" y2="80" stroke="#CAD7CC" stroke-width="1.5"/>

  <!-- ================= STAGE 0: DATA CLEANING ================= -->
  <g id="stage0">
    <!-- Box: Raw Dataset -->
    <rect x="230" y="100" width="220" height="60" rx="8" fill="#FFFFFF" stroke="#2F6FB6" stroke-width="2" filter="url(#shadow)"/>
    <text x="340" y="125" font-size="14" font-weight="bold" fill="#17231A" text-anchor="middle">BDPapayaLeaf Dataset</text>
    <text x="340" y="145" font-size="12" fill="#5B6B5F" text-anchor="middle">Raw Public Images (5 Classes)</text>

    <!-- Arrow right -->
    <line x1="450" y1="130" x2="520" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Box: Data Cleaning -->
    <rect x="530" y="100" width="260" height="60" rx="8" fill="#FCEAE8" stroke="#C94A45" stroke-width="2" filter="url(#shadow)"/>
    <text x="660" y="125" font-size="14" font-weight="bold" fill="#C94A45" text-anchor="middle">Rigorous Data Cleaning</text>
    <text x="660" y="145" font-size="12" fill="#17231A" text-anchor="middle">Purged ~200 duplicates (BacterialSpot / Curl)</text>
  </g>

  <!-- Arrow down from Data Cleaning to Branch Split -->
  <line x1="660" y1="160" x2="660" y2="185" stroke="#333" stroke-width="2"/>
  <line x1="280" y1="185" x2="720" y2="185" stroke="#333" stroke-width="2"/>
  <line x1="280" y1="185" x2="280" y2="215" stroke="#333" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <line x1="720" y1="185" x2="720" y2="215" stroke="#333" stroke-width="2" marker-end="url(#arrow-green)"/>

  <!-- ================= STAGE 1: TWO MAIN BRANCHES ================= -->
  <g id="branches">
    <!-- Left Branch Header: Disease Classes -->
    <rect x="130" y="215" width="300" height="65" rx="8" fill="#E7F0FA" stroke="#2F6FB6" stroke-width="2" filter="url(#shadow)"/>
    <text x="280" y="240" font-size="14" font-weight="bold" fill="#2F6FB6" text-anchor="middle">4 Disease Classes (1,707 Images)</text>
    <text x="280" y="260" font-size="12" fill="#17231A" text-anchor="middle">Anthracnose, Bacterial Spot, Curl, Ring Spot</text>
    <text x="280" y="275" font-size="11" font-weight="bold" fill="#5B6B5F" text-anchor="middle">+ Roboflow Bounding Box Annotation</text>

    <!-- Right Branch Header: Healthy Class -->
    <rect x="570" y="215" width="300" height="65" rx="8" fill="#E6F2EA" stroke="#2E7D55" stroke-width="2" filter="url(#shadow)"/>
    <text x="720" y="240" font-size="14" font-weight="bold" fill="#2E7D55" text-anchor="middle">1 Healthy Class (228 Images)</text>
    <text x="720" y="260" font-size="12" fill="#17231A" text-anchor="middle">Normal Papaya Leaves</text>
    <text x="720" y="275" font-size="11" font-style="italic" fill="#5B6B5F" text-anchor="middle">(No Bounding Boxes — Full Images Only)</text>
  </g>

  <!-- Arrows down to 70:15:15 Split labels -->
  <line x1="280" y1="280" x2="280" y2="310" stroke="#2F6FB6" stroke-width="2" marker-end="url(#arrow-blue)"/>
  <line x1="720" y1="280" x2="720" y2="310" stroke="#2E7D55" stroke-width="2" marker-end="url(#arrow-green)"/>

  <!-- Split Labels -->
  <rect x="200" y="310" width="160" height="30" rx="5" fill="#2F6FB6"/>
  <text x="280" y="330" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">Split 70 : 15 : 15</text>

  <rect x="640" y="310" width="160" height="30" rx="5" fill="#2E7D55"/>
  <text x="720" y="330" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">Split 70 : 15 : 15</text>

  <!-- ================= STAGE 2: YOLO DETECTION SUBSET ================= -->
  <!-- Arrows from Left Split to YOLO Box -->
  <line x1="280" y1="340" x2="280" y2="370" stroke="#2F6FB6" stroke-width="2" marker-end="url(#arrow-blue)"/>

  <!-- Big Container: YOLO Detection Stage -->
  <rect x="60" y="370" width="440" height="150" rx="10" fill="#FFFFFF" stroke="#2F6FB6" stroke-width="2" stroke-dasharray="6,4" filter="url(#shadow)"/>
  <text x="280" y="395" font-size="15" font-weight="bold" fill="#2F6FB6" text-anchor="middle">
    Stage 1: YOLOv11m Detection Dataset (4 Disease Classes Only)
  </text>
  <text x="280" y="413" font-size="12" fill="#5B6B5F" text-anchor="middle">Total: 1,707 Images with Normalized Coordinate Bounding Boxes</text>

  <!-- 3 YOLO Boxes -->
  <rect x="80" y="430" width="120" height="70" rx="6" fill="#E7F0FA" stroke="#2F6FB6" stroke-width="1.5"/>
  <text x="140" y="455" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Train YOLO</text>
  <text x="140" y="475" font-size="14" font-weight="bold" fill="#2F6FB6" text-anchor="middle">1,194 images</text>
  <text x="140" y="490" font-size="11" fill="#5B6B5F" text-anchor="middle">(70% Train)</text>

  <rect x="220" y="430" width="120" height="70" rx="6" fill="#E7F0FA" stroke="#2F6FB6" stroke-width="1.5"/>
  <text x="280" y="455" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Val YOLO</text>
  <text x="280" y="475" font-size="14" font-weight="bold" fill="#2F6FB6" text-anchor="middle">256 images</text>
  <text x="280" y="490" font-size="11" fill="#5B6B5F" text-anchor="middle">(15% Validation)</text>

  <rect x="360" y="430" width="120" height="70" rx="6" fill="#E7F0FA" stroke="#2F6FB6" stroke-width="1.5"/>
  <text x="420" y="455" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Test YOLO</text>
  <text x="420" y="475" font-size="14" font-weight="bold" fill="#2F6FB6" text-anchor="middle">257 images</text>
  <text x="420" y="490" font-size="11" fill="#5B6B5F" text-anchor="middle">(15% Test)</text>

  <!-- ================= STAGE 2.5: HEALTHY SUBSET ================= -->
  <!-- Arrows from Right Split to Healthy Boxes -->
  <line x1="720" y1="340" x2="720" y2="370" stroke="#2E7D55" stroke-width="2" marker-end="url(#arrow-green)"/>

  <rect x="550" y="370" width="340" height="150" rx="10" fill="#FFFFFF" stroke="#2E7D55" stroke-width="2" stroke-dasharray="6,4" filter="url(#shadow)"/>
  <text x="720" y="395" font-size="15" font-weight="bold" fill="#2E7D55" text-anchor="middle">
    Healthy Leaf Subset (Full Images)
  </text>
  <text x="720" y="413" font-size="12" fill="#5B6B5F" text-anchor="middle">Total: 228 Images (No Bounding Boxes Assigned)</text>

  <rect x="565" y="430" width="100" height="70" rx="6" fill="#E6F2EA" stroke="#2E7D55" stroke-width="1.5"/>
  <text x="615" y="455" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Train Healthy</text>
  <text x="615" y="475" font-size="14" font-weight="bold" fill="#2E7D55" text-anchor="middle">160 images</text>
  <text x="615" y="490" font-size="11" fill="#5B6B5F" text-anchor="middle">(70% Train)</text>

  <rect x="675" y="430" width="100" height="70" rx="6" fill="#E6F2EA" stroke="#2E7D55" stroke-width="1.5"/>
  <text x="725" y="455" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Val Healthy</text>
  <text x="725" y="475" font-size="14" font-weight="bold" fill="#2E7D55" text-anchor="middle">34 images</text>
  <text x="725" y="490" font-size="11" fill="#5B6B5F" text-anchor="middle">(15% Val)</text>

  <rect x="785" y="430" width="100" height="70" rx="6" fill="#E6F2EA" stroke="#2E7D55" stroke-width="1.5"/>
  <text x="835" y="455" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Test Healthy</text>
  <text x="835" y="475" font-size="14" font-weight="bold" fill="#2E7D55" text-anchor="middle">34 images</text>
  <text x="835" y="490" font-size="11" fill="#5B6B5F" text-anchor="middle">(15% Test)</text>


  <!-- ================= STAGE 3: ROI EXTRACTION & MERGING INTO CNN ================= -->
  <!-- Arrows from YOLO Boxes down to ROI Extraction -->
  <line x1="140" y1="500" x2="140" y2="550" stroke="#2F6FB6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
  <line x1="280" y1="500" x2="280" y2="550" stroke="#2F6FB6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>
  <line x1="420" y1="500" x2="420" y2="550" stroke="#2F6FB6" stroke-width="1.5" marker-end="url(#arrow-blue)"/>

  <rect x="80" y="550" width="340" height="45" rx="8" fill="#FFF3DE" stroke="#D38B1C" stroke-width="2" filter="url(#shadow)"/>
  <text x="250" y="572" font-size="13" font-weight="bold" fill="#D38B1C" text-anchor="middle">Dynamic ROI Extraction &amp; Crop</text>
  <text x="250" y="588" font-size="11" fill="#17231A" text-anchor="middle">Cropping multiple lesions per leaf -&gt; Resize to 260x260</text>

  <!-- Arrows from ROI down to CNN Stage -->
  <line x1="140" y1="595" x2="140" y2="670" stroke="#D38B1C" stroke-width="2" marker-end="url(#arrow-amber)"/>
  <line x1="280" y1="595" x2="280" y2="670" stroke="#D38B1C" stroke-width="2" marker-end="url(#arrow-amber)"/>
  <line x1="420" y1="595" x2="420" y2="670" stroke="#D38B1C" stroke-width="2" marker-end="url(#arrow-amber)"/>

  <!-- Arrows from Healthy directly merging into CNN Train/Val/Test (NO OVERLAPPING!) -->
  <path d="M 615 500 L 615 620 L 160 620 L 160 670" fill="none" stroke="#2E7D55" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-green)"/>
  <text x="380" y="615" font-size="11" font-weight="bold" fill="#2E7D55">+160 Healthy Full Images into Train</text>

  <path d="M 725 500 L 725 635 L 300 635 L 300 670" fill="none" stroke="#2E7D55" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-green)"/>
  <text x="510" y="630" font-size="11" font-weight="bold" fill="#2E7D55">+34 Healthy Full Images into Val</text>

  <path d="M 835 500 L 835 650 L 440 650 L 440 670" fill="none" stroke="#2E7D55" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow-green)"/>
  <text x="640" y="645" font-size="11" font-weight="bold" fill="#2E7D55">+34 Healthy Full Images into Test</text>


  <!-- Big Container: CNN Classification Stage -->
  <rect x="60" y="670" width="440" height="150" rx="10" fill="#FFFFFF" stroke="#D38B1C" stroke-width="2" stroke-dasharray="6,4" filter="url(#shadow)"/>
  <text x="280" y="695" font-size="15" font-weight="bold" fill="#D38B1C" text-anchor="middle">
    Stage 2: EfficientNet-B2 Classification Dataset (All 5 Classes)
  </text>
  <text x="280" y="713" font-size="12" fill="#5B6B5F" text-anchor="middle">Total: 11,111 Samples (4 Disease ROI Classes + 1 Healthy Full Image Class)</text>

  <!-- 3 CNN Boxes -->
  <rect x="80" y="730" width="120" height="70" rx="6" fill="#FFF3DE" stroke="#D38B1C" stroke-width="1.5"/>
  <text x="140" y="755" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Train CNN</text>
  <text x="140" y="775" font-size="14" font-weight="bold" fill="#D38B1C" text-anchor="middle">7,562 samples</text>
  <text x="140" y="790" font-size="11" fill="#5B6B5F" text-anchor="middle">(70% Train)</text>

  <rect x="220" y="730" width="120" height="70" rx="6" fill="#FFF3DE" stroke="#D38B1C" stroke-width="1.5"/>
  <text x="280" y="755" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Val CNN</text>
  <text x="280" y="775" font-size="14" font-weight="bold" fill="#D38B1C" text-anchor="middle">1,713 samples</text>
  <text x="280" y="790" font-size="11" fill="#5B6B5F" text-anchor="middle">(15% Validation)</text>

  <rect x="360" y="730" width="120" height="70" rx="6" fill="#FFF3DE" stroke="#D38B1C" stroke-width="1.5"/>
  <text x="420" y="755" font-size="13" font-weight="bold" fill="#17231A" text-anchor="middle">Test CNN</text>
  <text x="420" y="775" font-size="14" font-weight="bold" fill="#D38B1C" text-anchor="middle">1,836 samples</text>
  <text x="420" y="790" font-size="11" fill="#5B6B5F" text-anchor="middle">(15% Test)</text>


  <!-- ================= STAGE 4: FINAL CASCADE BENCHMARK SET ================= -->
  <!-- We draw clean arrows from Test YOLO (257) and Test Healthy (34) to Final Benchmark Set -->
  <path d="M 460 500 L 520 500 L 520 745 L 560 745" fill="none" stroke="#2F6FB6" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
  <text x="535" y="680" font-size="11" font-weight="bold" fill="#2F6FB6" transform="rotate(90,535,680)">257 Disease Test Images</text>

  <path d="M 885 500 L 885 745 L 860 745" fill="none" stroke="#2E7D55" stroke-width="2.5" marker-end="url(#arrow-green)"/>
  <text x="895" y="680" font-size="11" font-weight="bold" fill="#2E7D55" transform="rotate(90,895,680)">34 Healthy Test Images</text>

  <!-- Big Box: Final Test -->
  <rect x="560" y="700" width="300" height="90" rx="10" fill="#E7F0FA" stroke="#2F6FB6" stroke-width="2.5" filter="url(#shadow)"/>
  <text x="710" y="728" font-size="16" font-weight="bold" fill="#17231A" text-anchor="middle">Final Cascade Benchmark Set</text>
  <text x="710" y="752" font-size="20" font-weight="bold" fill="#2F6FB6" text-anchor="middle">291 Full Images (5 Classes)</text>
  <text x="710" y="775" font-size="12" font-weight="bold" fill="#2E7D55" text-anchor="middle">Achieved 94.85% Accuracy (276/291 Correct)</text>

  <!-- Legend Box at bottom -->
  <rect x="60" y="845" width="880" height="50" rx="6" fill="#EEF2EE" stroke="#CAD7CC"/>
  <text x="80" y="868" font-size="12" font-weight="bold" fill="#17231A">Key Architectural Principles:</text>
  <text x="80" y="885" font-size="12" fill="#5B6B5F">
    • No Bounding Boxes for Healthy leaves (saves annotation cost &amp; prevents false positives).  
    • 4 Disease classes split 70:15:15 for YOLOv11m localization -> ROI crops + Healthy split 70:15:15 for EfficientNet-B2 classification.
  </text>
  <text x="730" y="875" font-size="12" font-weight="bold" fill="#2F6FB6">IEEE GTSD 2026 Ready</text>
</svg>
"""

SVG_PATH.write_text(SVG_CONTENT, encoding="utf-8")

# Also wrap in HTML for easy local browser viewing
HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>BDPapayaLeaf Dataset Workflow Diagram</title>
  <style>
    body {{
      background-color: #222;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 30px;
      margin: 0;
      font-family: sans-serif;
    }}
    .container {{
      background-color: #fff;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
  </style>
</head>
<body>
  <div class="container">
    {SVG_CONTENT}
  </div>
</body>
</html>
"""
HTML_PATH.write_text(HTML_CONTENT, encoding="utf-8")

print(f"Generated clean SVG: {SVG_PATH.resolve()}")
print(f"Generated preview HTML: {HTML_PATH.resolve()}")
