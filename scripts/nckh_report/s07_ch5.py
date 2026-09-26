"""CHƯƠNG 5. KẾT QUẢ THỰC NGHIỆM VÀ THẢO LUẬN."""
from __future__ import annotations

from . import sec_5_1_5, sec_5_6_hinh
from .core import (bullet, figure, figure_row, h, h_center, new_page, note, p,
                   ref, table)


def build() -> None:
    h_center("CHƯƠNG 5. KẾT QUẢ THỰC NGHIỆM VÀ THẢO LUẬN", 1)

    # ================================================================== 5.1
    h("5.1. Kết quả giai đoạn phát hiện đối tượng", 2)

    h("5.1.1. So sánh ba biến thể YOLOv11", 3)
    p("Ba biến thể YOLOv11n, YOLOv11s và YOLOv11m được huấn luyện với cùng bộ siêu tham số và "
      "đánh giá trên cùng tập kiểm tra gồm 257 ảnh. Kết quả được tổng hợp trong bảng dưới đây.")

    table("So sánh hiệu năng ba biến thể YOLOv11 trên tập kiểm tra",
          ["Biến thể", "Precision", "Recall", "mAP@0,5", "mAP@0,75", "mAP@0,5:0,95",
           "Thời gian suy luận (ms)"],
          [
              ["YOLOv11n", "0,7461", "0,7563", "0,7471", "0,6568", "0,6126", "7,24"],
              ["YOLOv11s", "0,8132", "0,8089", "0,7657", "0,6838", "0,6446", "10,83"],
              ["YOLOv11m", "0,8024", "0,8162", "0,7767", "0,6976", "0,6520", "29,66"],
          ],
          widths=[2.4, 2.2, 2.0, 2.2, 2.2, 2.6, 2.4], font_size=10.5)

    p("YOLOv11m đạt giá trị cao nhất ở ba chỉ số quan trọng nhất là Recall (0,8162), mAP@0,5 "
      "(0,7767) và mAP@0,5:0,95 (0,6520). Điểm đáng chú ý là YOLOv11s có Precision cao hơn "
      "(0,8132 so với 0,8024) nhưng Recall và mAP thấp hơn. Điều này phản ánh xu hướng của mô "
      "hình nhỏ hơn: nó thận trọng hơn, chỉ báo cáo những tổn thương rõ ràng, nên ít báo nhầm "
      "nhưng bỏ sót nhiều hơn.")
    p("Với bài toán chẩn đoán bệnh cây, Recall được ưu tiên hơn Precision vì hậu quả của việc bỏ "
      "sót một lá bệnh nặng nề hơn nhiều so với một cảnh báo nhầm. Hơn nữa, trong kiến trúc xếp "
      "tầng, một khung dương tính giả ở giai đoạn một vẫn có cơ hội được giai đoạn hai sửa chữa, "
      "còn một tổn thương bị bỏ sót thì mất vĩnh viễn. Vì vậy YOLOv11m được chọn cho hệ thống "
      "cuối cùng, chấp nhận chi phí thời gian suy luận cao hơn khoảng ba lần so với YOLOv11s.")
    p("Về chênh lệch giữa mAP@0,5 và mAP@0,5:0,95 — khoảng 0,125 với YOLOv11m — con số này cho "
      "biết mô hình định vị đúng vị trí tổn thương nhưng ranh giới khung chưa thật khớp. Đây là "
      "hạn chế cố hữu của bài toán: tổn thương bệnh lá không có biên rõ ràng như vật thể nhân "
      "tạo, ngay cả chuyên gia gán nhãn cũng khó thống nhất tuyệt đối về ranh giới. Trong kiến "
      "trúc của đề tài, hạn chế này ít ảnh hưởng vì khung còn được mở rộng thêm 10% trước khi "
      "cắt.")

    h("5.1.2. Kết quả chi tiết theo lớp của YOLOv11m", 3)
    table("Hiệu năng phát hiện theo từng lớp bệnh của YOLOv11m trên tập kiểm tra",
          ["Lớp", "Số ảnh", "Số thực thể", "Precision", "Recall", "F1", "mAP@0,5", "mAP@0,5:0,95"],
          [
              ["Anthracnose", "54", "1.054", "0,5776", "0,6214", "0,5987", "0,5151", "0,3186"],
              ["BacterialSpot", "69", "69", "0,9583", "1,0000", "0,9787", "0,9934", "0,9151"],
              ["Curl", "54", "54", "0,9818", "1,0000", "0,9908", "0,9948", "0,9483"],
              ["RingSpot", "80", "639", "0,6920", "0,6432", "0,6667", "0,6035", "0,4261"],
          ],
          widths=[3.0, 1.8, 2.2, 2.2, 2.0, 1.8, 2.0, 2.4], font_size=10.5,
          key="yolo_per_class")

    p("Bảng trên hé lộ một quy luật rất rõ ràng: hiệu năng phát hiện tỷ lệ nghịch với mật độ "
      "thực thể trên mỗi ảnh. Hai lớp BacterialSpot và Curl có đúng một thực thể trên mỗi ảnh "
      "(69 thực thể trên 69 ảnh; 54 thực thể trên 54 ảnh) và đạt Recall tuyệt đối 1,0 cùng "
      "mAP@0,5 trên 0,99. Ngược lại, lớp Anthracnose có trung bình 19,5 thực thể trên mỗi ảnh và "
      "chỉ đạt mAP@0,5 bằng 0,5151; lớp RingSpot có trung bình 8,0 thực thể mỗi ảnh và đạt "
      "0,6035.")
    p("Nguyên nhân nằm ở bản chất của phép đo mAP ở mức thực thể. Khi một lá thán thư có bốn "
      "mươi đốm bệnh nhỏ nằm sát nhau, mô hình có thể gộp hai đốm liền kề thành một khung hoặc "
      "tách một đốm lớn thành hai khung. Mỗi sai lệch như vậy sinh ra đồng thời một dương tính "
      "giả và một âm tính giả, làm sụt cả Precision lẫn Recall — trong khi về mặt chẩn đoán, kết "
      "luận cuối cùng vẫn hoàn toàn đúng.")
    p("Đây chính là lý do quan trọng nhất giải thích vì sao đề tài không đánh giá hệ thống bằng "
      "chỉ số của riêng giai đoạn phát hiện. Chỉ số mAP ở mức thực thể phạt nặng những sai lệch "
      "không ảnh hưởng tới quyết định chẩn đoán. Kết quả ở mục 5.3 sẽ cho thấy lớp Anthracnose "
      "đạt F1 bằng 0,9358 ở mức ảnh, cao hơn rất nhiều so với con số 0,5987 ở mức thực thể.")

    figure("outputs/yolo/test_evaluations/yolov11_m/BoxPR_curve.png",
           "Đường cong Precision–Recall của YOLOv11m trên tập kiểm tra, tách theo từng lớp bệnh",
           width=13.5)

    figure("outputs/yolo/test_evaluations/yolov11_m/BoxF1_curve.png",
           "Đường cong F1 theo ngưỡng tin cậy của YOLOv11m trên tập kiểm tra", width=13.5)

    p("Đường cong F1 theo ngưỡng tin cậy là căn cứ thực nghiệm cho việc chọn ngưỡng khởi đầu "
      "0,50 trong hệ thống suy luận: đây là vùng ngưỡng mà F1 tổng hợp đạt gần cực đại, đồng "
      "thời chưa quá thấp để sinh ra lượng lớn khung nhiễu.")

    figure_row([
        ("outputs/yolo/test_evaluations/yolov11_m/BoxP_curve.png", "Precision"),
        ("outputs/yolo/test_evaluations/yolov11_m/BoxR_curve.png", "Recall"),
    ], "Đường cong Precision và Recall theo ngưỡng tin cậy của YOLOv11m trên tập kiểm tra",
        width=7.4)

    h("5.1.3. Ma trận nhầm lẫn ở giai đoạn phát hiện", 3)
    table("Ma trận nhầm lẫn của YOLOv11m ở mức thực thể trên tập kiểm tra "
          "(hàng: lớp dự đoán; cột: lớp thực tế)",
          ["Dự đoán \\ Thực tế", "Anthracnose", "BacterialSpot", "Curl", "RingSpot", "Nền"],
          [
              ["Anthracnose", "735", "0", "0", "1", "672"],
              ["BacterialSpot", "0", "69", "0", "0", "3"],
              ["Curl", "0", "0", "54", "0", "1"],
              ["RingSpot", "0", "0", "0", "440", "244"],
              ["Nền (bỏ sót)", "319", "0", "0", "198", "0"],
          ],
          widths=[3.4, 2.6, 2.8, 2.0, 2.4, 2.4], font_size=10.5)

    p("Ma trận nhầm lẫn khẳng định lại phân tích trên và bổ sung một chi tiết quan trọng: hầu "
      "như không có sự nhầm lẫn chéo giữa các lớp bệnh. Cột Anthracnose chỉ có duy nhất một thực "
      "thể bị gán nhầm sang RingSpot; các lớp BacterialSpot và Curl hoàn toàn không bị nhầm sang "
      "lớp nào khác.")
    p("Toàn bộ sai sót tập trung ở hai cột liên quan tới nền: 672 khung Anthracnose và 244 khung "
      "RingSpot là dương tính giả trên nền, còn 319 thực thể Anthracnose và 198 thực thể RingSpot "
      "bị bỏ sót. Nói cách khác, mô hình phân biệt rất tốt bệnh nào là bệnh nào; khó khăn duy "
      "nhất của nó là đếm và khoanh chính xác từng đốm riêng lẻ trong đám đông đốm.")
    p("Đối với kiến trúc xếp tầng, đây là kiểu sai sót ít nguy hại nhất. Một khung dương tính "
      "giả trên nền lá sẽ được giai đoạn hai phân loại và đóng góp một phiếu có trọng số thấp; "
      "một tổn thương bị bỏ sót trong số hàng chục tổn thương cùng loại không làm thay đổi kết "
      "quả bỏ phiếu.")

    figure_row([
        ("outputs/yolo/test_evaluations/yolov11_m/confusion_matrix.png", "Giá trị tuyệt đối"),
        ("outputs/yolo/test_evaluations/yolov11_m/confusion_matrix_normalized.png", "Chuẩn hóa"),
    ], "Ma trận nhầm lẫn của YOLOv11m trên tập kiểm tra", width=7.4)

    h("5.1.4. Minh họa kết quả phát hiện", 3)
    figure_row([
        ("outputs/yolo/test_evaluations/yolov11_m/val_batch0_labels.jpg", "Nhãn thực tế"),
        ("outputs/yolo/test_evaluations/yolov11_m/val_batch0_pred.jpg", "Dự đoán của mô hình"),
    ], "Đối chiếu nhãn thực tế và dự đoán của YOLOv11m trên một lô ảnh kiểm tra", width=7.4)

    sec_5_1_5.build()

    new_page()

    # ================================================================== 5.2
    h("5.2. Kết quả giai đoạn phân loại vùng quan tâm", 2)

    h("5.2.1. Hiệu năng tổng thể của EfficientNet-B2", 3)
    p("Bộ phân loại EfficientNet-B2 được đánh giá trên 1.836 vùng quan tâm của tập kiểm tra, "
      "hoàn toàn tách biệt với dữ liệu huấn luyện và xác thực.")

    table("Hiệu năng tổng thể của EfficientNet-B2 trên 1.836 vùng quan tâm kiểm tra",
          ["Chỉ số", "Giá trị"],
          [
              ["Độ chính xác tổng thể (Accuracy)", "0,9602"],
              ["Precision trung bình vĩ mô", "0,9598"],
              ["Recall trung bình vĩ mô", "0,9560"],
              ["F1 trung bình vĩ mô", "0,9569"],
              ["Precision trung bình có trọng số", "0,9606"],
              ["Recall trung bình có trọng số", "0,9602"],
              ["F1 trung bình có trọng số", "0,9602"],
              ["Số mẫu kiểm tra", "1.836"],
          ],
          widths=[8.0, 4.0])

    p("Điểm đáng chú ý nhất là khoảng cách rất nhỏ giữa trung bình vĩ mô (0,9569) và trung bình "
      "có trọng số (0,9602) của chỉ số F1 — chỉ 0,0033. Trên một bộ dữ liệu mất cân bằng 27,6 "
      "lần, khoảng cách hẹp như vậy chứng tỏ mô hình không hy sinh các lớp hiếm để tối ưu độ "
      "chính xác tổng thể. Đây là bằng chứng trực tiếp cho hiệu quả của cơ chế trọng số lớp đã "
      "trình bày ở mục 4.3.1.")

    h("5.2.2. Hiệu năng theo từng lớp", 3)
    table("Hiệu năng phân loại theo từng lớp của EfficientNet-B2 trên vùng quan tâm",
          ["Lớp", "Precision", "Recall", "F1-score", "Số mẫu"],
          [
              ["Anthracnose", "0,9638", "0,9721", "0,9679", "1.040"],
              ["BacterialSpot", "0,8961", "1,0000", "0,9452", "69"],
              ["Curl", "0,9804", "0,9259", "0,9524", "54"],
              ["Healthy", "1,0000", "0,9412", "0,9697", "34"],
              ["RingSpot", "0,9585", "0,9405", "0,9494", "639"],
          ],
          widths=[3.6, 3.0, 3.0, 3.0, 3.0])

    p("Lớp Healthy đạt Precision tuyệt đối 1,0000: không có vùng bệnh nào bị nhận nhầm thành "
      "khỏe mạnh. Đây là đặc tính rất giá trị trong ứng dụng thực tế vì nó loại trừ kiểu sai sót "
      "nguy hiểm nhất — trấn an người dùng khi cây thực sự đang mang bệnh. Recall của lớp này là "
      "0,9412, tương ứng hai trong ba mươi tư vùng khỏe mạnh bị nhận nhầm thành có bệnh; sai sót "
      "theo chiều này chỉ dẫn tới kiểm tra lại, không gây thiệt hại.")
    p("Lớp BacterialSpot cho thấy mẫu hình ngược lại: Recall tuyệt đối 1,0000 nhưng Precision "
      "thấp nhất trong năm lớp (0,8961). Mô hình phát hiện được toàn bộ 69 vùng đốm vi khuẩn "
      "nhưng đồng thời gán nhầm một số vùng thuộc lớp khác vào đây. Do đốm vi khuẩn giai đoạn "
      "sớm có hình thái gần giống đốm thán thư nhỏ, xu hướng nhầm lẫn này là dễ hiểu.")
    p("Lớp Curl có Precision cao (0,9804) nhưng Recall thấp nhất (0,9259). Nguyên nhân có tính "
      "cấu trúc: xoăn lá là biến dạng ở mức toàn cục, khi bị cắt thành vùng quan tâm cục bộ, một "
      "phần thông tin hình thái bị mất. Bốn trong năm mươi tư vùng Curl bị bỏ sót chính là hệ "
      "quả của điều này.")

    figure("outputs/cnn/efficientnet_b2/test_confusion_matrix.png",
           "Ma trận nhầm lẫn của EfficientNet-B2 trên 1.836 vùng quan tâm kiểm tra", width=12.5)

    h("5.2.3. Quá trình huấn luyện", 3)
    figure_row([
        ("outputs/cnn/efficientnet_b2/history_accuracy.png", "Độ chính xác"),
        ("outputs/cnn/efficientnet_b2/history_loss.png", "Hàm mất mát"),
    ], "Diễn biến độ chính xác và hàm mất mát của EfficientNet-B2 qua hai pha huấn luyện",
        width=7.4)

    p("Đường cong huấn luyện thể hiện rõ hai pha. Trong tám epoch đầu với xương sống bị đóng "
      "băng, mô hình hội tụ nhanh về một mức bình nguyên — đây là giới hạn của việc chỉ huấn "
      "luyện phần đầu phân loại trên các đặc trưng ImageNet chưa thích nghi. Khi pha hai bắt đầu "
      "và sáu mươi tầng cuối được mở khóa với tốc độ học giảm hai mươi lần, cả độ chính xác lẫn "
      "hàm mất mát đều cải thiện thêm một bậc rõ rệt. Pha hai dừng ở epoch thứ mười bốn trên "
      "tổng số hai mươi epoch dự kiến do cơ chế dừng sớm kích hoạt, cho thấy mô hình đã khai "
      "thác hết thông tin có ích từ dữ liệu huấn luyện.")
    p("Khoảng cách giữa đường huấn luyện và đường xác thực được duy trì ở mức hẹp trong suốt quá "
      "trình, xác nhận rằng tổ hợp dropout 0,35, tăng cường dữ liệu và dừng sớm đã kiểm soát "
      "hiệu quả hiện tượng quá khớp.")

    h("5.2.4. So sánh ba biến thể EfficientNet", 3)
    figure_row([
        ("outputs/cnn/efficientnet_b0/history_accuracy.png", "EfficientNet-B0"),
        ("outputs/cnn/efficientnet_b1/history_accuracy.png", "EfficientNet-B1"),
    ], "Diễn biến độ chính xác của EfficientNet-B0 và EfficientNet-B1 trong quá trình huấn luyện",
        width=7.4)

    figure_row([
        ("outputs/cnn/efficientnet_b0/test_confusion_matrix.png", "EfficientNet-B0"),
        ("outputs/cnn/efficientnet_b1/test_confusion_matrix.png", "EfficientNet-B1"),
    ], "Ma trận nhầm lẫn của EfficientNet-B0 và EfficientNet-B1 trên tập vùng quan tâm kiểm tra",
        width=7.4)

    p("So sánh trực tiếp ba biến thể sẽ được trình bày ở mức hệ thống trong mục 5.3, vì đây mới "
      "là tiêu chí lựa chọn cuối cùng của đề tài.")

    new_page()

    # ================================================================== 5.3
    h("5.3. Kết quả của hệ thống xếp tầng ở mức ảnh", 2)

    h("5.3.1. So sánh chín tổ hợp", 3)
    p("Chín tổ hợp giữa ba biến thể bộ phát hiện và ba biến thể bộ phân loại được đánh giá trên "
      "cùng 291 ảnh kiểm tra, với cùng bộ siêu tham số suy luận đã liệt kê ở Bảng "
      + ref("sieu_tham_so") + ".")

    table("Hiệu năng của chín tổ hợp xếp tầng trên 291 ảnh kiểm tra, sắp xếp theo độ chính xác",
          ["Xếp hạng", "Bộ phát hiện", "Bộ phân loại", "Accuracy", "Macro P", "Macro R", "Macro F1"],
          [
              ["1", "YOLOv11m", "EfficientNet-B2", "0,9485", "0,9492", "0,9493", "0,9492"],
              ["2", "YOLOv11n", "EfficientNet-B2", "0,9381", "0,9440", "0,9440", "0,9414"],
              ["3", "YOLOv11m", "EfficientNet-B1", "0,9450", "0,9375", "0,9468", "0,9409"],
              ["4", "YOLOv11s", "EfficientNet-B2", "0,9381", "0,9371", "0,9428", "0,9398"],
              ["5", "YOLOv11m", "EfficientNet-B0", "0,9347", "0,9278", "0,9373", "0,9309"],
              ["6", "YOLOv11s", "EfficientNet-B1", "0,9313", "0,9232", "0,9386", "0,9285"],
              ["7", "YOLOv11n", "EfficientNet-B1", "0,9278", "0,9242", "0,9361", "0,9262"],
              ["8", "YOLOv11s", "EfficientNet-B0", "0,9141", "0,9070", "0,9221", "0,9102"],
              ["9", "YOLOv11n", "EfficientNet-B0", "0,9072", "0,9031", "0,9183", "0,9041"],
          ],
          widths=[1.8, 2.8, 3.2, 2.2, 2.0, 2.0, 2.0], font_size=10.5)

    p("Kết quả cho phép rút ra ba nhận định. Thứ nhất, tổ hợp YOLOv11m + EfficientNet-B2 đứng "
      "đầu ở cả bốn chỉ số, xác nhận lựa chọn của đề tài. Thứ hai, ảnh hưởng của bộ phân loại "
      "lớn hơn ảnh hưởng của bộ phát hiện: khi cố định bộ phát hiện là YOLOv11m và thay bộ phân "
      "loại từ B0 lên B2, macro F1 tăng 1,83 điểm phần trăm; ngược lại, khi cố định bộ phân loại "
      "là B2 và thay bộ phát hiện từ n lên m, macro F1 chỉ tăng 0,78 điểm phần trăm.")
    p("Thứ ba, và đáng chú ý nhất, tổ hợp YOLOv11n + EfficientNet-B2 xếp hạng hai với macro F1 "
      "bằng 0,9414, vượt qua cả tổ hợp YOLOv11m + EfficientNet-B1 về chỉ số này. Điều đó có "
      "nghĩa là một bộ phát hiện nhẹ hơn bốn lần về thời gian suy luận vẫn đủ tốt nếu được ghép "
      "với bộ phân loại mạnh. Phát hiện này có giá trị thực tiễn trực tiếp cho định hướng triển "
      "khai trên thiết bị di động.")

    figure_row([
        ("outputs/pipeline_evaluation/comparison_accuracy.png", "Accuracy"),
        ("outputs/pipeline_evaluation/comparison_macro_f1.png", "Macro F1"),
    ], "So sánh độ chính xác và F1 trung bình vĩ mô của chín tổ hợp xếp tầng", width=7.4)

    figure_row([
        ("outputs/pipeline_evaluation/comparison_macro_recall.png", "Macro Recall"),
        ("outputs/pipeline_evaluation/comparison_weighted_f1.png", "Weighted F1"),
    ], "So sánh Recall trung bình vĩ mô và F1 trung bình có trọng số của chín tổ hợp xếp tầng",
        width=7.4)

    h("5.3.2. Kết quả chi tiết của cấu hình đề xuất", 3)
    table("Hiệu năng theo từng lớp của hệ thống YOLOv11m + EfficientNet-B2 trên 291 ảnh kiểm tra",
          ["Lớp", "Precision", "Recall", "F1-score", "Số ảnh", "Số ảnh đúng"],
          [
              ["Anthracnose", "0,9273", "0,9444", "0,9358", "54", "51"],
              ["BacterialSpot", "0,9701", "0,9420", "0,9559", "69", "65"],
              ["Curl", "0,9815", "0,9815", "0,9815", "54", "53"],
              ["Healthy", "0,9412", "0,9412", "0,9412", "34", "32"],
              ["RingSpot", "0,9259", "0,9375", "0,9317", "80", "75"],
              ["Trung bình vĩ mô", "0,9492", "0,9493", "0,9492", "291", "276"],
              ["Trung bình có trọng số", "0,9488", "0,9485", "0,9485", "291", "276"],
          ],
          widths=[4.2, 2.6, 2.4, 2.6, 2.2, 2.6])

    p("Hệ thống dự đoán đúng 276 trên 291 ảnh, tương đương 94,85%. Cả năm lớp đều đạt F1 trên "
      "0,93, không có lớp nào bị bỏ rơi. Kết quả này cần được đặt cạnh kết quả ở mục 5.1.2 để "
      "thấy rõ giá trị của kiến trúc xếp tầng: lớp Anthracnose chỉ đạt F1 bằng 0,5987 ở mức thực "
      "thể nhưng đạt 0,9358 ở mức ảnh; lớp RingSpot tăng từ 0,6667 lên 0,9317. Cơ chế bỏ phiếu "
      "có trọng số đã chuyển hóa những dự đoán cục bộ không hoàn hảo thành một kết luận tổng thể "
      "chính xác.")
    p("Lớp Curl đạt kết quả tốt nhất với F1 bằng 0,9815, chỉ sai một ảnh. Điều thú vị là ở mức "
      "vùng quan tâm, Curl lại là lớp có Recall thấp nhất (0,9259). Nghịch lý này được giải "
      "thích bởi đặc thù dữ liệu: mỗi ảnh Curl chỉ có một vùng quan tâm, nên khi bộ phát hiện "
      "khoanh đúng vùng đó (Recall 1,0 ở mức thực thể theo Bảng " + ref("yolo_per_class")
      + ") thì kết quả mức ảnh gần như "
      "được quyết định hoàn toàn bởi một dự đoán duy nhất, và dự đoán đó thường đúng.")

    figure("outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/confusion_matrix.png",
           "Ma trận nhầm lẫn của hệ thống YOLOv11m + EfficientNet-B2 trên 291 ảnh kiểm tra",
           width=12.5)

    table("Ma trận nhầm lẫn của hệ thống đề xuất (hàng: lớp thực tế; cột: lớp dự đoán)",
          ["Thực tế \\ Dự đoán", "Anthracnose", "BacterialSpot", "Curl", "Healthy", "RingSpot"],
          [
              ["Anthracnose", "51", "0", "0", "0", "3"],
              ["BacterialSpot", "1", "65", "1", "0", "2"],
              ["Curl", "0", "1", "53", "0", "0"],
              ["Healthy", "0", "1", "0", "32", "1"],
              ["RingSpot", "3", "0", "0", "2", "75"],
          ],
          widths=[3.4, 2.6, 2.8, 2.0, 2.2, 2.4])

    p("Ma trận nhầm lẫn cho thấy cặp lớp bị nhầm lẫn nhiều nhất là Anthracnose và RingSpot, với "
      "ba ảnh sai theo mỗi chiều, tổng cộng sáu trong mười lăm ca sai. Đây là kết quả hoàn toàn "
      "phù hợp với kỳ vọng sinh học: cả hai bệnh đều biểu hiện bằng đốm tròn màu nâu trên phiến "
      "lá, dấu hiệu phân biệt duy nhất là cấu trúc vòng đồng tâm của đốm vòng — một đặc trưng "
      "rất tinh tế, thường mờ nhạt ở giai đoạn sớm và dễ bị che lấp bởi bóng lá hoặc phản xạ ánh "
      "sáng.")

    new_page()

    # ================================================================== 5.4
    h("5.4. So sánh với các đường cơ sở", 2)

    h("5.4.1. So sánh với phân loại toàn ảnh", 3)
    p("Câu hỏi then chốt của đề tài là: kiến trúc xếp tầng có thực sự tốt hơn cách làm thông "
      "thường là đưa cả ảnh vào một mạng phân loại hay không? Để trả lời, cùng một kiến trúc "
      "EfficientNet-B2 được huấn luyện lại theo hướng phân loại toàn ảnh và đánh giá trên đúng "
      "291 ảnh kiểm tra.")

    table("So sánh hệ thống xếp tầng với đường cơ sở phân loại toàn ảnh trên 291 ảnh kiểm tra",
          ["Phương pháp", "Accuracy", "Macro P", "Macro R", "Macro F1", "Weighted F1"],
          [
              ["EfficientNet-B2 phân loại toàn ảnh", "0,9278", "0,9317", "0,9286", "0,9293", "0,9274"],
              ["YOLOv11m + EfficientNet-B2 (đề xuất)", "0,9485", "0,9492", "0,9493", "0,9492", "0,9485"],
              ["Mức cải thiện", "+2,07 đp", "+1,75 đp", "+2,07 đp", "+1,99 đp", "+2,11 đp"],
          ],
          widths=[6.2, 2.2, 2.0, 2.0, 2.0, 2.2], font_size=10.5)

    p("Hệ thống xếp tầng vượt đường cơ sở 2,07 điểm phần trăm về độ chính xác và 1,99 điểm phần "
      "trăm về F1 trung bình vĩ mô. Xét trên 291 ảnh, mức chênh này tương ứng sáu ảnh được sửa "
      "đúng: đường cơ sở sai 21 ảnh trong khi hệ thống đề xuất chỉ sai 15 ảnh, tức giảm 28,6% số "
      "ca lỗi.")
    p("Điều quan trọng là cả hai cấu hình đều dùng chung một kiến trúc xương sống, cùng bộ dữ "
      "liệu và cùng giao thức huấn luyện. Vì vậy, toàn bộ mức cải thiện được quy cho đúng một "
      "yếu tố: việc đưa bước khoanh vùng tổn thương vào trước bước phân loại. Đây là bằng chứng "
      "thực nghiệm trực tiếp cho giả thuyết trung tâm của đề tài.")

    figure_row([
        ("outputs/cnn_full_image_baselines/efficientnet_b2_full_image/accuracy_curve.png",
         "Độ chính xác"),
        ("outputs/cnn_full_image_baselines/efficientnet_b2_full_image/loss_curve.png",
         "Hàm mất mát"),
    ], "Quá trình huấn luyện của đường cơ sở EfficientNet-B2 phân loại toàn ảnh", width=7.4)

    figure("outputs/cnn_full_image_baselines/efficientnet_b2_full_image/confusion_matrix.png",
           "Ma trận nhầm lẫn của đường cơ sở EfficientNet-B2 phân loại toàn ảnh trên 291 ảnh kiểm tra",
           width=12.0)

    h("5.4.2. So sánh với các kiến trúc phân loại tham chiếu", 3)
    p("Để kiểm chứng lựa chọn EfficientNet-B2, ba kiến trúc kinh điển được huấn luyện theo cùng "
      "giao thức và ghép với cùng bộ phát hiện YOLOv11m.")

    table("So sánh EfficientNet-B2 với ba kiến trúc tham chiếu khi ghép cùng YOLOv11m",
          ["Bộ phân loại", "Accuracy", "Macro P", "Macro R", "Macro F1", "Chênh lệch Macro F1"],
          [
              ["EfficientNet-B2 (đề xuất)", "0,9485", "0,9492", "0,9493", "0,9492", "—"],
              ["ResNet50", "0,9450", "0,9393", "0,9476", "0,9426", "−0,66 đp"],
              ["DenseNet121", "0,9416", "0,9372", "0,9473", "0,9409", "−0,83 đp"],
              ["VGG16", "0,9347", "0,9288", "0,9423", "0,9328", "−1,64 đp"],
          ],
          widths=[4.8, 2.2, 2.0, 2.0, 2.2, 3.0], font_size=10.5)

    p("EfficientNet-B2 dẫn đầu ở cả bốn chỉ số. Thứ tự xếp hạng ResNet50 > DenseNet121 > VGG16 "
      "phản ánh đúng tiến trình phát triển của các kiến trúc: VGG16, kiến trúc lâu đời nhất và "
      "không có cơ chế kết nối tắt, xếp cuối với khoảng cách 1,64 điểm phần trăm so với cấu hình "
      "đề xuất.")
    p("Cần lưu ý rằng khoảng cách giữa các kiến trúc ở mức hệ thống (0,66 tới 1,64 điểm phần "
      "trăm) hẹp hơn nhiều so với kỳ vọng dựa trên chênh lệch của chúng trên ImageNet. Nguyên "
      "nhân là kiến trúc xếp tầng đã đơn giản hóa đáng kể nhiệm vụ của bộ phân loại: khi tổn "
      "thương đã được cô lập và phóng to, ngay cả một kiến trúc cũ như VGG16 cũng đủ năng lực "
      "phân biệt. Nói cách khác, phần lớn giá trị đến từ thiết kế hệ thống chứ không phải từ "
      "việc chọn kiến trúc tối tân nhất — một kết luận có ý nghĩa thực tiễn khi cần đánh đổi với "
      "ràng buộc tài nguyên.")

    figure_row([
        ("outputs/pipeline_evaluation_baselines/comparison_baselines_accuracy.png", "Accuracy"),
        ("outputs/pipeline_evaluation_baselines/comparison_baselines_macro_f1.png", "Macro F1"),
    ], "So sánh độ chính xác và F1 trung bình vĩ mô giữa EfficientNet-B2 và ba kiến trúc tham chiếu",
        width=7.4)

    figure_row([
        ("outputs/pipeline_evaluation_baselines/yolov11_m__resnet50/confusion_matrix.png", "ResNet50"),
        ("outputs/pipeline_evaluation_baselines/yolov11_m__densenet121/confusion_matrix.png",
         "DenseNet121"),
    ], "Ma trận nhầm lẫn của hai cấu hình tham chiếu YOLOv11m + ResNet50 và YOLOv11m + DenseNet121",
        width=7.4)

    figure_row([
        ("outputs/cnn_baselines/vgg_16/test_confusion_matrix.png", "VGG16"),
        ("outputs/cnn_baselines/densenet_121/test_confusion_matrix.png", "DenseNet121"),
    ], "Ma trận nhầm lẫn ở mức vùng quan tâm của hai kiến trúc tham chiếu VGG16 và DenseNet121",
        width=7.4)

    new_page()

    # ================================================================== 5.5
    h("5.5. Phân tích chi tiết mười lăm trường hợp sai", 2)
    p("Toàn bộ mười lăm ảnh bị phân loại sai được trích xuất và phân tích riêng. Đây là phần "
      "phân tích có giá trị chẩn đoán cao nhất, vì nó chỉ ra chính xác giới hạn hiện tại của hệ "
      "thống và định hướng cải tiến.")

    table("Danh sách đầy đủ mười lăm trường hợp phân loại sai của hệ thống đề xuất",
          ["STT", "Mã ảnh", "Nhãn thực tế", "Dự đoán", "Số khung", "Ngưỡng", "Nguyên nhân"],
          [
              ["1", "BacterialSpot_00047", "BacterialSpot", "Anthracnose", "4", "0,50",
               "Bỏ phiếu có trọng số nghiêng sang lớp sai"],
              ["2", "BacterialSpot_00086", "BacterialSpot", "RingSpot", "4", "0,50",
               "Bỏ phiếu có trọng số nghiêng sang lớp sai"],
              ["3", "BacterialSpot_00004", "BacterialSpot", "RingSpot", "2", "0,50",
               "Bỏ phiếu có trọng số nghiêng sang lớp sai"],
              ["4", "BacterialSpot_00305", "BacterialSpot", "Curl", "1", "0,50",
               "Chỉ một khung, dự đoán sai quyết định toàn bộ"],
              ["5", "Anthracnose_00135", "Anthracnose", "RingSpot", "1", "0,50",
               "Chỉ một khung, dự đoán sai quyết định toàn bộ"],
              ["6", "Anthracnose_00265", "Anthracnose", "RingSpot", "3", "0,50",
               "Nhầm lẫn hình thái giữa hai lớp đốm"],
              ["7", "Anthracnose_00319", "Anthracnose", "RingSpot", "3", "0,50",
               "Nhầm lẫn hình thái giữa hai lớp đốm"],
              ["8", "RingSpot_00371", "RingSpot", "Anthracnose", "3", "0,50",
               "Nhầm lẫn hình thái giữa hai lớp đốm"],
              ["9", "RingSpot_00305", "RingSpot", "Anthracnose", "2", "0,35",
               "Phải hạ ngưỡng, khung thu được kém tin cậy"],
              ["10", "RingSpot_00313", "RingSpot", "Anthracnose", "2", "0,50",
               "Nhầm lẫn hình thái giữa hai lớp đốm"],
              ["11", "Curl_00249", "Curl", "BacterialSpot", "1", "0,35",
               "Phải hạ ngưỡng, chỉ thu được một khung"],
              ["12", "RingSpot_00235", "RingSpot", "Healthy", "0", "0,35",
               "Nhánh dự phòng: không có khung sau khi hạ ngưỡng"],
              ["13", "RingSpot_00364", "RingSpot", "Healthy", "0", "0,35",
               "Nhánh dự phòng: phân loại toàn ảnh trả về Healthy 0,983"],
              ["14", "Healthy_00089", "Healthy", "RingSpot", "1", "0,50",
               "Dương tính giả trên lá khỏe mạnh"],
              ["15", "Healthy_00228", "Healthy", "BacterialSpot", "1", "0,50",
               "Dương tính giả trên lá khỏe mạnh"],
          ],
          widths=[1.2, 3.4, 2.6, 2.4, 1.6, 1.6, 4.2], font_size=10, key="ca_sai")

    h("5.5.1. Phân nhóm nguyên nhân", 3)
    table("Phân nhóm mười lăm trường hợp sai theo nguyên nhân gốc",
          ["Nhóm nguyên nhân", "Số ca", "Tỷ lệ", "Bản chất vấn đề"],
          [
              ["Nhầm lẫn hình thái Anthracnose ↔ RingSpot", "6", "40,0%",
               "Hai bệnh có biểu hiện đốm tương tự, khác biệt tinh tế"],
              ["Ảnh chỉ có một khung duy nhất", "3", "20,0%",
               "Cơ chế bỏ phiếu mất tác dụng khi chỉ có một phiếu"],
              ["Bỏ phiếu nghiêng sai trên lớp BacterialSpot", "2", "13,3%",
               "Đốm vi khuẩn nhỏ, bộ phân loại thiếu tự tin"],
              ["Nhánh dự phòng phân loại toàn ảnh", "2", "13,3%",
               "Bộ phát hiện bỏ sót hoàn toàn tổn thương mờ"],
              ["Dương tính giả trên lá khỏe mạnh", "2", "13,3%",
               "Bộ phát hiện khoanh nhầm vết cháy nắng hoặc bóng lá"],
          ],
          widths=[5.8, 1.6, 1.8, 6.8], font_size=10.5)

    p("Nhóm nguyên nhân lớn nhất, chiếm 40% số ca sai, là nhầm lẫn giữa Anthracnose và RingSpot. "
      "Đây không phải lỗi kỹ thuật của mô hình mà là giới hạn nội tại của việc chẩn đoán bằng "
      "hình ảnh RGB đơn thuần: hai bệnh này có hình thái tổn thương chồng lấn ở giai đoạn sớm. "
      "Ngay cả chuyên gia cũng thường phải kết hợp thông tin về lịch sử canh tác, sự hiện diện "
      "của côn trùng truyền bệnh hoặc xét nghiệm huyết thanh học để phân biệt chắc chắn.")
    p("Nhóm thứ hai, chiếm 20%, là các ảnh chỉ thu được một khung duy nhất. Khi đó cơ chế bỏ "
      "phiếu có trọng số mất hoàn toàn tác dụng vì chỉ có một phiếu; kết quả mức ảnh trở nên "
      "hoàn toàn phụ thuộc vào một dự đoán mức vùng. Đây là điểm yếu có thể khắc phục được, ví "
      "dụ bằng cách khi số khung nhỏ hơn một ngưỡng thì kết hợp thêm kết quả của nhánh phân loại "
      "toàn ảnh thay vì chỉ dùng nó làm dự phòng.")
    p("Nhóm nhánh dự phòng chỉ gây ra hai ca sai, đều là ảnh RingSpot bị kết luận Healthy. Với "
      "ảnh RingSpot_00364, bộ phân loại toàn ảnh trả về Healthy với xác suất rất cao là 0,983 — "
      "cho thấy biểu hiện bệnh trên ảnh này thực sự rất mờ nhạt. Với ảnh RingSpot_00235, bộ phân "
      "loại toàn ảnh thậm chí đề xuất BacterialSpot với xác suất 0,966, nhưng logic hệ thống ưu "
      "tiên kết luận Healthy khi bộ phát hiện không tìm thấy gì. Trường hợp này gợi ý một hướng "
      "tinh chỉnh: khi nhánh toàn ảnh khẳng định một lớp bệnh với xác suất rất cao, nên tin theo "
      "nó thay vì mặc định kết luận Healthy.")
    p("Cuối cùng, hai ca dương tính giả trên lá khỏe mạnh đều bắt nguồn từ việc bộ phát hiện "
      "khoanh một vùng trên lá lành. Do lớp Healthy không được huấn luyện ở giai đoạn phát hiện, "
      "mọi khung mà nó trả về trên một lá lành đều là dương tính giả theo định nghĩa. Bổ sung "
      "ảnh lá khỏe mạnh làm mẫu nền trong quá trình huấn luyện bộ phát hiện là giải pháp trực "
      "tiếp cho vấn đề này.")

    h("5.5.2. Minh họa trực quan các ca sai", 3)
    figure_row([
        ("outputs/pipeline_evaluation_baselines/yolov11_m__resnet50/annotated_images/"
         "00011_wrong_gt_Healthy_pred_BacterialSpot.jpg", "Healthy bị dự đoán BacterialSpot"),
        ("outputs/pipeline_evaluation_baselines/yolov11_m__resnet50/annotated_images/"
         "00023_wrong_gt_BacterialSpot_pred_Curl.jpg", "BacterialSpot bị dự đoán Curl"),
    ], "Minh họa hai trường hợp phân loại sai với khung phát hiện được chú thích trên ảnh",
        width=7.0)

    note("Hai ảnh chú thích ở hình trên được sinh ra từ cấu hình tham chiếu YOLOv11m + ResNet50, "
         "vì hiện tại chỉ thư mục outputs/pipeline_evaluation_baselines/yolov11_m__resnet50/"
         "annotated_images/ có ảnh chú thích. Cần chạy lại bước xuất ảnh chú thích cho cấu hình "
         "đề xuất YOLOv11m + EfficientNet-B2 và thay thế bằng đúng mười lăm ca sai đã liệt kê ở "
         "Bảng " + ref("ca_sai") + ", để phần minh họa khớp hoàn toàn với phân tích.")

    new_page()

    # ================================================================== 5.6
    h("5.6. Đánh giá hiệu năng thời gian thực", 2)
    p("Thực nghiệm đo thông lượng được thực hiện trên cùng 291 ảnh kiểm tra, xử lý tuần tự từng "
      "ảnh một, không gộp lô các vùng cắt. Tổng cộng 1.347 khung được sinh ra, trong đó 1.339 "
      "vùng cắt hợp lệ, và có 10 lần phải hạ ngưỡng tin cậy.")

    table("Thời gian suy luận đầu-cuối của bốn cấu hình xếp tầng trên 291 ảnh",
          ["Cấu hình", "Trung bình (ms)", "Trung vị (ms)", "P90 (ms)", "P95 (ms)",
           "Nhỏ nhất (ms)", "Lớn nhất (ms)", "Thông lượng (ảnh/s)"],
          [
              ["YOLOv11m + VGG16", "470,09", "197,32", "988,32", "1.561,23", "111,28", "4.746,98", "2,127"],
              ["YOLOv11m + ResNet50", "475,40", "194,44", "1.043,13", "1.606,96", "122,40", "4.891,17", "2,103"],
              ["YOLOv11m + DenseNet121", "510,96", "212,42", "1.039,70", "1.984,42", "131,70", "5.600,19", "1,957"],
              ["YOLOv11m + EfficientNet-B2", "973,48", "683,58", "1.694,48", "2.434,80", "149,23", "6.461,14", "1,027"],
          ],
          widths=[4.4, 2.2, 2.0, 1.8, 1.8, 1.8, 1.8, 2.2], font_size=9.5)

    p("Cấu hình đề xuất có thời gian trung bình 973,48 ms mỗi ảnh, tức chậm hơn khoảng hai lần "
      "so với ba cấu hình tham chiếu. Đây là cái giá phải trả cho mức chính xác cao hơn. Trong "
      "bối cảnh ứng dụng chẩn đoán bệnh cây — nơi người dùng chụp một bức ảnh và chờ kết quả — "
      "độ trễ dưới một giây vẫn hoàn toàn chấp nhận được.")
    p("Khoảng cách rất lớn giữa trung vị (683,58 ms) và giá trị lớn nhất (6.461,14 ms) là đặc "
      "điểm đáng chú ý nhất của bảng trên. Tỷ lệ gần chín lần này phản ánh trực tiếp bản chất "
      "của kiến trúc xếp tầng: tổng thời gian tỷ lệ thuận với số vùng quan tâm được phát hiện. "
      "Một ảnh lá xoăn với một vùng duy nhất được xử lý trong khoảng 150 ms, trong khi một ảnh "
      "lá thán thư với hàng chục đốm có thể mất hơn sáu giây.")
    p("Hai hướng tối ưu trực tiếp có thể áp dụng. Thứ nhất, gộp lô các vùng cắt: thay vì gọi bộ "
      "phân loại n lần cho n vùng, gom toàn bộ thành một lô duy nhất, cách này khai thác được "
      "khả năng song song của GPU và dự kiến giảm đáng kể thời gian với các ảnh nhiều tổn "
      "thương. Thứ hai, giới hạn số vùng quan tâm tối đa, ví dụ chỉ giữ lại hai mươi khung có độ "
      "tin cậy cao nhất; do cơ chế bỏ phiếu có trọng số, các khung xếp sau hầu như không làm "
      "thay đổi kết quả.")
    p("Thời gian nạp mô hình cũng được ghi nhận: 19,05 giây cho cấu hình đề xuất so với 8,56 tới "
      "14,19 giây cho các cấu hình tham chiếu. Đây là chi phí một lần khi khởi động dịch vụ, "
      "không ảnh hưởng tới thời gian phản hồi của từng yêu cầu. Trong thiết kế dịch vụ, mô hình "
      "được nạp lười vào lần yêu cầu đầu tiên và giữ trong bộ nhớ cho các yêu cầu tiếp theo.")

    sec_5_6_hinh.build()

    # ================================================================== 5.7
    h("5.7. Thảo luận tổng hợp", 2)
    p("Tập hợp các kết quả thực nghiệm cho phép rút ra bốn kết luận có cơ sở định lượng.")
    p("Thứ nhất, giả thuyết trung tâm của đề tài được xác nhận. Việc chèn một bước khoanh vùng "
      "tổn thương trước bước phân loại mang lại mức cải thiện 2,07 điểm phần trăm về độ chính "
      "xác so với phân loại toàn ảnh, trong điều kiện mọi yếu tố khác được giữ nguyên. Mức cải "
      "thiện này tương ứng giảm 28,6% số ca lỗi.")
    p("Thứ hai, chỉ số đánh giá phải tương ứng với mục tiêu ứng dụng. Bộ phát hiện chỉ đạt "
      "mAP@0,5 bằng 0,7767 — một con số khiêm tốn nếu xét riêng — nhưng hệ thống tổng thể đạt "
      "94,85%. Sự chênh lệch này không phải nghịch lý mà là hệ quả trực tiếp của việc mAP đo "
      "chất lượng khoanh vùng từng tổn thương, trong khi mục tiêu thực sự là chẩn đoán đúng ở "
      "mức ảnh.")
    p("Thứ ba, thiết kế hệ thống quan trọng hơn việc chọn kiến trúc tối tân. Khoảng cách giữa "
      "kiến trúc tốt nhất và kém nhất trong bốn bộ phân loại khảo sát chỉ là 1,64 điểm phần "
      "trăm, nhỏ hơn mức lợi ích 2,07 điểm phần trăm thu được từ việc thay đổi kiến trúc hệ "
      "thống. Với ràng buộc tài nguyên, một tổ hợp nhẹ như YOLOv11n + EfficientNet-B2 vẫn đạt "
      "93,81%, chỉ kém cấu hình tốt nhất 1,04 điểm phần trăm.")
    p("Thứ tư, giới hạn hiện tại của hệ thống mang tính bản chất hơn là kỹ thuật. Bốn mươi phần "
      "trăm số ca sai là nhầm lẫn giữa hai bệnh có hình thái chồng lấn, loại nhầm lẫn mà bản "
      "thân chuyên gia cũng gặp phải khi chỉ quan sát ảnh RGB. Điều này gợi ý rằng để vượt qua "
      "ngưỡng 95%, cần bổ sung nguồn thông tin mới chứ không chỉ tinh chỉnh mô hình.")

    # ================================================================== 5.8
    h("5.8. Hạn chế của nghiên cứu", 2)
    for line in [
        "Dữ liệu thứ cấp: bộ dữ liệu được thu thập tại Bangladesh; giống đu đủ, điều kiện thổ "
        "nhưỡng và chủng gây bệnh tại Việt Nam có thể khác biệt, cần kiểm chứng bổ sung trên dữ "
        "liệu địa phương trước khi triển khai diện rộng.",
        "Quy mô tập đánh giá mức ảnh: 291 ảnh là số lượng đủ để rút ra kết luận có ý nghĩa nhưng "
        "chưa đủ lớn để ước lượng khoảng tin cậy hẹp; chênh lệch dưới một điểm phần trăm giữa "
        "các cấu hình cần được diễn giải thận trọng.",
        "Mất cân bằng dữ liệu: lớp Healthy chỉ có 34 ảnh trong tập đánh giá mức ảnh, nên các chỉ "
        "số của lớp này nhạy cảm với từng ca sai đơn lẻ.",
        "Chưa đánh giá trên thiết bị di động thực tế: phần triển khai Android chưa hoàn tất nên "
        "chưa có số liệu về thời gian suy luận và mức tiêu thụ pin trên thiết bị.",
        "Chưa khảo sát ảnh hưởng riêng của từng siêu tham số suy luận: các giá trị ngưỡng và hệ "
        "số mở rộng được chọn theo kinh nghiệm và giữ cố định, chưa có thực nghiệm loại trừ để "
        "định lượng đóng góp của từng thành phần.",
    ]:
        bullet(line)

    p("Những hạn chế trên không làm suy giảm giá trị của các kết luận đã rút ra, nhưng xác định "
      "rõ phạm vi áp dụng của chúng và định hướng cho các nghiên cứu tiếp theo.")

    new_page()


build()
