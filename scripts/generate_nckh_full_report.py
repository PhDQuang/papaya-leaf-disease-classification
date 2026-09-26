"""Build the full SV2026-08 university research summary report (Báo cáo tổng kết).

Usage:
    python scripts/generate_nckh_full_report.py

Every section module builds its part of the shared document at import time, so the
import order below is the order of the report.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.nckh_report import core  # noqa: E402
from scripts.nckh_report import s01_front  # noqa: F401,E402
from scripts.nckh_report import s02_mo_dau  # noqa: F401,E402
from scripts.nckh_report import s03_ch1  # noqa: F401,E402
from scripts.nckh_report import s04_ch2  # noqa: F401,E402
from scripts.nckh_report import s05_ch3  # noqa: F401,E402
from scripts.nckh_report import s06_ch4  # noqa: F401,E402
from scripts.nckh_report import s07_ch5  # noqa: F401,E402
from scripts.nckh_report import s08_ch6  # noqa: F401,E402
from scripts.nckh_report import s09_ket_luan  # noqa: F401,E402


def main() -> None:
    # Console Windows mặc định là cp1252, không in được tiếng Việt có dấu.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    out = core.save()
    print(f"Saved : {out}")
    print(f"Figures: {core.fig_count()}")
    print(f"Tables : {core.tab_count()}")
    print(f"Missing / TODO markers: {len(core.missing_assets)}")
    for i, item in enumerate(core.missing_assets, 1):
        print(f"  {i:2d}. {item[:110]}")


if __name__ == "__main__":
    main()
