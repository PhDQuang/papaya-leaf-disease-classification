"""CHƯƠNG 4. DỮ LIỆU VÀ THIẾT KẾ THỰC NGHIỆM."""
from __future__ import annotations

from .core import bullet, figure, h, h_center, new_page, note, p, table


def build() -> None:
    h_center("CHƯƠNG 4. DỮ LIỆU VÀ THIẾT KẾ THỰC NGHIỆM", 1)

    # ------------------------------------------------------------------ 4.1
    h("4.1. Bộ dữ liệu BDPapayaLeaf", 2)
    p("Đề tài sử dụng bộ dữ liệu thứ cấp BDPapayaLeaf phiên bản V2 do Sarker và cộng sự công bố "
      "năm 2024 trên kho dữ liệu mở Mendeley Data. Việc lựa chọn một bộ dữ liệu đã công bố thay "
      "vì tự thu thập xuất phát từ ba cân nhắc. Thứ nhất, bộ dữ liệu này đã được cộng đồng khoa "
      "học sử dụng và đối chứng, cho phép so sánh trực tiếp kết quả của đề tài với các công "
      "trình khác. Thứ hai, việc gán nhãn bệnh cây đòi hỏi chuyên môn bảo vệ thực vật mà nhóm "
      "nghiên cứu không có; sử dụng nhãn đã được chuyên gia xác nhận bảo đảm chất lượng nhãn. "
      "Thứ ba, quy mô và tính đa dạng của bộ dữ liệu vượt xa khả năng thu thập trong thời gian "
      "mười hai tháng của đề tài.")
    p("Bộ dữ liệu được thu thập ngoài đồng ruộng tại Bangladesh, bao gồm ảnh lá đu đủ chụp ở "
      "nhiều điều kiện ánh sáng, góc chụp và phông nền khác nhau. Đây là đặc điểm quan trọng: "
      "mô hình huấn luyện trên dữ liệu thực địa có khả năng tổng quát hóa tốt hơn so với mô hình "
      "huấn luyện trên ảnh chụp trong phòng thí nghiệm với nền đồng nhất.")

    # ------------------------------------------------------------------ 4.2
    h("4.2. Chuẩn bị dữ liệu cho giai đoạn phát hiện", 2)
    p("Dữ liệu cho bộ phát hiện được tổ chức theo định dạng YOLO, trong đó mỗi ảnh đi kèm một "
      "tệp nhãn văn bản chứa các dòng gồm chỉ số lớp và tọa độ khung chuẩn hóa. Tập dữ liệu được "
      "chia theo tỷ lệ xấp xỉ 70% huấn luyện, 15% xác thực và 15% kiểm tra.")

    table("Phân chia dữ liệu cho giai đoạn phát hiện đối tượng",
          ["Tập dữ liệu", "Số ảnh", "Tỷ lệ", "Vai trò"],
          [
              ["Huấn luyện (train)", "1.194", "70,0%", "Cập nhật trọng số mô hình"],
              ["Xác thực (val)", "256", "15,0%", "Chọn điểm dừng và siêu tham số"],
              ["Kiểm tra (test)", "257", "15,0%", "Đánh giá cuối cùng, không dùng trong huấn luyện"],
              ["Tổng cộng", "1.707", "100%", "—"],
          ],
          widths=[4.6, 3.0, 2.6, 5.8])

    p("Trước khi huấn luyện, một bước kiểm tra tính toàn vẹn dữ liệu được thực hiện và ghi lại "
      "trong tệp dataset_split_sanity.csv. Kết quả xác nhận không có ảnh nào thiếu tệp nhãn "
      "tương ứng và không có tệp nhãn mồ côi nào không có ảnh đi kèm, trên cả ba tập. Đây là "
      "bước kiểm soát chất lượng cần thiết, bởi một cặp ảnh–nhãn lệch nhau có thể làm sai lệch "
      "toàn bộ quá trình huấn luyện mà không phát sinh lỗi rõ ràng.")

    figure("outputs/yolo/yolov11_m/labels.jpg",
           "Thống kê phân bố nhãn của tập huấn luyện giai đoạn phát hiện: số lượng thực thể theo "
           "lớp, phân bố tọa độ tâm và phân bố kích thước khung bao", width=14.0)

    p("Biểu đồ phân bố nhãn cho thấy hai đặc điểm đáng chú ý. Một là sự chênh lệch lớn về số "
      "lượng thực thể giữa các lớp, phản ánh bản chất của bệnh: một lá thán thư có thể mang hàng "
      "chục đốm trong khi một lá xoăn chỉ có một vùng biến dạng duy nhất. Hai là phần lớn khung "
      "bao có kích thước rất nhỏ so với ảnh, khẳng định lại nhận định ở Chương 1 về thách thức "
      "phát hiện đối tượng nhỏ.")

    figure("outputs/yolo/yolov11_m/train_batch0.jpg",
           "Một lô ảnh huấn luyện của YOLOv11m sau khi áp dụng tăng cường dữ liệu mosaic, kèm "
           "khung bao và nhãn lớp", width=14.2)

    # ------------------------------------------------------------------ 4.3
    h("4.3. Chuẩn bị dữ liệu cho giai đoạn phân loại", 2)
    p("Dữ liệu cho bộ phân loại được sinh ra bằng cách cắt các vùng quan tâm từ ảnh gốc theo "
      "khung bao thực tế đã gán nhãn, kết hợp với các vùng lá khỏe mạnh lấy từ ảnh thuộc lớp "
      "Healthy. Nhờ vậy, mỗi ảnh gốc sinh ra nhiều mẫu huấn luyện, làm tăng đáng kể quy mô dữ "
      "liệu cho giai đoạn hai.")

    table("Phân bố số lượng vùng quan tâm theo lớp và theo tập dữ liệu",
          ["Lớp", "Huấn luyện", "Xác thực", "Kiểm tra", "Tổng"],
          [
              ["Anthracnose", "4.416", "1.046", "1.040", "6.502"],
              ["BacterialSpot", "320", "69", "69", "458"],
              ["Curl", "254", "54", "54", "362"],
              ["Healthy", "160", "34", "34", "228"],
              ["RingSpot", "2.412", "510", "639", "3.561"],
              ["Tổng cộng", "7.562", "1.713", "1.836", "11.111"],
          ],
          widths=[4.0, 3.0, 3.0, 3.0, 3.0])

    p("Bảng trên cho thấy mức độ mất cân bằng nghiêm trọng: tỷ lệ giữa lớp đông nhất "
      "(Anthracnose, 4.416 mẫu huấn luyện) và lớp hiếm nhất (Healthy, 160 mẫu huấn luyện) là "
      "27,6 lần. Nếu không xử lý, mô hình có thể đạt độ chính xác tổng thể cao bằng cách gần như "
      "luôn dự đoán Anthracnose, trong khi hoàn toàn thất bại trên các lớp hiếm.")

    h("4.3.1. Trọng số lớp", 3)
    p("Trọng số lớp được tính theo công thức (2.3) với N_total = 7.562 và C = 5. Giá trị cụ thể "
      "được trình bày trong bảng dưới đây.")

    table("Trọng số lớp áp dụng cho hàm mất mát của bộ phân loại",
          ["Lớp", "Số mẫu huấn luyện N_c", "Trọng số w_c = 7562 / (5 × N_c)", "Diễn giải"],
          [
              ["Anthracnose", "4.416", "0,343", "Giảm ảnh hưởng của lớp đa số"],
              ["BacterialSpot", "320", "4,726", "Khuếch đại gần 5 lần"],
              ["Curl", "254", "5,954", "Khuếch đại gần 6 lần"],
              ["Healthy", "160", "9,453", "Khuếch đại mạnh nhất, hơn 9 lần"],
              ["RingSpot", "2.412", "0,627", "Giảm nhẹ"],
          ],
          widths=[3.4, 4.0, 5.2, 4.4])

    p("Chênh lệch giữa trọng số lớn nhất và nhỏ nhất lên tới 27,6 lần, đúng bằng tỷ lệ mất cân "
      "bằng ban đầu. Điều này có nghĩa là trong hàm mất mát, một mẫu Healthy bị phân loại sai "
      "gây thiệt hại tương đương hai mươi tám mẫu Anthracnose bị phân loại sai, buộc mô hình "
      "phải học nghiêm túc cả các lớp hiếm.")

    # ------------------------------------------------------------------ 4.4
    h("4.4. Dữ liệu đánh giá hệ thống ở mức ảnh", 2)
    p("Việc đánh giá toàn hệ thống được thực hiện ở mức ảnh, không phải mức vùng, vì đây mới là "
      "đơn vị mà người dùng cuối quan tâm: họ chụp một bức ảnh lá và mong nhận về một chẩn đoán. "
      "Tập đánh giá gồm 291 ảnh, được hợp thành từ 257 ảnh của tập kiểm tra giai đoạn phát hiện "
      "và 34 ảnh lá khỏe mạnh lấy từ tập kiểm tra giai đoạn phân loại.")

    table("Phân bố tập đánh giá hệ thống ở mức ảnh",
          ["Lớp", "Số ảnh", "Tỷ lệ", "Nguồn"],
          [
              ["Anthracnose", "54", "18,6%", "Tập kiểm tra giai đoạn phát hiện"],
              ["BacterialSpot", "69", "23,7%", "Tập kiểm tra giai đoạn phát hiện"],
              ["Curl", "54", "18,6%", "Tập kiểm tra giai đoạn phát hiện"],
              ["Healthy", "34", "11,7%", "Tập kiểm tra giai đoạn phân loại"],
              ["RingSpot", "80", "27,5%", "Tập kiểm tra giai đoạn phát hiện"],
              ["Tổng cộng", "291", "100%", "—"],
          ],
          widths=[3.6, 2.6, 2.6, 7.2])

    p("Cần nhấn mạnh rằng toàn bộ 291 ảnh này chưa từng xuất hiện trong bất kỳ giai đoạn huấn "
      "luyện nào, kể cả dưới dạng vùng cắt. Đây là điều kiện bắt buộc để kết quả đánh giá phản "
      "ánh trung thực năng lực tổng quát hóa của hệ thống.")

    # ------------------------------------------------------------------ 4.5
    h("4.5. Thiết kế các thực nghiệm", 2)
    p("Đề tài thiết kế bốn nhóm thực nghiệm nhằm trả lời bốn câu hỏi nghiên cứu độc lập.")

    table("Thiết kế thực nghiệm và câu hỏi nghiên cứu tương ứng",
          ["Nhóm", "Câu hỏi nghiên cứu", "Cấu hình khảo sát", "Chỉ số chính"],
          [
              ["TN1", "Biến thể YOLOv11 nào phù hợp nhất cho giai đoạn phát hiện?",
               "YOLOv11n, YOLOv11s, YOLOv11m", "mAP@0,5; mAP@0,5:0,95; thời gian suy luận"],
              ["TN2", "Biến thể EfficientNet nào phù hợp nhất cho giai đoạn phân loại?",
               "EfficientNet-B0, B1, B2", "Accuracy; macro F1 trên 1.836 vùng kiểm tra"],
              ["TN3", "Tổ hợp xếp tầng nào cho kết quả tốt nhất ở mức ảnh?",
               "9 tổ hợp {n, s, m} × {B0, B1, B2}", "Accuracy; macro F1 trên 291 ảnh"],
              ["TN4", "Kiến trúc xếp tầng có thực sự tốt hơn phân loại toàn ảnh và các kiến trúc "
                      "tham chiếu hay không?",
               "YOLOv11m × {VGG16, ResNet50, DenseNet121}; EfficientNet-B2 toàn ảnh",
               "Accuracy; macro F1; thời gian suy luận"],
          ],
          widths=[1.8, 5.2, 4.6, 4.4], font_size=10.5)

    p("Ngoài bốn nhóm trên, một thực nghiệm bổ sung đo thông lượng của bốn cấu hình xếp tầng "
      "trên cùng phần cứng nhằm đánh giá tính khả thi triển khai thực tế.")

    # ------------------------------------------------------------------ 4.6
    h("4.6. Môi trường thực nghiệm và quy trình tái lập", 2)
    p("Toàn bộ quá trình huấn luyện được thực hiện trên nền tảng Google Colab với GPU. Quá trình "
      "suy luận và đo thông lượng được thực hiện trên môi trường thống nhất để bảo đảm các con "
      "số thời gian có thể so sánh với nhau.")

    table("Cấu hình phần mềm của môi trường thực nghiệm",
          ["Thành phần", "Công cụ / thư viện", "Vai trò"],
          [
              ["Ngôn ngữ", "Python 3", "Nền tảng triển khai toàn bộ mã nguồn"],
              ["Phát hiện đối tượng", "Ultralytics YOLO, PyTorch", "Huấn luyện và suy luận YOLOv11"],
              ["Phân loại ảnh", "TensorFlow / Keras", "Huấn luyện và suy luận EfficientNet"],
              ["Xử lý ảnh", "OpenCV, Pillow, NumPy", "Đọc ảnh, cắt vùng, biến đổi hình học"],
              ["Đánh giá", "scikit-learn, pandas, Matplotlib", "Tính chỉ số, vẽ ma trận nhầm lẫn"],
              ["Dịch vụ", "FastAPI, Uvicorn", "Cung cấp API suy luận dạng REST"],
              ["Giao diện", "Gradio", "Giao diện web cho người dùng cuối"],
              ["Đóng gói", "Docker, Docker Compose", "Container hóa và điều phối dịch vụ"],
              ["Hạ tầng", "Terraform", "Mô tả hạ tầng triển khai dưới dạng mã"],
          ],
          widths=[3.6, 5.2, 7.2], font_size=10.5)

    p("Khả năng tái lập được bảo đảm bằng bốn biện pháp: cố định hạt giống ngẫu nhiên bằng 42 "
      "cho cả hai giai đoạn; bật chế độ tất định trong Ultralytics; lưu trữ toàn bộ cấu hình "
      "huấn luyện dưới dạng tệp args.yaml đi kèm mỗi lần chạy; và ghi lại lịch sử huấn luyện "
      "từng epoch dưới dạng tệp CSV. Mọi số liệu trình bày trong Chương 5 đều được trích xuất "
      "trực tiếp từ các tệp kết quả này, danh mục đầy đủ được liệt kê trong Phụ lục C.")

    # ------------------------------------------------------------------ 4.7
    h("4.7. Quy trình thực nghiệm tổng thể", 2)
    p("Các bước thực nghiệm được tổ chức thành chuỗi sổ tay Jupyter chạy tuần tự, mỗi sổ tay đảm "
      "nhiệm một khâu và ghi kết quả ra thư mục outputs để khâu sau sử dụng lại.")
    for line in [
        "Sổ tay 01 — Chuẩn bị dữ liệu: tải bộ dữ liệu, kiểm tra tính toàn vẹn, chia tập, sinh "
        "vùng quan tâm cho giai đoạn phân loại.",
        "Sổ tay 02 — Huấn luyện bộ phát hiện: huấn luyện ba biến thể YOLOv11 và đánh giá trên tập "
        "kiểm tra.",
        "Sổ tay 03, 04, 05 — Huấn luyện bộ phân loại: lần lượt cho EfficientNet-B0, B1 và B2 theo "
        "chiến lược hai pha.",
        "Sổ tay 06 — Đánh giá xếp tầng: ghép mọi tổ hợp bộ phát hiện và bộ phân loại, đánh giá "
        "trên 291 ảnh mức ảnh.",
        "Sổ tay 07 — Đo thông lượng: đo thời gian suy luận đầu-cuối của bốn cấu hình trên cùng "
        "phần cứng.",
        "Sổ tay 08 — Xuất mô hình cho Android: chuyển đổi mô hình sang định dạng phù hợp triển "
        "khai trên thiết bị di động.",
        "Thư mục baselines — Huấn luyện các kiến trúc tham chiếu VGG16, ResNet50, DenseNet121 và "
        "đường cơ sở phân loại toàn ảnh.",
    ]:
        bullet(line)

    p("Cách tổ chức này bảo đảm mọi kết quả đều truy vết được tới mã nguồn sinh ra nó, và cho "
      "phép chạy lại từng khâu độc lập khi cần kiểm chứng.")

    new_page()


build()
