"""MỞ ĐẦU: tổng quan tình hình nghiên cứu, lý do, mục tiêu, phương pháp, phạm vi, bố cục."""
from __future__ import annotations

from .core import bullet, h, h_center, new_page, p, table


def build() -> None:
    h_center("MỞ ĐẦU", 1)

    # ------------------------------------------------ 1. Tổng quan tình hình
    h("1. Tổng quan tình hình nghiên cứu thuộc lĩnh vực của đề tài", 2)
    p("Chẩn đoán bệnh cây trồng bằng hình ảnh là một trong những hướng ứng dụng thành công nhất "
      "của thị giác máy tính trong nông nghiệp. Trong hơn một thập kỷ qua, hướng nghiên cứu này "
      "đã dịch chuyển từ các phương pháp trích xuất đặc trưng thủ công kết hợp bộ phân lớp cổ "
      "điển sang các mô hình học sâu đầu-cuối, và gần đây là các kiến trúc lai ghép nhiều mô-đun "
      "chuyên biệt. Phần này tổng hợp các công trình tiêu biểu trong nước và ngoài nước làm cơ sở "
      "xác định khoảng trống nghiên cứu mà đề tài hướng tới.")

    h("1.1. Tình hình nghiên cứu trong nước", 3)
    p("Nguyễn Minh Triết và cộng sự (2017) đã xây dựng hệ thống nhận dạng bệnh trên lá bưởi bằng "
      "cách trích xuất đặc trưng màu sắc, kết cấu và hình dạng rồi phân lớp bằng máy vec-tơ hỗ "
      "trợ. Nhóm tác giả báo cáo độ chính xác khoảng 99,5% trên tập huấn luyện và xấp xỉ 99,2% "
      "khi kiểm tra trên 500 ảnh thực tế. Kết quả cho thấy tiềm năng của hướng tiếp cận truyền "
      "thống trong điều kiện ảnh được chuẩn hóa tốt, song hệ thống phụ thuộc mạnh vào khâu phân "
      "đoạn thủ công và khó mở rộng cho nhiều loại bệnh có biểu hiện gần giống nhau.")
    p("Nguyễn Đức Tấn và Thái Thuận Thương (2025) so sánh EfficientNetB0 và MobileNetV2 trên bài "
      "toán nhận dạng 41 loài cây thuốc; EfficientNetB0 đạt khoảng 94% trong khi MobileNetV2 chỉ "
      "đạt khoảng 90%. Công trình này củng cố nhận định rằng họ EfficientNet cho tỷ lệ chính "
      "xác trên mỗi đơn vị tham số tốt hơn các kiến trúc nhẹ truyền thống, và là căn cứ quan "
      "trọng để đề tài lựa chọn EfficientNet làm bộ phân loại giai đoạn hai.")
    p("Về hướng phát hiện đối tượng, Đào Văn Thiên và cộng sự (2022) triển khai YOLOv3 trên dây "
      "chuyền phân loại hoa quả điều khiển bằng PLC, đạt khoảng 94% trên tập khoảng 1.000 ảnh cà "
      "chua. Nguyễn Văn Mạnh và cộng sự (2024) sử dụng YOLOv7 để phân loại cà chua, đạt 93,3% "
      "với quả bình thường và 89,1% với quả hỏng. Hai công trình này chứng minh họ YOLO đủ nhanh "
      "và đủ chính xác cho bài toán nông nghiệp thời gian thực, nhưng đều dừng ở mức nhận dạng "
      "đối tượng có ranh giới rõ ràng, chưa xử lý các tổn thương bệnh lý có biên mờ và kích "
      "thước rất nhỏ như trên lá cây.")

    h("1.2. Tình hình nghiên cứu ngoài nước", 3)
    p("Trên bình diện quốc tế, cây đu đủ đã bắt đầu nhận được sự quan tâm riêng. Gani (2025) giới "
      "thiệu PapayaNet, một kiến trúc học sâu chuyên biệt cho bệnh đu đủ. Mustofa và cộng sự "
      "(2024) công bố bộ dữ liệu BDPapayaLeaf và đánh giá nhiều mô hình trên bộ dữ liệu này, "
      "trong đó kết hợp YOLOv8 với Vision Transformer cho kết quả tốt nhất. Đây chính là bộ dữ "
      "liệu được đề tài sử dụng, cho phép so sánh trực tiếp với các kết quả đã công bố.")
    p("De Moraes và cộng sự (2023) đề xuất Yolo-Papaya, cải tiến YOLOv7 bằng khối chú ý CBAM để "
      "phát hiện bệnh trên quả đu đủ, công bố trên tạp chí Electronics. Công trình này cho thấy "
      "việc bổ sung cơ chế chú ý giúp mô hình tập trung tốt hơn vào vùng tổn thương nhỏ, nhưng "
      "đối tượng nghiên cứu là quả chứ không phải lá.")
    p("Ở phạm vi rộng hơn, Sharma và cộng sự (2020) khảo sát VGG-16, ResNet-50, DenseNet-121 và "
      "Inception V4 cho bài toán phân loại bệnh cây; Hussain và cộng sự (2022) huấn luyện một "
      "mạng tích chập sâu gồm ba tầng tích chập và hai tầng kết nối đầy đủ trên 10.000 ảnh kích "
      "thước 200×200 thuộc 20 loại bệnh, đạt khoảng 96%. Điểm chung của các công trình này là "
      "phân loại trên toàn bộ ảnh lá. Cách làm đó hoạt động tốt khi tổn thương chiếm tỷ lệ lớn "
      "trong khung hình, nhưng suy giảm rõ rệt khi vết bệnh chỉ chiếm vài phần trăm diện tích lá "
      "và bị lẫn vào nền phức tạp.")

    h("1.3. Khoảng trống nghiên cứu", 3)
    p("Từ khảo sát trên có thể rút ra ba khoảng trống. Thứ nhất, số lượng công trình dành riêng "
      "cho bệnh trên lá đu đủ còn rất hạn chế so với các cây trồng phổ biến như cà chua, lúa hay "
      "khoai tây. Thứ hai, phần lớn nghiên cứu lựa chọn hoặc hướng phát hiện đối tượng, hoặc "
      "hướng phân loại toàn ảnh, mà chưa khai thác sự bổ trợ giữa hai hướng này. Thứ ba, rất ít "
      "công trình công bố kèm theo một hệ thống triển khai hoàn chỉnh cho phép kiểm chứng lại "
      "kết quả. Đề tài này hướng tới lấp đồng thời cả ba khoảng trống đó.")

    # ----------------------------------------------------- 2. Lý do chọn đề tài
    h("2. Lý do chọn đề tài", 2)
    p("Đu đủ là cây ăn quả nhiệt đới có giá trị kinh tế cao, được trồng phổ biến tại nhiều tỉnh "
      "thành Việt Nam. Theo thống kê của Tổ chức Lương thực và Nông nghiệp Liên Hợp Quốc, sản "
      "lượng đu đủ toàn cầu liên tục tăng, song song với đó là áp lực dịch bệnh ngày càng lớn. "
      "Savary và cộng sự (2019) ước tính dịch hại cây trồng gây sụt giảm 20–40% sản lượng nông "
      "nghiệp toàn cầu mỗi năm.")
    p("Trên lá đu đủ, bốn nhóm bệnh thường gặp nhất là thán thư, đốm vòng, đốm vi khuẩn và xoăn "
      "lá. Các bệnh này có biểu hiện ban đầu khá giống nhau: đều bắt đầu bằng những đốm nhỏ đổi "
      "màu trên phiến lá. Chẩn đoán thủ công phụ thuộc vào kinh nghiệm của cán bộ kỹ thuật, tốn "
      "thời gian và dễ nhầm lẫn, đặc biệt ở giai đoạn sớm là giai đoạn can thiệp hiệu quả nhất. "
      "Việc nhầm lẫn giữa bệnh do nấm và bệnh do vi khuẩn hoặc virus dẫn tới sử dụng sai loại "
      "thuốc, vừa lãng phí chi phí vừa gây ô nhiễm môi trường.")
    p("Trong khi đó, điện thoại thông minh đã phổ cập tới hầu hết nông hộ. Nếu xây dựng được một "
      "hệ thống chỉ cần một bức ảnh chụp lá là có thể trả về chẩn đoán trong vài giây, rào cản "
      "kỹ thuật đối với người nông dân gần như được xóa bỏ. Đây là động lực chính để nhóm lựa "
      "chọn đề tài, với định hướng kỹ thuật là kết hợp thế mạnh định vị của họ YOLO và thế mạnh "
      "phân biệt chi tiết của họ EfficientNet trong một kiến trúc xếp tầng.")

    # ------------------------------------------------------------ 3. Mục tiêu
    h("3. Mục tiêu đề tài", 2)
    h("3.1. Mục tiêu tổng quát", 3)
    p("Xây dựng hệ thống tự động phát hiện và phân loại các loại bệnh hại trên lá cây đu đủ dựa "
      "trên công nghệ trí tuệ nhân tạo, mô hình YOLOv11 và CNN. Hệ thống nhằm hỗ trợ nông dân "
      "nhận biết sớm dịch bệnh, từ đó đưa ra biện pháp xử lý kịp thời, giúp giảm thiểu thiệt hại "
      "kinh tế và nâng cao năng suất cây trồng.")

    h("3.2. Mục tiêu cụ thể", 3)
    for line in [
        "Phát triển mô hình YOLOv11 có khả năng khoanh vùng chính xác các vùng biểu hiện bệnh "
        "trên lá đu đủ.",
        "Xây dựng mô hình mạng nơ-ron tích chập phân loại năm trạng thái: khỏe mạnh, đốm vòng, "
        "xoăn lá, đốm vi khuẩn và thán thư.",
        "Lựa chọn và sử dụng bộ dữ liệu khoa học có sẵn, bảo đảm tính khách quan và khả năng so "
        "sánh với các công trình đã công bố.",
        "Đạt độ chính xác cao, đặc biệt là khả năng phân biệt tốt giữa các bệnh có biểu hiện gần "
        "giống nhau.",
        "Triển khai mô hình lên nền tảng Web hoặc Mobile để trình diễn khả năng nhận dạng thời "
        "gian thực.",
        "Đánh giá tốc độ xử lý, độ chính xác và khả năng thích nghi của hệ thống trong các điều "
        "kiện ánh sáng và góc chụp khác nhau.",
    ]:
        bullet(line)

    # -------------------------------------------------------- 4. Phương pháp
    h("4. Phương pháp nghiên cứu", 2)
    p("Đề tài sử dụng phối hợp bốn nhóm phương pháp.")
    p("Phương pháp nghiên cứu tài liệu được dùng để khảo sát các công trình trong và ngoài nước, "
      "xác định khoảng trống nghiên cứu và lựa chọn kiến trúc nền tảng. Phương pháp thực nghiệm "
      "là phương pháp chủ đạo: toàn bộ mô hình được huấn luyện và đánh giá trên bộ dữ liệu "
      "BDPapayaLeaf với quy trình chia tập cố định và hạt giống ngẫu nhiên xác định, bảo đảm khả "
      "năng tái lập. Phương pháp so sánh định lượng được áp dụng khi đối chiếu chín tổ hợp bộ "
      "phát hiện và bộ phân loại, ba cấu hình tham chiếu và một đường cơ sở phân loại toàn ảnh. "
      "Cuối cùng, phương pháp phát triển hệ thống được dùng để đóng gói mô hình thành dịch vụ "
      "REST, giao diện web và container triển khai.")
    p("Các chỉ số đánh giá bao gồm Precision, Recall, F1-score, mAP@0,5, mAP@0,5:0,95 cho giai "
      "đoạn phát hiện; Precision, Recall, F1-score, độ chính xác tổng thể và ma trận nhầm lẫn "
      "cho giai đoạn phân loại và cho toàn hệ thống; cùng các chỉ số thời gian suy luận trung "
      "bình, trung vị và bách phân vị 90/95 cho đánh giá hiệu năng.")

    # ------------------------------------------------- 5. Đối tượng, phạm vi
    h("5. Đối tượng và phạm vi nghiên cứu", 2)
    h("5.1. Đối tượng nghiên cứu", 3)
    p("Đối tượng nghiên cứu là ảnh kỹ thuật số chụp lá cây đu đủ và các biểu hiện bệnh lý xuất "
      "hiện trên phiến lá, cùng với các mô hình học sâu phục vụ phát hiện và phân loại các biểu "
      "hiện đó.")

    h("5.2. Phạm vi nghiên cứu", 3)
    table("Phạm vi nghiên cứu của đề tài",
          ["Khía cạnh", "Phạm vi xác định"],
          [
              ["Đối tượng sinh học", "Lá cây đu đủ (Carica papaya); không xét thân, rễ, hoa, quả"],
              ["Số lớp", "5 lớp: Healthy, RingSpot, Curl, BacterialSpot, Anthracnose"],
              ["Nguồn dữ liệu", "BDPapayaLeaf V2 (Sarker và cộng sự, 2024), dữ liệu thứ cấp công bố trên Mendeley Data"],
              ["Kiến trúc phát hiện", "YOLOv11 (biến thể n, s, m)"],
              ["Kiến trúc phân loại", "EfficientNet-B0/B1/B2; tham chiếu VGG16, ResNet50, DenseNet121"],
              ["Công cụ", "Python, PyTorch, TensorFlow/Keras, Ultralytics, OpenCV, FastAPI, Gradio, Docker"],
              ["Môi trường thực nghiệm", "Google Colab với GPU; suy luận kiểm chứng trên máy trạm cục bộ"],
              ["Ngoài phạm vi", "Chẩn đoán mức độ nặng nhẹ của bệnh, khuyến cáo liều lượng thuốc, dữ liệu đa phổ"],
          ],
          widths=[4.6, 11.4])

    # ----------------------------------------------------------- 6. Bố cục
    h("6. Bố cục báo cáo", 2)
    p("Ngoài phần Mở đầu, Kết luận và kiến nghị, Tài liệu tham khảo và Phụ lục, nội dung chính "
      "của báo cáo được trình bày trong sáu chương:")
    for line in [
        "Chương 1. Tổng quan bài toán phát hiện và phân loại bệnh trên lá đu đủ.",
        "Chương 2. Cơ sở lý thuyết về học sâu, phát hiện đối tượng và các kiến trúc sử dụng.",
        "Chương 3. Phương pháp đề xuất: kiến trúc xếp tầng hai giai đoạn.",
        "Chương 4. Dữ liệu và thiết kế thực nghiệm.",
        "Chương 5. Kết quả thực nghiệm và thảo luận.",
        "Chương 6. Chương trình ứng dụng và khả năng triển khai.",
    ]:
        bullet(line)

    new_page()


build()
