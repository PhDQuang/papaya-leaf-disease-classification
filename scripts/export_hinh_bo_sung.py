"""Xuất các hình bổ sung cho báo cáo SV2026-08 ra một tệp .docx rời.

Dùng khi BaoCaoTongKet_SV2026-08_FULL.docx đang được chỉnh tay: mở tệp rời này, chép
từng phần sang đúng vị trí trong báo cáo. Tệp rời dùng chung bộ style với báo cáo
chính (Times New Roman 13pt, giãn dòng 1,4, lề 3-2-2-2) nên định dạng giữ nguyên sau
khi dán. Số hiệu hình là trường SEQ của Word, dán xong bấm Ctrl+A rồi F9 để Word đánh
lại đúng thứ tự.

Tệp gồm hai phần:
  Phần A – các hình đã sinh được, dán thẳng vào báo cáo.
  Phần B – bảng hướng dẫn cho những hình chỉ tạo được bằng tay hoặc trên Colab.

Cách dùng:
    python scripts/plot_throughput_comparison.py --force   # sinh ảnh trước
    python scripts/export_hinh_bo_sung.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.nckh_report import core, sec_5_6_hinh  # noqa: E402
from scripts.nckh_report.core import (  # noqa: E402
    bullet, centered, h, p, new_page, table,
)

OUT = core.ROOT / "NghienCuuKhoaHoc" / "Hinh_BoSung_SV2026-08.docx"


def _intro() -> None:
    centered("HÌNH BỔ SUNG CHO BÁO CÁO TỔNG KẾT SV2026-08", size=15, bold=True, after=6)
    centered("Tệp phụ trợ – không nộp kèm, chỉ dùng để chép nội dung sang báo cáo chính",
             size=12, italic=True, after=16)

    p("Tệp này được sinh tự động nhằm bổ sung những hình còn thiếu trong báo cáo tổng kết. "
      "Phần A chứa các hình đã dựng xong, có thể bôi đen và dán thẳng vào báo cáo. Phần B "
      "liệt kê những hình không thể sinh trên máy cục bộ kèm hướng dẫn tạo.")
    p("Lưu ý khi dán: sau khi dán xong toàn bộ, bấm Ctrl+A rồi F9 trong báo cáo chính để Word "
      "đánh lại số hiệu hình, số hiệu bảng và mục lục cho đúng thứ tự.")


def _phan_a() -> None:
    h("PHẦN A. CÁC HÌNH ĐÃ DỰNG SẴN", 1)

    h("A.1. Hình cho mục 5.6 – So sánh độ trễ và độ chính xác", 2)
    p("Dán toàn bộ khối dưới đây (gồm đoạn dẫn, hình và đoạn phân tích) vào ngay sau bảng "
      "thời gian suy luận ở mục 5.6, thay cho đoạn ghi chú [CẦN BỔ SUNG] hiện có.",
      italic=True)
    p()
    sec_5_6_hinh.build()


def _phan_b() -> None:
    new_page()
    h("PHẦN B. CÁC HÌNH CẦN TỰ TẠO", 1)
    p("Bốn hình dưới đây phụ thuộc vào dữ liệu hoặc môi trường không có trên máy cục bộ, "
      "nên phải tạo theo hướng dẫn tương ứng.")

    h("B.1. Ảnh chú thích mười lăm ca sai (mục 5.5.2)", 2)
    p("Hai ảnh đang dùng ở mục 5.5.2 lấy từ cấu hình tham chiếu YOLOv11m + ResNet50, không "
      "khớp với phần phân tích vốn nói về cấu hình đề xuất. Notebook "
      "notebooks/09_export_annotated_error_cases_colab.ipynb sinh lại đúng mười lăm ca sai "
      "của cấu hình đề xuất.")
    bullet("Notebook không nạp lại mô hình. Tệp error_cases.csv đã lưu sẵn toạ độ từng khung, "
           "lớp và độ tin cậy mà YOLO gán cho khung, lớp và độ tin cậy mà EfficientNet-B2 gán "
           "cho vùng cắt, nên chỉ cần vẽ lại. Chạy khoảng một phút, không cần GPU.")
    bullet("Phải chạy trên Colab vì 291 ảnh kiểm tra gốc nằm trên Google Drive chứ không có "
           "trong repo.")
    bullet("Kết quả gồm mười lăm ảnh ca01–ca15, hai ảnh đặt tên hinh_5_5_2_1 và hinh_5_5_2_2 "
           "dùng thay trực tiếp cho hai ảnh hiện tại, và một bảng ảnh lưới ba nhân năm gộp cả "
           "mười lăm ca để đưa vào phụ lục.")
    bullet("Hai ca được chọn cho hình 5.5.2 đúng bằng hai ca mà chú thích hình hiện tại đang "
           "mô tả (Healthy bị dự đoán BacterialSpot, BacterialSpot bị dự đoán Curl), nên phần "
           "lời văn và chú thích trong báo cáo giữ nguyên, không phải sửa.")

    h("B.2. Ảnh chụp màn hình dịch vụ và giao diện", 2)
    p("Ba mục còn lại đều là ảnh chụp màn hình, phải tự chụp vì máy hiện không cài "
      "ultralytics và không chạy được Docker.")

    table("Hướng dẫn tạo ba ảnh chụp màn hình còn thiếu",
          ["Mục trong báo cáo", "Cần có", "Cách tạo"],
          [
              ["6.x – Kết quả trả về của API",
               "Một khối JSON thật do API trả về",
               "Khởi động dịch vụ, gửi một ảnh lá bệnh lên điểm cuối dự đoán, chép nguyên văn "
               "phần JSON trả về vào báo cáo dưới dạng khối mã."],
              ["6.x – Giao diện web",
               "Ảnh chụp màn hình giao diện tại http://localhost:7860",
               "Chạy dịch vụ web, tải lên một ảnh lá bệnh, chờ hiển thị kết quả rồi chụp toàn "
               "bộ cửa sổ trình duyệt ở độ phân giải tối thiểu 1600 điểm ảnh chiều ngang."],
              ["6.x – Tài liệu API",
               "Ảnh chụp trang tài liệu tự sinh tại http://localhost:8000/docs",
               "Mở trang tài liệu, mở rộng điểm cuối dự đoán để thấy rõ tham số đầu vào và "
               "cấu trúc phản hồi, rồi chụp màn hình."],
          ],
          widths=[4.2, 4.6, 7.2], font_size=10.5)

    p("Khi chèn ảnh chụp màn hình, đặt bề ngang 15,5 cm cho ảnh toàn cửa sổ và 12 cm cho ảnh "
      "chỉ chụp một phần, kèm chú thích đặt dưới ảnh theo đúng khuôn mẫu của các hình khác "
      "trong báo cáo.")


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    _intro()
    _phan_a()
    _phan_b()
    core.save(OUT)

    print(f"Đã xuất: {OUT}")
    if core.missing_assets:
        print("Cảnh báo – thiếu tệp ảnh:")
        for item in core.missing_assets:
            print(f"  - {item}")


if __name__ == "__main__":
    main()
