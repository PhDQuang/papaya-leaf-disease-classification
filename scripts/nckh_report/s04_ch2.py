"""CHƯƠNG 2. CƠ SỞ LÝ THUYẾT."""
from __future__ import annotations

from .core import bullet, formula, h, h_center, new_page, note, p, table


def build() -> None:
    h_center("CHƯƠNG 2. CƠ SỞ LÝ THUYẾT", 1)

    # ------------------------------------------------------------------ 2.1
    h("2.1. Học máy và học sâu", 2)
    p("Học máy là nhánh của trí tuệ nhân tạo nghiên cứu các thuật toán cho phép máy tính cải "
      "thiện hiệu năng trên một nhiệm vụ thông qua kinh nghiệm, thay vì được lập trình tường "
      "minh từng bước. Với bài toán phân loại có giám sát, mục tiêu là học một ánh xạ từ không "
      "gian đầu vào sang tập nhãn dựa trên một tập mẫu đã gán nhãn.")
    p("Học sâu là nhóm phương pháp học máy sử dụng mạng nơ-ron nhân tạo nhiều tầng. Điểm khác "
      "biệt căn bản so với học máy truyền thống là khả năng học biểu diễn: thay vì phải thiết kế "
      "thủ công các đặc trưng như biểu đồ màu, ma trận đồng xuất hiện mức xám hay bộ lọc Gabor, "
      "mạng học sâu tự động học các đặc trưng phân cấp từ dữ liệu thô. Các tầng nông học những "
      "đặc trưng cấp thấp như cạnh và góc; các tầng sâu tổ hợp chúng thành các khái niệm ngữ "
      "nghĩa như kết cấu tổn thương hay hình dạng đốm bệnh.")
    p("Quá trình huấn luyện mạng nơ-ron dựa trên hai cơ chế. Lan truyền thuận tính toán đầu ra "
      "của mạng và giá trị hàm mất mát. Lan truyền ngược sử dụng quy tắc chuỗi để tính đạo hàm "
      "của hàm mất mát theo từng tham số, sau đó thuật toán tối ưu cập nhật tham số theo hướng "
      "làm giảm mất mát.")

    h("2.1.1. Hàm mất mát cho bài toán phân loại đa lớp", 3)
    p("Với bài toán phân loại C lớp, hàm mất mát phổ biến nhất là entropy chéo phân loại. Gọi "
      "y là vec-tơ nhãn dạng one-hot và p là vec-tơ xác suất dự đoán sau hàm softmax, hàm mất "
      "mát được tính theo công thức:")
    formula("L = − Σ(c = 1..C) y_c · log(p_c)", "2.1")
    p("Trong đó xác suất của lớp thứ c được chuẩn hóa bằng hàm softmax trên các giá trị logit z:")
    formula("p_c = exp(z_c) / Σ(j = 1..C) exp(z_j)", "2.2")
    p("Khi dữ liệu mất cân bằng, hàm mất mát trên bị chi phối bởi các lớp đa số. Giải pháp được "
      "đề tài sử dụng là gán trọng số nghịch đảo tần suất cho từng lớp:")
    formula("w_c = N_total / (C · N_c)", "2.3")
    p("với N_total là tổng số mẫu huấn luyện, C là số lớp và N_c là số mẫu của lớp c. Hàm mất "
      "mát có trọng số trở thành L = − Σ w_c · y_c · log(p_c), qua đó buộc mô hình dành sự chú ý "
      "tương xứng cho các lớp thiểu số.")

    h("2.1.2. Học chuyển giao", 3)
    p("Học chuyển giao là kỹ thuật tái sử dụng tri thức đã học từ một nhiệm vụ nguồn cho một "
      "nhiệm vụ đích. Trong thị giác máy tính, cách làm phổ biến là lấy một mạng đã huấn luyện "
      "trên ImageNet gồm hơn một triệu ảnh thuộc một nghìn lớp, giữ lại phần xương sống trích "
      "xuất đặc trưng và thay thế tầng phân loại cuối bằng tầng mới phù hợp số lớp của nhiệm vụ "
      "đích.")
    p("Kỹ thuật này đặc biệt phù hợp với đề tài vì bộ dữ liệu chuyên ngành có quy mô khiêm tốn so "
      "với ImageNet. Đề tài áp dụng chiến lược huấn luyện hai pha: pha thứ nhất đóng băng toàn "
      "bộ xương sống và chỉ huấn luyện phần đầu phân loại với tốc độ học lớn, giúp phần đầu hội "
      "tụ nhanh mà không phá hủy trọng số đã học; pha thứ hai mở khóa một số tầng cuối của xương "
      "sống và tinh chỉnh với tốc độ học nhỏ hơn hai bậc, giúp các đặc trưng cấp cao thích nghi "
      "với đặc thù tổn thương lá đu đủ.")

    h("2.1.3. Tăng cường dữ liệu và chính quy hóa", 3)
    p("Tăng cường dữ liệu tạo ra các biến thể hợp lý của ảnh huấn luyện nhằm mở rộng phân bố dữ "
      "liệu và giảm quá khớp. Các phép biến đổi được đề tài sử dụng gồm lật ngang ngẫu nhiên, "
      "xoay ngẫu nhiên trong biên độ nhỏ, thu phóng ngẫu nhiên và thay đổi độ tương phản ngẫu "
      "nhiên. Các phép biến đổi này được chọn có chủ đích: chúng mô phỏng sự thay đổi góc chụp "
      "và điều kiện chiếu sáng thực tế, đồng thời không làm biến dạng đặc trưng bệnh lý.")
    p("Bên cạnh đó, đề tài dùng dropout tại tầng trước phân loại để ngẫu nhiên vô hiệu hóa một "
      "tỷ lệ nơ-ron trong mỗi bước huấn luyện, dừng sớm khi chỉ số trên tập xác thực không cải "
      "thiện sau một số lượt nhất định, và giảm tốc độ học theo bình nguyên khi quá trình học "
      "chững lại.")

    # ------------------------------------------------------------------ 2.2
    h("2.2. Mạng nơ-ron tích chập", 2)
    p("Mạng nơ-ron tích chập là kiến trúc chuyên biệt cho dữ liệu có cấu trúc lưới như ảnh. Ba "
      "đặc tính cốt lõi của nó là kết nối cục bộ, chia sẻ trọng số và bất biến dịch chuyển cục "
      "bộ. Nhờ đó số tham số giảm mạnh so với mạng kết nối đầy đủ, đồng thời mô hình khai thác "
      "được tính tương quan không gian của điểm ảnh lân cận.")

    h("2.2.1. Tầng tích chập", 3)
    p("Tầng tích chập trượt một tập bộ lọc trên ảnh đầu vào và tính tích vô hướng tại mỗi vị "
      "trí. Với ảnh đầu vào kích thước H×W, bộ lọc kích thước k, bước trượt s và đệm p, kích "
      "thước đầu ra theo mỗi chiều được xác định bởi:")
    formula("H_out = ⌊(H + 2p − k) / s⌋ + 1", "2.4")
    p("Mỗi bộ lọc tạo ra một bản đồ đặc trưng phản ánh mức độ xuất hiện của một mẫu hình cụ thể "
      "tại từng vị trí trong ảnh.")

    h("2.2.2. Hàm kích hoạt và tầng gộp", 3)
    p("Hàm kích hoạt đưa tính phi tuyến vào mạng. Hàm ReLU được dùng phổ biến nhờ tính đơn giản "
      "và khả năng giảm hiện tượng tiêu biến đạo hàm:")
    formula("ReLU(x) = max(0, x)", "2.5")
    p("Các kiến trúc hiện đại như EfficientNet sử dụng hàm Swish, còn gọi là SiLU, cho kết quả "
      "tốt hơn nhờ tính trơn:")
    formula("Swish(x) = x · σ(x) = x / (1 + e^(−x))", "2.6")
    p("Tầng gộp giảm kích thước không gian của bản đồ đặc trưng, qua đó giảm chi phí tính toán "
      "và tăng trường tiếp nhận. Tầng gộp trung bình toàn cục được dùng ở cuối mạng để nén mỗi "
      "bản đồ đặc trưng thành một giá trị vô hướng, thay thế các tầng kết nối đầy đủ cồng kềnh.")

    h("2.2.3. Chuẩn hóa theo lô", 3)
    p("Chuẩn hóa theo lô chuẩn hóa đầu ra của mỗi tầng về trung bình không và phương sai đơn vị "
      "trong phạm vi một lô dữ liệu, sau đó áp dụng hai tham số khả học để khôi phục khả năng "
      "biểu diễn. Kỹ thuật này ổn định quá trình huấn luyện, cho phép dùng tốc độ học lớn hơn và "
      "có tác dụng chính quy hóa nhẹ.")

    # ------------------------------------------------------------------ 2.3
    h("2.3. Bài toán phát hiện đối tượng", 2)
    p("Khác với phân loại ảnh chỉ trả về một nhãn cho toàn ảnh, phát hiện đối tượng đồng thời "
      "xác định vị trí và nhãn của mọi đối tượng có mặt. Đầu ra của một bộ phát hiện là danh "
      "sách các bộ ba gồm khung bao quanh, nhãn lớp và độ tin cậy.")
    p("Các phương pháp phát hiện được chia thành hai nhóm. Nhóm hai giai đoạn, tiêu biểu là họ "
      "R-CNN, trước hết sinh ra tập vùng đề xuất rồi phân loại và tinh chỉnh từng vùng; nhóm này "
      "cho độ chính xác cao nhưng tốc độ chậm. Nhóm một giai đoạn, tiêu biểu là YOLO và SSD, dự "
      "đoán trực tiếp khung bao và nhãn trong một lần lan truyền thuận; nhóm này nhanh hơn nhiều "
      "và ngày nay đã thu hẹp đáng kể khoảng cách về độ chính xác.")
    p("Cần lưu ý rằng kiến trúc xếp tầng của đề tài không phải là bộ phát hiện hai giai đoạn "
      "theo nghĩa của họ R-CNN. Ở đây, giai đoạn một là một bộ phát hiện một giai đoạn hoàn "
      "chỉnh, còn giai đoạn hai là một bộ phân loại độc lập được huấn luyện riêng trên các vùng "
      "cắt, chứ không phải là phần đầu phân loại gắn liền trong cùng một mạng.")

    h("2.3.1. Tỷ lệ giao trên hợp", 3)
    p("Tỷ lệ giao trên hợp đo mức độ trùng khớp giữa khung dự đoán B_p và khung thực tế B_gt:")
    formula("IoU(B_p, B_gt) = Area(B_p ∩ B_gt) / Area(B_p ∪ B_gt)", "2.7")
    p("Một dự đoán được coi là dương tính thật khi IoU vượt một ngưỡng quy ước, thường là 0,5. "
      "IoU cũng là thành phần cốt lõi của thuật toán loại bỏ khung trùng lặp và của hàm mất mát "
      "định vị CIoU được dùng trong họ YOLO hiện đại.")

    h("2.3.2. Loại bỏ khung trùng lặp", 3)
    p("Sau khi dự đoán, một đối tượng thường được bao bởi nhiều khung gần giống nhau. Thuật toán "
      "loại bỏ khung trùng lặp sắp xếp các khung theo độ tin cậy giảm dần, giữ lại khung có độ "
      "tin cậy cao nhất và loại bỏ mọi khung còn lại có IoU với nó vượt ngưỡng đã định, rồi lặp "
      "lại cho tới khi hết khung. Đề tài sử dụng ngưỡng IoU bằng 0,7 cho bước này.")

    # ------------------------------------------------------------------ 2.4
    h("2.4. Họ mô hình YOLO và phiên bản YOLOv11", 2)
    p("YOLO chuyển bài toán phát hiện thành một bài toán hồi quy duy nhất trên lưới ô của ảnh. "
      "Terven và cộng sự (2024) đã tổng thuật quá trình phát triển từ YOLOv1 tới YOLOv11, cho "
      "thấy xu hướng cải tiến nhất quán qua các phiên bản: bỏ dần khung neo cố định, tăng cường "
      "kết hợp đặc trưng đa tỷ lệ, tách riêng nhánh phân loại và nhánh hồi quy khung, và tối ưu "
      "cân bằng giữa độ chính xác với chi phí tính toán.")
    p("Một mô hình YOLO hiện đại gồm ba khối. Xương sống trích xuất đặc trưng phân cấp từ ảnh "
      "đầu vào. Cổ nối hợp nhất đặc trưng từ nhiều mức độ phân giải để mô hình vừa phát hiện "
      "được đối tượng lớn vừa không bỏ sót đối tượng nhỏ. Đầu dự đoán sinh ra khung bao, nhãn "
      "lớp và độ tin cậy.")

    h("2.4.1. Các thành phần đặc trưng của YOLOv11", 3)
    for line in [
        "Khối C3k2: biến thể của khối nút cổ chai xuyên giai đoạn, sử dụng hai nhánh tích chập "
        "với kích thước nhân linh hoạt, giúp giảm số tham số mà vẫn duy trì khả năng biểu diễn.",
        "Khối SPPF: gộp kim tự tháp không gian phiên bản nhanh, áp dụng nhiều tầng gộp cực đại "
        "nối tiếp để mở rộng trường tiếp nhận với chi phí thấp, hữu ích khi tổn thương có kích "
        "thước rất khác nhau.",
        "Khối C2PSA: khối chú ý không gian từng phần, cho phép mạng tập trung vào vùng có khả "
        "năng chứa đối tượng và giảm ảnh hưởng của nền phức tạp.",
        "Đầu dự đoán tách rời, không khung neo: nhánh phân loại và nhánh hồi quy khung được tách "
        "riêng, loại bỏ nhu cầu thiết kế khung neo thủ công.",
    ]:
        bullet(line)

    h("2.4.2. Hàm mất mát của YOLOv11", 3)
    p("Hàm mất mát tổng của YOLOv11 là tổ hợp có trọng số của ba thành phần:")
    formula("L_total = λ_box · L_CIoU + λ_cls · L_BCE + λ_dfl · L_DFL", "2.8")
    p("Thành phần L_CIoU đo sai lệch định vị có xét đồng thời độ trùng lặp, khoảng cách giữa hai "
      "tâm và độ tương đồng tỷ lệ khung. Thành phần L_BCE là entropy chéo nhị phân cho nhánh "
      "phân loại. Thành phần L_DFL mô hình hóa tọa độ biên khung dưới dạng một phân phối rời rạc "
      "thay vì một giá trị đơn, giúp hồi quy biên chính xác hơn khi ranh giới đối tượng mờ — "
      "đúng với đặc thù tổn thương bệnh lá.")

    table("So sánh các biến thể YOLOv11 được khảo sát trong đề tài",
          ["Biến thể", "Quy mô tham số", "Đặc điểm", "Định hướng sử dụng"],
          [
              ["YOLOv11n", "Rất nhỏ", "Nhanh nhất, chi phí bộ nhớ thấp nhất",
               "Ưu tiên cho thiết bị di động, biên"],
              ["YOLOv11s", "Nhỏ", "Cân bằng giữa tốc độ và độ chính xác",
               "Triển khai trên máy chủ tài nguyên hạn chế"],
              ["YOLOv11m", "Trung bình", "Độ chính xác cao nhất trong ba biến thể khảo sát",
               "Lựa chọn cho hệ thống đề xuất"],
          ],
          widths=[2.8, 3.0, 5.4, 4.8])

    # ------------------------------------------------------------------ 2.5
    h("2.5. Họ mô hình EfficientNet", 2)
    p("EfficientNet do Tan và Le đề xuất, xuất phát từ nhận xét rằng việc mở rộng mạng theo một "
      "chiều đơn lẻ, chẳng hạn chỉ tăng chiều sâu hoặc chỉ tăng chiều rộng, nhanh chóng bão hòa "
      "về hiệu quả. Nhóm tác giả đề xuất phương pháp mở rộng phức hợp, tăng đồng thời chiều sâu "
      "d, chiều rộng w và độ phân giải r theo một hệ số φ duy nhất:")
    formula("d = α^φ,  w = β^φ,  r = γ^φ,  với α · β² · γ² ≈ 2 và α, β, γ ≥ 1", "2.9")
    p("Ràng buộc trên bảo đảm chi phí tính toán tăng xấp xỉ 2^φ lần khi φ tăng một đơn vị. Kết "
      "quả là họ mô hình từ B0 tới B7 với tỷ lệ chính xác trên mỗi đơn vị tham số vượt trội so "
      "với các kiến trúc trước đó.")

    h("2.5.1. Khối MBConv và khối Squeeze-and-Excitation", 3)
    p("Đơn vị cấu trúc chính của EfficientNet là khối MBConv. Khối này trước hết mở rộng số kênh "
      "bằng tích chập 1×1, sau đó áp dụng tích chập tách theo chiều sâu để trích xuất đặc trưng "
      "không gian với chi phí thấp, rồi nén trở lại số kênh ban đầu bằng một tích chập 1×1 khác. "
      "Kết nối tắt được thêm vào khi kích thước đầu vào và đầu ra trùng nhau.")
    p("Bên trong mỗi khối MBConv có một khối Squeeze-and-Excitation. Khối này nén thông tin không "
      "gian của mỗi kênh thành một giá trị bằng gộp trung bình toàn cục, đưa qua hai tầng kết "
      "nối đầy đủ để học trọng số quan trọng của từng kênh, rồi nhân trở lại vào bản đồ đặc "
      "trưng. Cơ chế này cho phép mạng tự động đề cao các kênh mang thông tin về màu sắc và kết "
      "cấu tổn thương, đồng thời giảm trọng số các kênh chủ yếu mã hóa nền.")

    table("Ba biến thể EfficientNet được khảo sát và cấu hình tương ứng",
          ["Biến thể", "Kích thước ảnh đầu vào", "Kích thước lô", "Số tầng mở khóa ở pha 2", "Tỷ lệ dropout"],
          [
              ["EfficientNet-B0", "224 × 224", "48", "40", "0,30"],
              ["EfficientNet-B1", "240 × 240", "40", "50", "0,30"],
              ["EfficientNet-B2", "260 × 260", "32", "60", "0,35"],
          ],
          widths=[3.6, 3.6, 2.8, 3.4, 2.6])

    # ------------------------------------------------------------------ 2.6
    h("2.6. Các kiến trúc tham chiếu", 2)
    p("Để đánh giá khách quan lựa chọn EfficientNet-B2, đề tài huấn luyện thêm ba kiến trúc kinh "
      "điển làm tham chiếu, đều theo cùng giao thức dữ liệu và cùng chiến lược hai pha.")
    p("VGG16 gồm mười ba tầng tích chập 3×3 xếp chồng và ba tầng kết nối đầy đủ. Kiến trúc đồng "
      "nhất và dễ hiểu, nhưng số tham số rất lớn, chủ yếu tập trung ở các tầng kết nối đầy đủ.")
    p("ResNet50 giới thiệu kết nối phần dư, cho phép tín hiệu đạo hàm truyền thẳng qua nhiều "
      "tầng và nhờ đó huấn luyện được các mạng rất sâu. Mỗi khối phần dư học phần hiệu chỉnh so "
      "với ánh xạ đồng nhất thay vì học trực tiếp ánh xạ mục tiêu.")
    p("DenseNet121 mở rộng ý tưởng trên bằng cách nối đầu ra của mọi tầng trước vào đầu vào của "
      "tầng sau trong cùng một khối dày đặc. Cách kết nối này tái sử dụng đặc trưng triệt để và "
      "giảm số tham số so với chiều sâu tương đương.")

    # ------------------------------------------------------------------ 2.7
    h("2.7. Các chỉ số đánh giá", 2)
    p("Gọi TP, FP, FN lần lượt là số dương tính thật, dương tính giả và âm tính giả. Các chỉ số "
      "cơ bản được định nghĩa như sau.")
    formula("Precision = TP / (TP + FP)", "2.10")
    formula("Recall = TP / (TP + FN)", "2.11")
    formula("F1 = 2 · Precision · Recall / (Precision + Recall)", "2.12")
    formula("Accuracy = (TP + TN) / (TP + TN + FP + FN)", "2.13")
    p("Precision trả lời câu hỏi trong những trường hợp mô hình báo bệnh, bao nhiêu phần trăm là "
      "đúng; Recall trả lời câu hỏi trong những trường hợp thực sự có bệnh, mô hình phát hiện "
      "được bao nhiêu phần trăm. Với ứng dụng nông nghiệp, Recall thường được ưu tiên vì bỏ sót "
      "một cây bệnh gây thiệt hại lớn hơn một cảnh báo nhầm.")
    p("Với bài toán phát hiện, độ chính xác trung bình AP của một lớp là diện tích dưới đường "
      "cong Precision–Recall; mAP là trung bình của AP trên tất cả các lớp:")
    formula("AP = ∫(0..1) Precision(Recall) d(Recall);   mAP = (1/C) · Σ AP_c", "2.14")
    p("mAP@0,5 tính ở ngưỡng IoU cố định 0,5, phản ánh khả năng phát hiện đúng đối tượng. "
      "mAP@0,5:0,95 lấy trung bình trên mười ngưỡng IoU từ 0,5 tới 0,95 với bước 0,05, là chỉ số "
      "khắt khe hơn vì đòi hỏi khung bao khớp chặt với khung thực tế.")
    p("Với bài toán phân loại đa lớp, trung bình vĩ mô lấy trung bình số học của chỉ số trên các "
      "lớp, coi mọi lớp quan trọng như nhau; trung bình có trọng số lấy trung bình theo số mẫu "
      "của từng lớp. Trong bối cảnh dữ liệu mất cân bằng của đề tài, trung bình vĩ mô là chỉ số "
      "phản ánh trung thực hơn năng lực thực sự của mô hình trên các lớp hiếm.")
    p("Ma trận nhầm lẫn là công cụ chẩn đoán quan trọng nhất trong phần phân tích lỗi. Mỗi ô của "
      "ma trận cho biết số mẫu thuộc lớp thực tế ở hàng được dự đoán thành lớp ở cột, nhờ đó "
      "xác định được chính xác cặp lớp nào bị nhầm lẫn và theo chiều nào.")

    # ------------------------------------------------------------------ 2.8
    h("2.8. Tổng kết chương", 2)
    p("Chương này đã trình bày nền tảng lý thuyết cho toàn bộ phần thực nghiệm: cơ chế học của "
      "mạng nơ-ron tích chập, kỹ thuật học chuyển giao hai pha và xử lý mất cân bằng bằng trọng "
      "số lớp, nguyên lý phát hiện đối tượng cùng các thành phần đặc trưng của YOLOv11, nguyên "
      "lý mở rộng phức hợp của EfficientNet, ba kiến trúc tham chiếu và hệ thống chỉ số đánh "
      "giá. Chương tiếp theo vận dụng các nền tảng này để trình bày phương pháp xếp tầng hai "
      "giai đoạn mà đề tài đề xuất.")

    new_page()


build()
