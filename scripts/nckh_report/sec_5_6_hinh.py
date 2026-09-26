"""Hình so sánh thông lượng cho mục 5.6.

Tách riêng theo cùng khuôn mẫu với sec_5_1_5.py: báo cáo đầy đủ và bản trích xuất
rời cùng gọi build() nên nội dung không bao giờ lệch nhau.

Module này KHÔNG tự chạy build() khi import.
"""
from __future__ import annotations

from .core import figure, p


def build() -> None:
    p("Hình dưới đây trực quan hóa số liệu của bảng trên. Khung (a) đặt cạnh nhau bốn thống kê "
      "độ trễ của từng cấu hình; khung (b) hiển thị độ chính xác tương ứng trên thang phóng đại, "
      "vì bốn giá trị chỉ chênh nhau chưa tới một điểm rưỡi phần trăm.")

    figure("outputs/Performance_Benchmark/throughput_comparison.png",
           "So sánh độ trễ và độ chính xác của bốn cấu hình xếp tầng trên 291 ảnh kiểm tra. "
           "(a) Thời gian xử lý một ảnh theo bốn thống kê trung vị, trung bình, P90 và P95; "
           "(b) Độ chính xác mức ảnh tương ứng, trục hoành được phóng đại để thấy rõ chênh lệch",
           width=15.5)

    p("Cách đặt hai khung cạnh nhau làm lộ rõ sự đánh đổi của đề tài. Cấu hình đề xuất nằm ở "
      "hàng trên cùng của cả hai khung: dẫn đầu về độ chính xác với 94,85% nhưng cũng là cấu "
      "hình có dải độ trễ rộng nhất. Ba cấu hình tham chiếu có thời gian trung vị xấp xỉ nhau "
      "trong khoảng 194 đến 212 ms, trong khi cấu hình đề xuất cần 684 ms, tức gấp khoảng ba "
      "lần rưỡi. Đáng chú ý là khoảng cách này thu hẹp đáng kể ở đuôi phân phối: tại mức P95, "
      "tỷ lệ chỉ còn khoảng một phẩy năm lần so với cấu hình chậm nhất trong nhóm tham chiếu. "
      "Điều đó xác nhận nhận định ở trên rằng chi phí thời gian chủ yếu đến từ số vùng quan tâm "
      "phải xử lý chứ không phải từ bản thân kiến trúc bộ phân loại.")
