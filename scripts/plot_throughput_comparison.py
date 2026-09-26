"""Vẽ biểu đồ so sánh độ trễ và độ chính xác của bốn cấu hình xếp tầng.

Nguồn số liệu: outputs/Performance_Benchmark/model_throughput_*.csv — chính là tệp
đã sinh ra Bảng thời gian suy luận ở mục 5.6 của báo cáo, nên biểu đồ và bảng luôn
khớp nhau.

Bố cục hai khung:
  (a) Độ trễ đầu-cuối: bốn nhóm thanh ngang, mỗi nhóm bốn thống kê xếp theo thứ tự
      tăng dần (trung vị → trung bình → P90 → P95), tô bằng dải màu lam đơn sắc
      đậm dần để thứ tự thống kê đọc được ngay cả khi in đen trắng.
  (b) Độ chính xác mức ảnh: biểu đồ chấm thay vì thanh, vì bốn giá trị nằm sát nhau
      trong khoảng 93,5–94,9% — thanh có gốc 0 sẽ nén hết khác biệt thành vô hình.
      Cấu hình đề xuất được tô lam, ba cấu hình tham chiếu để xám.

Thứ tự bốn cấu hình giống nhau ở cả hai khung (xếp theo độ chính xác giảm dần) để
người đọc dò ngang được: cấu hình đứng đầu về độ chính xác cũng là cấu hình chậm nhất.

Cách dùng:
    python scripts/plot_throughput_comparison.py [--force]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
BENCH_DIR = ROOT / "outputs" / "Performance_Benchmark"
OUT_PNG = BENCH_DIR / "throughput_comparison.png"

# Dải màu tuần tự một sắc lam, độ sáng giảm đều (đã kiểm bằng validate_palette --ordinal).
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#184f95"]
ACCENT = "#2a78d6"
MUTED = "#9ca3af"
TEXT = "#1f2937"
GRID = "#e5e7eb"

# Tên hiển thị gọn lại cho vừa trục.
DISPLAY = {
    "YOLOv11m__EfficientNetB2": "YOLOv11m +\nEfficientNet-B2",
    "YOLOv11m__ResNet50": "YOLOv11m +\nResNet50",
    "YOLOv11m__DenseNet121": "YOLOv11m +\nDenseNet121",
    "YOLOv11m__VGG16": "YOLOv11m +\nVGG16",
}
PROPOSED = "YOLOv11m__EfficientNetB2"

# (cột trong CSV, nhãn hiển thị) xếp theo thứ tự thống kê tăng dần.
STATS = [
    ("median_ms", "Trung vị"),
    ("milliseconds_per_image", "Trung bình"),
    ("p90_ms", "P90"),
    ("p95_ms", "P95"),
]


def _vn(x: float, decimals: int = 0) -> str:
    """Định dạng số theo quy ước tiếng Việt: chấm phân cách nghìn, phẩy thập phân."""
    s = f"{x:,.{decimals}f}"
    return s.replace(",", "\u0001").replace(".", ",").replace("\u0001", ".")


def find_csv() -> Path:
    files = sorted(BENCH_DIR.glob("model_throughput_*.csv"))
    if not files:
        raise SystemExit(f"Không tìm thấy tệp model_throughput_*.csv trong {BENCH_DIR}")
    return files[-1]


def plot(df: pd.DataFrame, out_png: Path) -> None:
    # Cùng một thứ tự cho cả hai khung: độ chính xác giảm dần, đọc từ trên xuống.
    df = df.sort_values("accuracy", ascending=False).reset_index(drop=True)
    names = [DISPLAY.get(n, n) for n in df["pair_name"]]
    n = len(df)
    ypos = list(range(n - 1, -1, -1))  # hàng đầu tiên nằm trên cùng

    fig, (ax_a, ax_b) = plt.subplots(
        1, 2, figsize=(12.6, 4.8), gridspec_kw={"width_ratios": [1.75, 1.0]}
    )

    # ---------------------------------------------------------------- khung (a)
    bar_h = 0.19
    offsets = [1.5, 0.5, -0.5, -1.5]  # trung vị nằm trên cùng trong mỗi nhóm
    for (col, label), color, off in zip(STATS, RAMP, offsets):
        vals = df[col].to_numpy()
        ys = [y + off * bar_h for y in ypos]
        ax_a.barh(ys, vals, height=bar_h, color=color, label=label, zorder=3)
        for y, v in zip(ys, vals):
            ax_a.text(v + 40, y, _vn(v), va="center", ha="left",
                      fontsize=8, color=TEXT, zorder=4)

    ax_a.set_yticks(ypos)
    ax_a.set_yticklabels(names, fontsize=9.5, color=TEXT)
    ax_a.set_xlabel("Thời gian xử lý một ảnh (ms)", fontsize=10, color=TEXT)
    ax_a.set_title("(a) Độ trễ đầu-cuối trên 291 ảnh kiểm tra",
                   fontsize=11.5, color=TEXT, pad=12, loc="left")
    ax_a.set_xlim(0, float(df[[c for c, _ in STATS]].to_numpy().max()) * 1.18)
    ax_a.legend(title="Thống kê", fontsize=9, title_fontsize=9,
                loc="lower right", frameon=False)
    ax_a.xaxis.set_major_formatter(FuncFormatter(lambda v, _: _vn(v)))
    ax_a.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax_a.set_axisbelow(True)

    # ---------------------------------------------------------------- khung (b)
    acc = (df["accuracy"] * 100).to_numpy()
    colors = [ACCENT if pn == PROPOSED else MUTED for pn in df["pair_name"]]
    lo, hi = acc.min(), acc.max()
    pad = max(0.35, (hi - lo) * 0.45)
    x0, x1 = lo - pad, hi + pad

    for y, v, c in zip(ypos, acc, colors):
        ax_b.hlines(y, x0, v, color=c, linewidth=1.2, alpha=0.45, zorder=2)
        ax_b.plot([v], [y], "o", markersize=10, color=c, zorder=3)
        ax_b.text(v, y + 0.26, _vn(v, 2) + "%", ha="center", va="bottom",
                  fontsize=9.5, color=c, fontweight="bold", zorder=4)

    ax_b.set_yticks(ypos)
    ax_b.set_yticklabels([])
    ax_b.set_xlim(x0, x1)
    ax_b.set_ylim(-0.6, n - 0.35)
    ax_b.set_xlabel("Độ chính xác mức ảnh (%)", fontsize=10, color=TEXT)
    ax_b.set_title("(b) Độ chính xác tương ứng",
                   fontsize=11.5, color=TEXT, pad=12, loc="left")
    ax_b.xaxis.set_major_formatter(FuncFormatter(lambda v, _: _vn(v, 1)))
    ax_b.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax_b.set_axisbelow(True)
    ax_b.annotate("Cấu hình đề xuất", xy=(acc[0], ypos[0]),
                  xytext=(-14, -20), textcoords="offset points",
                  fontsize=9, color=ACCENT, ha="right",
                  arrowprops=dict(arrowstyle="-", color=ACCENT, linewidth=0.9))

    for ax in (ax_a, ax_b):
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(axis="both", length=0, labelsize=9, colors=TEXT)

    fig.tight_layout(w_pad=2.0)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=200, facecolor="white")
    plt.close(fig)


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="vẽ lại kể cả khi PNG đã tồn tại")
    args = ap.parse_args()

    if OUT_PNG.exists() and not args.force:
        print(f"Đã có sẵn, bỏ qua (dùng --force để vẽ lại): {OUT_PNG}")
        return

    csv_path = find_csv()
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    plot(df, OUT_PNG)
    print(f"Nguồn : {csv_path}")
    print(f"Đã lưu: {OUT_PNG}")


if __name__ == "__main__":
    main()
