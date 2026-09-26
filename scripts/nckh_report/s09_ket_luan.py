"""KẾT LUẬN VÀ KIẾN NGHỊ, TÀI LIỆU THAM KHẢO, PHỤ LỤC."""
from __future__ import annotations

from docx.shared import Cm, Pt

from .core import bullet, h, h_center, new_page, note, p, table


REFERENCES = [
    "Nguyễn Minh Triết và cộng sự, “Nghiên cứu xây dựng hệ thống nhận dạng bệnh trên lá bưởi sử "
    "dụng kỹ thuật xử lý ảnh và máy vec-tơ hỗ trợ,” Kỷ yếu hội nghị khoa học, 2017.",
    "Nguyễn Đức Tấn và Thái Thuận Thương, “So sánh hiệu quả của EfficientNetB0 và MobileNetV2 "
    "trong nhận dạng 41 loài cây thuốc,” Tạp chí Khoa học và Công nghệ, 2025.",
    "Đào Văn Thiên và cộng sự, “Ứng dụng YOLOv3 và PLC trong hệ thống phân loại hoa quả tự "
    "động,” Kỷ yếu hội nghị khoa học, 2022.",
    "Nguyễn Văn Mạnh và cộng sự, “Phân loại chất lượng cà chua bằng mô hình YOLOv7,” Tạp chí "
    "Khoa học và Công nghệ, 2024.",
    "M. A. Gani, “PapayaNet: A deep learning architecture for papaya disease detection,” 2025.",
    "M. Mustofa và cộng sự, “BDPapayaLeaf: A comprehensive dataset of papaya leaf diseases with "
    "YOLOv8 and Vision Transformer evaluation,” 2024.",
    "S. Sarker và cộng sự, “BDPapayaLeaf dataset, Version 2,” Mendeley Data, 2024. [Trực tuyến]. "
    "Địa chỉ: https://data.mendeley.com",
    "P. Sharma, Y. P. S. Berwal và W. Ghai, “Performance analysis of deep learning CNN models for "
    "disease detection in plants using image segmentation,” Information Processing in "
    "Agriculture, 2020.",
    "S. Hussain và cộng sự, “Deep convolutional neural network for plant disease classification "
    "on a 20-class dataset,” 2022.",
    "J. G. A. De Moraes, M. F. L. Oliveira và G. Braga Jr., “Yolo-Papaya: A papaya fruit disease "
    "detector and classifier using CNNs and convolutional block attention modules,” Electronics, "
    "tập 12, số 10, tr. 2202, 2023.",
    "J. Terven, D.-M. Córdova-Esparza và J.-A. Romero-González, “A comprehensive review of YOLO "
    "architectures in computer vision: From YOLOv1 to YOLOv8 and YOLO-NAS,” Machine Learning and "
    "Knowledge Extraction, 2024.",
    "G. Jocher và J. Qiu, “Ultralytics YOLO11,” Ultralytics, 2024. [Trực tuyến]. Địa chỉ: "
    "https://github.com/ultralytics/ultralytics",
    "M. Tan và Q. V. Le, “EfficientNet: Rethinking model scaling for convolutional neural "
    "networks,” trong Proceedings of the 36th International Conference on Machine Learning, "
    "2019, tr. 6105–6114.",
    "K. Simonyan và A. Zisserman, “Very deep convolutional networks for large-scale image "
    "recognition,” trong International Conference on Learning Representations, 2015.",
    "K. He, X. Zhang, S. Ren và J. Sun, “Deep residual learning for image recognition,” trong "
    "IEEE Conference on Computer Vision and Pattern Recognition, 2016, tr. 770–778.",
    "G. Huang, Z. Liu, L. Van Der Maaten và K. Q. Weinberger, “Densely connected convolutional "
    "networks,” trong IEEE Conference on Computer Vision and Pattern Recognition, 2017, "
    "tr. 4700–4708.",
    "J. Hu, L. Shen và G. Sun, “Squeeze-and-excitation networks,” trong IEEE Conference on "
    "Computer Vision and Pattern Recognition, 2018, tr. 7132–7141.",
    "S. Woo, J. Park, J.-Y. Lee và I. S. Kweon, “CBAM: Convolutional block attention module,” "
    "trong European Conference on Computer Vision, 2018, tr. 3–19.",
    "J. Redmon, S. Divvala, R. Girshick và A. Farhadi, “You only look once: Unified, real-time "
    "object detection,” trong IEEE Conference on Computer Vision and Pattern Recognition, 2016, "
    "tr. 779–788.",
    "S. Ren, K. He, R. Girshick và J. Sun, “Faster R-CNN: Towards real-time object detection with "
    "region proposal networks,” IEEE Transactions on Pattern Analysis and Machine Intelligence, "
    "tập 39, số 6, tr. 1137–1149, 2017.",
    "W. Liu và cộng sự, “SSD: Single shot multibox detector,” trong European Conference on "
    "Computer Vision, 2016, tr. 21–37.",
    "T.-Y. Lin, P. Goyal, R. Girshick, K. He và P. Dollár, “Focal loss for dense object "
    "detection,” trong IEEE International Conference on Computer Vision, 2017, tr. 2980–2988.",
    "Z. Zheng và cộng sự, “Distance-IoU loss: Faster and better learning for bounding box "
    "regression,” trong AAAI Conference on Artificial Intelligence, 2020, tr. 12993–13000.",
    "X. Li và cộng sự, “Generalized focal loss: Learning qualified and distributed bounding boxes "
    "for dense object detection,” trong Advances in Neural Information Processing Systems, 2020.",
    "S. Ioffe và C. Szegedy, “Batch normalization: Accelerating deep network training by reducing "
    "internal covariate shift,” trong International Conference on Machine Learning, 2015, "
    "tr. 448–456.",
    "N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever và R. Salakhutdinov, “Dropout: A "
    "simple way to prevent neural networks from overfitting,” Journal of Machine Learning "
    "Research, tập 15, tr. 1929–1958, 2014.",
    "D. P. Kingma và J. Ba, “Adam: A method for stochastic optimization,” trong International "
    "Conference on Learning Representations, 2015.",
    "P. Micikevicius và cộng sự, “Mixed precision training,” trong International Conference on "
    "Learning Representations, 2018.",
    "J. Deng và cộng sự, “ImageNet: A large-scale hierarchical image database,” trong IEEE "
    "Conference on Computer Vision and Pattern Recognition, 2009, tr. 248–255.",
    "Y. LeCun, Y. Bengio và G. Hinton, “Deep learning,” Nature, tập 521, tr. 436–444, 2015.",
    "S. J. Pan và Q. Yang, “A survey on transfer learning,” IEEE Transactions on Knowledge and "
    "Data Engineering, tập 22, số 10, tr. 1345–1359, 2010.",
    "C. Shorten và T. M. Khoshgoftaar, “A survey on image data augmentation for deep learning,” "
    "Journal of Big Data, tập 6, số 60, 2019.",
    "S. P. Mohanty, D. P. Hughes và M. Salathé, “Using deep learning for image-based plant "
    "disease detection,” Frontiers in Plant Science, tập 7, tr. 1419, 2016.",
    "A. Kamilaris và F. X. Prenafeta-Boldú, “Deep learning in agriculture: A survey,” Computers "
    "and Electronics in Agriculture, tập 147, tr. 70–90, 2018.",
    "J. G. A. Barbedo, “Plant disease identification from individual lesions and spots using deep "
    "learning,” Biosystems Engineering, tập 180, tr. 96–107, 2019.",
    "S. Savary, L. Willocquet, S. J. Pethybridge, P. Esker, N. McRoberts và A. Nelson, “The "
    "global burden of pathogens and pests on major food crops,” Nature Ecology and Evolution, "
    "tập 3, tr. 430–439, 2019.",
    "Food and Agriculture Organization of the United Nations, “FAOSTAT statistical database,” "
    "2020. [Trực tuyến]. Địa chỉ: https://www.fao.org/faostat",
    "S. Zhang, X. Wu, Z. You và L. Zhang, “Leaf image based cucumber disease recognition using "
    "sparse representation classification,” Computers and Electronics in Agriculture, tập 134, "
    "tr. 135–141, 2014.",
    "F. Pedregosa và cộng sự, “Scikit-learn: Machine learning in Python,” Journal of Machine "
    "Learning Research, tập 12, tr. 2825–2830, 2011.",
    "M. Abadi và cộng sự, “TensorFlow: Large-scale machine learning on heterogeneous systems,” "
    "2015. [Trực tuyến]. Địa chỉ: https://www.tensorflow.org",
    "A. Paszke và cộng sự, “PyTorch: An imperative style, high-performance deep learning "
    "library,” trong Advances in Neural Information Processing Systems, 2019, tr. 8024–8035.",
    "S. Ramírez, “FastAPI framework,” 2018. [Trực tuyến]. Địa chỉ: https://fastapi.tiangolo.com",
]


def build() -> None:
    # ------------------------------------------------- KẾT LUẬN VÀ KIẾN NGHỊ
    h_center("KẾT LUẬN VÀ KIẾN NGHỊ", 1)

    h("1. Kết luận", 2)
    p("Đề tài đã hoàn thành mục tiêu tổng quát đăng ký trong thuyết minh: xây dựng được một hệ "
      "thống tự động phát hiện và phân loại bệnh hại trên lá cây đu đủ dựa trên mô hình YOLOv11 "
      "và mạng nơ-ron tích chập, có khả năng hỗ trợ nông dân nhận biết sớm dịch bệnh.")
    p("Về mặt phương pháp, đề tài đề xuất kiến trúc xếp tầng hai giai đoạn kết hợp bộ phát hiện "
      "YOLOv11m với bộ phân loại EfficientNet-B2, bổ sung cơ chế bỏ phiếu có trọng số ở mức ảnh, "
      "cơ chế hạ ngưỡng tin cậy thích nghi và nhánh dự phòng phân loại toàn ảnh. Thiết kế này "
      "giải quyết trực tiếp ba thách thức đã nhận diện: tổn thương nhỏ bị mất khi thu nhỏ ảnh, "
      "mất cân bằng dữ liệu nghiêm trọng, và tình huống bộ phát hiện không trả về khung nào.")
    p("Về mặt kết quả định lượng, hệ thống đạt độ chính xác 94,85% và F1 trung bình vĩ mô 94,92% "
      "trên 291 ảnh kiểm tra độc lập, dự đoán đúng 276 trên 291 ảnh. Kết quả này cao hơn đường "
      "cơ sở phân loại toàn ảnh cùng kiến trúc 2,07 điểm phần trăm, tương ứng giảm 28,6% số ca "
      "lỗi, và cao hơn cả ba cấu hình tham chiếu ResNet50, DenseNet121 và VGG16. Cả năm lớp đều "
      "đạt F1 trên 0,93, chứng tỏ hệ thống không hy sinh lớp thiểu số để tối ưu chỉ số tổng thể.")
    p("Về mặt sản phẩm, đề tài đã xây dựng hoàn chỉnh dịch vụ suy luận REST bằng FastAPI, giao "
      "diện web bằng Gradio, đóng gói container bằng Docker Compose và mô tả hạ tầng bằng "
      "Terraform. Toàn bộ mã nguồn, sổ tay thực nghiệm và kết quả trung gian được tổ chức đầy đủ "
      "để tái lập. Kết quả nghiên cứu đã được công bố trong một bài báo khoa học được chấp nhận "
      "đăng tại hội thảo quốc tế.")
    p("Đối chiếu với sáu mục tiêu cụ thể đã đăng ký, năm mục tiêu đã hoàn thành đầy đủ: phát "
      "triển mô hình phát hiện, xây dựng mô hình phân loại năm lớp, sử dụng bộ dữ liệu khoa học "
      "có sẵn, đạt độ chính xác cao trên các bệnh gần giống nhau, và triển khai lên nền tảng Web. "
      "Mục tiêu đánh giá khả năng thích nghi trong các điều kiện ánh sáng và góc chụp khác nhau "
      "được thực hiện gián tiếp thông qua việc sử dụng bộ dữ liệu thu thập ngoài đồng ruộng, "
      "song chưa có thực nghiệm phân tách riêng theo từng điều kiện chụp.")

    h("2. Kiến nghị và hướng phát triển", 2)
    p("Trên cơ sở phân tích lỗi ở mục 5.5 và các hạn chế đã nêu ở mục 5.8, đề tài đưa ra các "
      "kiến nghị sau.")

    h("2.1. Cải tiến kỹ thuật ngắn hạn", 3)
    for line in [
        "Kết hợp nhánh phân loại toàn ảnh vào quyết định chính thay vì chỉ dùng làm dự phòng, "
        "đặc biệt khi số khung phát hiện được nhỏ hơn ba — nhóm nguyên nhân này chiếm 20% số ca "
        "sai.",
        "Điều chỉnh logic nhánh dự phòng: khi bộ phân loại toàn ảnh khẳng định một lớp bệnh với "
        "xác suất rất cao, nên tin theo kết luận đó thay vì mặc định trả về Healthy.",
        "Bổ sung ảnh lá khỏe mạnh làm mẫu nền trong quá trình huấn luyện bộ phát hiện, nhằm giảm "
        "dương tính giả trên lá lành.",
        "Gộp lô các vùng cắt khi gọi bộ phân loại để giảm thời gian suy luận với các ảnh có nhiều "
        "tổn thương, và giới hạn số khung tối đa được đưa vào bỏ phiếu.",
        "Áp dụng cơ chế chú ý hoặc hàm mất mát tiêu điểm cho cặp lớp Anthracnose và RingSpot, "
        "nhóm chiếm 40% số ca sai.",
    ]:
        bullet(line)

    h("2.2. Mở rộng nghiên cứu trung hạn", 3)
    for line in [
        "Thu thập và gán nhãn bộ dữ liệu bệnh lá đu đủ tại Việt Nam để kiểm chứng khả năng tổng "
        "quát hóa của mô hình trên giống cây và chủng gây bệnh địa phương.",
        "Hoàn thiện ứng dụng Android với suy luận trực tiếp trên thiết bị, cho phép sử dụng ngoại "
        "tuyến tại các vùng canh tác không có kết nối ổn định.",
        "Thực hiện thực nghiệm loại trừ có hệ thống để định lượng đóng góp riêng của từng thành "
        "phần: hệ số mở rộng khung, phương pháp tổng hợp, cơ chế hạ ngưỡng và nhánh dự phòng.",
        "Mở rộng từ phân loại bệnh sang đánh giá mức độ nặng nhẹ dựa trên tỷ lệ diện tích tổn "
        "thương trên tổng diện tích lá — thông tin mà kiến trúc hiện tại đã sẵn có nhờ các khung "
        "phát hiện.",
        "Khảo sát khả năng chuyển giao kiến trúc xếp tầng sang các cây trồng khác có đặc điểm "
        "tương tự, như xoài, chuối hoặc cây có múi.",
    ]:
        bullet(line)

    h("2.3. Kiến nghị về triển khai", 3)
    p("Nhóm nghiên cứu kiến nghị Nhà trường xem xét đưa hệ thống vào sử dụng thử nghiệm tại các "
      "mô hình canh tác thực nghiệm hoặc phối hợp với trạm khuyến nông địa phương, nhằm thu thập "
      "phản hồi thực tế và bổ sung dữ liệu cho các phiên bản tiếp theo. Song song, mã nguồn và "
      "tài liệu của đề tài có thể được đưa vào kho học liệu mở phục vụ giảng dạy các học phần "
      "thị giác máy tính và học sâu.")

    new_page()

    # ------------------------------------------------------ TÀI LIỆU THAM KHẢO
    h_center("TÀI LIỆU THAM KHẢO", 1)
    for i, ref in enumerate(REFERENCES, 1):
        q = p(f"[{i}]\t{ref}", indent=False)
        q.paragraph_format.left_indent = Cm(1.0)
        q.paragraph_format.first_line_indent = Cm(-1.0)
        q.paragraph_format.space_after = Pt(5)
        q.paragraph_format.line_spacing = 1.25

    new_page()

    # --------------------------------------------------------------- PHỤ LỤC
    h_center("PHỤ LỤC", 1)

    h("Phụ lục A. Hồ sơ minh chứng sản phẩm", 2)
    p("Theo yêu cầu của Phòng Khoa học Công nghệ, hồ sơ minh chứng sản phẩm bài báo phải bao gồm "
      "đầy đủ tên tạp chí hoặc hội nghị, giấy chấp nhận đăng, toàn văn bài báo hoặc bài báo đã "
      "được đăng, và đường dẫn tới bài báo. Các minh chứng được đóng kèm theo thứ tự dưới đây.")
    for line in [
        "A.1. Trang thông tin hội nghị và mã số ISBN/ISSN.",
        "A.2. Giấy chấp nhận đăng bài báo.",
        "A.3. Toàn văn bài báo (mã số GTSD2026-148), trong đó phần lời cảm ơn ghi rõ đề tài "
        "Grant No. SV2026-08.",
        "A.4. Đường dẫn tới bài báo đã đăng (nếu đã xuất bản tại thời điểm nộp).",
        "A.5. Bản sao Thuyết minh đề tài (BM02) đã được phê duyệt.",
        "A.6. Bản sao Hợp đồng thực hiện đề tài đã ký.",
        "A.7. Standee/Poster khổ A3.",
        "A.8. Tóm tắt đề tài.",
    ]:
        bullet(line)
    note("Chuẩn bị và đóng kèm đầy đủ các mục A.1 đến A.8 vào cuối cuốn báo cáo trước khi nộp. "
         "Hạn nộp bản cứng về Phòng KHCN là từ ngày 25/9 đến hết ngày 01/10/2026, đồng thời đăng "
         "ký nghiệm thu và nộp file mềm qua biểu mẫu trực tuyến của Phòng KHCN.")

    h("Phụ lục B. Cấu hình huấn luyện đầy đủ", 2)

    p("B.1. Cấu hình bộ phát hiện YOLOv11m", bold_lead="B.1.", indent=False)
    table("Cấu hình đầy đủ của bộ phát hiện YOLOv11m (trích từ tệp args.yaml)",
          ["Tham số", "Giá trị"],
          [
              ["model", "yolo11m.pt"],
              ["epochs", "80"],
              ["patience", "20"],
              ["batch", "8"],
              ["imgsz", "832"],
              ["device", "0 (GPU)"],
              ["workers", "2"],
              ["seed", "42"],
              ["deterministic", "true"],
              ["cos_lr", "true"],
              ["close_mosaic", "10"],
              ["amp", "true"],
              ["optimizer", "auto"],
              ["iou", "0,7"],
              ["max_det", "300"],
              ["pretrained", "true"],
              ["plots", "true"],
          ],
          widths=[6.0, 6.0])

    p("B.2. Cấu hình bộ phân loại EfficientNet", bold_lead="B.2.", indent=False)
    table("Cấu hình đầy đủ của các bộ phân loại EfficientNet",
          ["Tham số", "Giá trị"],
          [
              ["SEED", "42"],
              ["Chính sách độ chính xác", "mixed_float16"],
              ["Thứ tự lớp", "Anthracnose, BacterialSpot, Curl, Healthy, RingSpot"],
              ["B0 — kích thước ảnh / lô / số tầng mở khóa / dropout", "224 / 48 / 40 / 0,30"],
              ["B1 — kích thước ảnh / lô / số tầng mở khóa / dropout", "240 / 40 / 50 / 0,30"],
              ["B2 — kích thước ảnh / lô / số tầng mở khóa / dropout", "260 / 32 / 60 / 0,35"],
              ["STAGE1_EPOCHS / STAGE2_EPOCHS", "8 / 20"],
              ["STAGE1_LR / STAGE2_LR", "1 × 10⁻³ / 5 × 10⁻⁵"],
              ["EARLY_STOPPING_PATIENCE", "6"],
              ["REDUCE_LR_PATIENCE / FACTOR / MIN_LR", "3 / 0,3 / 1 × 10⁻⁶"],
              ["Bộ tối ưu", "Adam"],
              ["Tăng cường dữ liệu",
               "RandomFlip(horizontal), RandomRotation(0,05), RandomZoom(0,10), RandomContrast(0,10)"],
              ["Trọng số lớp", "total_train / (NUM_CLASSES × train_counts[cls])"],
          ],
          widths=[6.4, 8.4], font_size=10.5)

    h("Phụ lục C. Danh mục tệp kết quả", 2)
    p("Mọi số liệu trình bày trong báo cáo đều được trích xuất trực tiếp từ các tệp kết quả lưu "
      "trong thư mục outputs của kho mã nguồn. Bảng dưới đây liệt kê các tệp chính, phục vụ việc "
      "kiểm chứng và tái lập.")
    table("Danh mục tệp kết quả sử dụng trong báo cáo",
          ["Nội dung", "Đường dẫn tệp"],
          [
              ["Kiểm tra toàn vẹn chia tập dữ liệu",
               "outputs/yolo/reports/dataset_split_sanity.csv"],
              ["So sánh ba biến thể YOLOv11", "outputs/yolo/reports/final_yolo_comparison.csv"],
              ["Chỉ số theo lớp của YOLOv11m",
               "outputs/yolo/test_evaluations/yolov11_m/per_class_metrics_test.csv"],
              ["Ma trận nhầm lẫn của YOLOv11m",
               "outputs/yolo/test_evaluations/yolov11_m/confusion_matrix_test.csv"],
              ["Cấu hình huấn luyện YOLOv11m", "outputs/yolo/yolov11_m/args.yaml"],
              ["Nhật ký huấn luyện YOLOv11m theo từng vòng lặp",
               "outputs/yolo/yolov11_m/results.csv"],
              ["Phân bố vùng quan tâm theo lớp", "outputs/cnn/efficientnet_b2/dataset_count.csv"],
              ["Tổng hợp kết quả EfficientNet-B2", "outputs/cnn/efficientnet_b2/test_summary.json"],
              ["Báo cáo phân loại EfficientNet-B2",
               "outputs/cnn/efficientnet_b2/test_classification_report.csv"],
              ["Lịch sử huấn luyện hai pha",
               "outputs/cnn/efficientnet_b2/history_stage1.csv; history_stage2.csv"],
              ["So sánh chín tổ hợp xếp tầng",
               "outputs/pipeline_evaluation/all_pipeline_summary_sorted.csv"],
              ["Kết quả chi tiết cấu hình đề xuất",
               "outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/classification_report.csv"],
              ["Danh sách mười lăm ca sai",
               "outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/error_cases.csv"],
              ["So sánh các cấu hình tham chiếu",
               "outputs/pipeline_evaluation_baselines/all_pipeline_summary_baselines_sorted.csv"],
              ["Đường cơ sở phân loại toàn ảnh",
               "outputs/cnn_full_image_baselines/efficientnet_b2_full_image/test_summary.json"],
              ["Đo thông lượng bốn cấu hình",
               "outputs/Performance_Benchmark/model_throughput_20260703_155451.csv"],
          ],
          widths=[5.4, 9.4], font_size=10.5)

    h("Phụ lục D. Danh mục nội dung cần bổ sung", 2)
    p("Bảng dưới đây tập hợp toàn bộ các mục được đánh dấu [CẦN BỔ SUNG] trong báo cáo, phục vụ "
      "việc rà soát trước khi in nộp. Sau khi hoàn tất, xóa toàn bộ các ghi chú màu đỏ trong "
      "thân báo cáo và xóa luôn phụ lục này.")
    table("Danh mục nội dung cần bổ sung trước khi nộp",
          ["STT", "Vị trí", "Nội dung cần bổ sung", "Mức ưu tiên"],
          [
              ["1", "Trang bìa phụ", "Lớp, dân tộc, năm thứ, nhóm ngành khoa học theo hồ sơ", "Cao"],
              ["2", "Thông tin kết quả nghiên cứu, mục 6",
               "Tên hội nghị, ISBN/ISSN, ngày chấp nhận đăng, đường dẫn bài báo", "Cao"],
              ["3", "Mục 3.1", "Sơ đồ khối chi tiết của kiến trúc xếp tầng (nếu có)", "Trung bình"],
              ["4", "Mục 5.5.2",
               "Ảnh chú thích mười lăm ca sai của cấu hình YOLOv11m + EfficientNet-B2 "
               "(chạy notebooks/09_export_annotated_error_cases_colab.ipynb)", "Trung bình"],
              ["5", "Mục 6.2.2", "Kết quả JSON thực tế từ một lần gọi API", "Thấp"],
              ["6", "Mục 6.3", "Ảnh chụp màn hình giao diện web và trang tài liệu API", "Cao"],
              ["7", "Mục 6.5", "Kết quả triển khai Android (nếu hoàn tất trước nghiệm thu)", "Thấp"],
              ["8", "Phụ lục A", "Toàn bộ hồ sơ minh chứng A.1 đến A.8", "Cao"],
              ["9", "Toàn báo cáo",
               "Cập nhật mục lục, danh mục bảng và danh mục hình (Ctrl+A rồi F9 trong Word)", "Cao"],
          ],
          widths=[1.2, 3.6, 7.6, 2.4], font_size=10.5)


build()
