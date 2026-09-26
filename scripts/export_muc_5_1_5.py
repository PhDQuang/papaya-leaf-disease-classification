"""Xuất riêng mục 5.1.5 (hình đường cong huấn luyện YOLOv11m) ra một tệp .docx rời.

Dùng khi báo cáo chính đang được chỉnh tay và không thể sinh lại toàn bộ: mở tệp rời
này, bôi đen toàn bộ rồi dán vào đúng vị trí trong báo cáo. Vì tệp rời dùng chung bộ
style với báo cáo chính (Times New Roman 13pt, giãn dòng 1,4, lề 3-2-2-2), định dạng
được giữ nguyên sau khi dán.

Số hiệu hình trong tệp rời sẽ hiển thị là "Hình 1" vì đây là hình đầu tiên của tệp.
Đó là trường SEQ của Word, nên sau khi dán vào báo cáo chỉ cần bấm Ctrl+A rồi F9 là
Word tự đánh lại đúng số thứ tự.

Cách dùng:
    python scripts/export_muc_5_1_5.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.nckh_report import core, sec_5_1_5  # noqa: E402

OUT = core.ROOT / "NghienCuuKhoaHoc" / "Muc_5_1_5_DuongCongHuanLuyen_YOLOv11m.docx"


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    sec_5_1_5.build()
    core.save(OUT)

    print(f"Đã xuất: {OUT}")
    print(f"Ảnh gốc: {core.ROOT / 'outputs' / 'yolo' / 'yolov11_m' / 'results.png'}")
    if core.missing_assets:
        print("Cảnh báo:")
        for item in core.missing_assets:
            print(f"  - {item}")


if __name__ == "__main__":
    main()
