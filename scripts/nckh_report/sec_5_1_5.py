"""Mục 5.1.5 – Diễn biến quá trình huấn luyện YOLOv11m.

Tách riêng khỏi s07_ch5.py để có thể xuất thành tệp .docx độc lập (chỉ chứa hình và
phần phân tích kèm theo) mà không phải chép lại nội dung, tránh hai bản bị lệch nhau.

Khác với các module s0*.py, module này KHÔNG tự chạy build() khi import.
"""
from __future__ import annotations

from .core import figure, h, p


def build(with_heading: bool = True) -> None:
    if with_heading:
        h("5.1.5. Diễn biến quá trình huấn luyện", 3)

    p("Để kiểm chứng rằng bộ phát hiện hội tụ lành mạnh chứ không phải khớp quá mức, đề tài "
      "theo dõi mười đại lượng qua từng vòng lặp huấn luyện. Toàn bộ số liệu được ghi vào tệp "
      "outputs/yolo/yolov11_m/results.csv và trực quan hóa ở hình dưới đây.")

    figure("outputs/yolo/yolov11_m/results.png",
           "Đường cong huấn luyện của YOLOv11m qua 80 vòng lặp. Hàng trên: ba thành phần mất mát "
           "trên tập huấn luyện cùng Precision và Recall; hàng dưới: ba thành phần mất mát trên "
           "tập xác thực cùng mAP@0,5 và mAP@0,5:0,95. Đường liền nối các giá trị thực đo, đường "
           "chấm là kết quả làm trơn bằng bộ lọc Gauss",
           width=15.5)

    p("Ba đường cong mất mát trên tập huấn luyện đều giảm đơn điệu trong suốt 80 vòng lặp: "
      "box_loss từ 1,363 xuống 0,794, cls_loss từ 2,031 xuống 0,641 và dfl_loss từ 1,337 xuống "
      "0,978. Điều đáng chú ý hơn là ba đường cong tương ứng trên tập xác thực cũng giảm theo "
      "cùng xu hướng, chứ không đi ngang rồi bật lên như trong hiện tượng khớp quá mức: "
      "val/box_loss kết thúc ở 0,814 và val/cls_loss ở 0,785. Khoảng cách giữa mất mát huấn "
      "luyện và mất mát xác thực giữ ở mức hẹp và ổn định, cho thấy mô hình vẫn còn khả năng "
      "khái quát hóa tại thời điểm dừng.")
    p("Cụm giá trị bất thường ở những vòng lặp đầu tiên là một chi tiết cần giải thích. "
      "val/cls_loss vọt lên 4,232 tại vòng thứ ba trước khi rơi nhanh xuống dưới 1,0 từ vòng "
      "thứ hai mươi. Đây là biểu hiện quen thuộc của giai đoạn khởi động tốc độ học: trong ba "
      "vòng đầu, tốc độ học tăng tuyến tính từ 0 lên giá trị đỉnh nên trọng số bị cập nhật "
      "mạnh, khiến đầu phân loại tạm thời mất ổn định. Hiện tượng này tự triệt tiêu sau khi "
      "lịch trình tốc độ học chuyển sang pha suy giảm, và không để lại dấu vết nào trên các "
      "chỉ số cuối cùng.")
    p("Về tốc độ hội tụ, mAP@0,5 tăng rất nhanh trong hai mươi vòng đầu, từ 0,5498 lên 0,7673, "
      "tức là đạt khoảng 95% giá trị cuối cùng chỉ sau một phần tư số vòng lặp. Từ vòng thứ ba "
      "mươi trở đi, đường cong đi vào vùng bão hòa và dao động quanh mốc 0,80; riêng hai mươi "
      "vòng cuối chỉ mang lại thêm 0,0108 điểm mAP@0,5. Chỉ số mAP@0,5:0,95 khắt khe hơn nên "
      "tiến triển chậm hơn, tăng từ 0,3432 lên 0,6816 và đạt đỉnh 0,6819 tại vòng thứ 69.")
    p("Quan sát này có hai hệ quả thực tiễn. Thứ nhất, ngân sách 80 vòng lặp là đủ và hợp lý: "
      "kéo dài thêm nhiều khả năng chỉ làm tăng chi phí tính toán mà không cải thiện đáng kể "
      "chất lượng, trong khi toàn bộ phiên huấn luyện đã tiêu tốn 2,12 giờ trên GPU. Thứ hai, "
      "vì các đường cong xác thực chưa có dấu hiệu đi lên, điểm nghẽn hiệu năng của giai đoạn "
      "phát hiện nằm ở độ khó nội tại của hai lớp đốm dày đặc đã phân tích ở mục 5.1.2, chứ "
      "không nằm ở việc huấn luyện thiếu hay thừa.")
