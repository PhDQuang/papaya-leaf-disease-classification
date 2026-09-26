"""Vẽ lại biểu đồ đường cong huấn luyện results.png từ results.csv của Ultralytics.

Ultralytics sinh results.png ngay khi kết thúc huấn luyện, nhưng tệp này dễ bị bỏ sót
khi tải kết quả từ Colab về. Vì toàn bộ dữ liệu của biểu đồ nằm trong results.csv, ta
dựng lại được mà không cần huấn luyện lại.

Bố cục lưới 2x5 và kiểu vẽ (điểm thật + đường làm trơn Gaussian) mô phỏng hàm
ultralytics.utils.plotting.plot_results, để hình sinh ra đồng bộ với các biểu đồ
Ultralytics khác đang dùng trong báo cáo.

Cách dùng:
    python scripts/plot_yolo_results.py                    # mọi thư mục dưới outputs/yolo/
    python scripts/plot_yolo_results.py outputs/yolo/yolov11_m
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.ndimage import gaussian_filter1d  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# Thứ tự 10 ô biểu đồ đúng như Ultralytics: hàng 1 là huấn luyện + P/R,
# hàng 2 là xác thực + mAP.
PANELS = [
    "train/box_loss",
    "train/cls_loss",
    "train/dfl_loss",
    "metrics/precision(B)",
    "metrics/recall(B)",
    "val/box_loss",
    "val/cls_loss",
    "val/dfl_loss",
    "metrics/mAP50(B)",
    "metrics/mAP50-95(B)",
]


def plot_run(run_dir: Path, overwrite: bool = False) -> Path | None:
    csv_path = run_dir / "results.csv"
    if not csv_path.exists():
        print(f"[bo qua] {run_dir.name}: khong co results.csv")
        return None

    png_path = run_dir / "results.png"
    if png_path.exists() and not overwrite:
        print(f"[bo qua] {run_dir.name}: results.png da ton tai (dung --force de ghi de)")
        return None

    data = pd.read_csv(csv_path)
    data.columns = [c.strip() for c in data.columns]
    x = data["epoch"].to_numpy()

    missing = [c for c in PANELS if c not in data.columns]
    if missing:
        print(f"[loi ] {run_dir.name}: results.csv thieu cot {missing}")
        return None

    fig, axes = plt.subplots(2, 5, figsize=(12, 6), tight_layout=True)
    axes = axes.ravel()
    for ax, col in zip(axes, PANELS):
        y = data[col].to_numpy(dtype="float")
        ax.plot(x, y, marker=".", linewidth=2, markersize=8, label=run_dir.name)
        # sigma=3 là giá trị Ultralytics dùng, giữ nguyên để đường trơn trông giống nhau.
        ax.plot(x, gaussian_filter1d(y, sigma=3), ":", linewidth=2, label="smooth")
        ax.set_title(col, fontsize=12)
        ax.set_xlabel("epoch", fontsize=9)
        ax.tick_params(labelsize=8)
    axes[1].legend(fontsize=9)

    fig.savefig(png_path, dpi=200)
    plt.close(fig)
    print(f"[xong ] {png_path.relative_to(ROOT)}  ({len(x)} epoch)")
    return png_path


def main(argv: list[str]) -> None:
    force = "--force" in argv
    targets = [a for a in argv if not a.startswith("--")]

    if targets:
        dirs = [Path(t) if Path(t).is_absolute() else ROOT / t for t in targets]
    else:
        dirs = sorted(d for d in (ROOT / "outputs" / "yolo").iterdir() if d.is_dir())

    for d in dirs:
        plot_run(d, overwrite=force)


if __name__ == "__main__":
    main(sys.argv[1:])
