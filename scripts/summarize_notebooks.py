from __future__ import annotations
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

notebook_dir = Path("notebooks")
main_files = [
    "01_data_preparation.ipynb",
    "02_train_yolov11_detector.ipynb",
    "03_train_efficientnet_b0_classifier.ipynb",
    "04_train_efficientnet_b1_classifier.ipynb",
    "05_train_efficientnet_b2_classifier.ipynb",
    "06_evaluate_yolov11_efficientnet_cascade.ipynb",
    "07_benchmark_model_throughput_colab.ipynb"
]

for name in main_files:
    f = notebook_dir / name
    if not f.exists():
        continue
    print(f"\n{'='*70}")
    print(f"NOTEBOOK: {f.name}")
    print(f"{'='*70}")
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        cells = data.get("cells", [])
        for i, cell in enumerate(cells):
            cell_type = cell.get("cell_type", "")
            source = "".join(cell.get("source", []))
            if not source.strip():
                continue
            first_line = [l.strip() for l in source.split("\n") if l.strip()][0]
            if cell_type == "markdown":
                print(f"  [MD   #{i:2d}] {first_line[:100]}")
            elif cell_type == "code":
                # Print title comment or first line of code
                lines = [l.strip() for l in source.split("\n") if l.strip()]
                title = lines[0] if lines[0].startswith("#") else f"Code ({len(lines)} lines): {lines[0]}"
                print(f"  [CODE #{i:2d}] {title[:100]}")
    except Exception as e:
        print(f"  Error reading {f}: {e}")
