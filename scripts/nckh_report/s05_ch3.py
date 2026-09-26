"""CHƯƠNG 3. PHƯƠNG PHÁP ĐỀ XUẤT."""
from __future__ import annotations

from .core import bullet, code_block, figure, formula, h, h_center, new_page, note, p, table


def build() -> None:
    h_center("CHƯƠNG 3. PHƯƠNG PHÁP ĐỀ XUẤT", 1)

    # ------------------------------------------------------------------ 3.1
    h("3.1. Kiến trúc tổng thể của hệ thống xếp tầng", 2)
    p("Hệ thống đề xuất gồm hai mô hình học sâu nối tiếp nhau và một khối logic tổng hợp. Luồng "
      "xử lý một ảnh đầu vào diễn ra theo sáu bước:")
    for i, line in enumerate([
        "Chuẩn hóa ảnh đầu vào về không gian màu RGB và đưa về kích thước 832 điểm ảnh cho cạnh "
        "dài nhất, giữ nguyên tỷ lệ khung hình.",
        "Bộ phát hiện YOLOv11m suy luận trên ảnh và trả về danh sách khung bao quanh các vùng "
        "nghi ngờ tổn thương kèm nhãn sơ bộ và độ tin cậy.",
        "Nếu không có khung nào vượt ngưỡng tin cậy hiện hành, hệ thống hạ ngưỡng theo bước cố "
        "định và suy luận lại; nếu vẫn không có khung nào, chuyển sang nhánh dự phòng phân loại "
        "toàn ảnh.",
        "Mỗi khung được mở rộng theo tỷ lệ cố định rồi cắt ra khỏi ảnh gốc, tạo thành một vùng "
        "quan tâm ở độ phân giải gốc.",
        "Bộ phân loại EfficientNet-B2 dự đoán phân phối xác suất trên năm lớp cho từng vùng quan "
        "tâm.",
        "Khối tổng hợp gộp các dự đoán mức vùng thành một nhãn duy nhất ở mức ảnh bằng cơ chế bỏ "
        "phiếu có trọng số.",
    ], 1):
        bullet(f"Bước {i}: {line}")

    figure("readme/workflow.png",
           "Kiến trúc xếp tầng hai giai đoạn YOLOv11m → EfficientNet-B2 với khối tổng hợp phiếu "
           "bầu có trọng số và nhánh dự phòng phân loại toàn ảnh", width=15.0)
    note("Nếu có sơ đồ khối chi tiết hơn được vẽ riêng cho kiến trúc xếp tầng (phân biệt rõ nhánh "
         "chính và nhánh dự phòng), hãy thay thế hình trên bằng sơ đồ đó để minh họa trực quan hơn.")

    p("Điểm mấu chốt của thiết kế là sự phân công nhiệm vụ rõ ràng. Bộ phát hiện chịu trách "
      "nhiệm định vị, tức trả lời câu hỏi vùng nào đáng quan tâm; nó không cần phân biệt chính "
      "xác loại bệnh. Bộ phân loại chịu trách nhiệm định danh trên vùng đã được cô lập, nơi tổn "
      "thương chiếm phần lớn diện tích khung hình. Sự phân công này giải thích vì sao hệ thống "
      "tổng thể đạt độ chính xác 94,85% ở mức ảnh mặc dù bộ phát hiện chỉ đạt mAP@0,5 bằng "
      "0,7767: các sai sót về nhãn ở giai đoạn phát hiện được giai đoạn phân loại sửa chữa, và "
      "cơ chế bỏ phiếu làm loãng ảnh hưởng của những khung nhiễu đơn lẻ.")

    # ------------------------------------------------------------------ 3.2
    h("3.2. Giai đoạn một: phát hiện vùng tổn thương bằng YOLOv11m", 2)
    p("Bộ phát hiện được huấn luyện trên bốn lớp bệnh: Anthracnose, BacterialSpot, Curl và "
      "RingSpot. Lớp Healthy có chủ đích không được đưa vào giai đoạn này, bởi lá khỏe mạnh theo "
      "định nghĩa không chứa tổn thương nào để khoanh vùng. Trường hợp lá khỏe mạnh được xử lý ở "
      "mức logic hệ thống thông qua nhánh dự phòng trình bày ở mục 3.6.")
    p("Cấu hình huấn luyện được lựa chọn nhằm cân bằng giữa khả năng phát hiện tổn thương nhỏ và "
      "chi phí tính toán. Kích thước ảnh đầu vào 832 điểm ảnh, lớn hơn mức mặc định 640, được "
      "chọn sau khi khảo sát cho thấy các đốm đốm vi khuẩn có đường kính chỉ vài điểm ảnh khi "
      "ảnh bị thu nhỏ quá mức.")

    table("Cấu hình huấn luyện bộ phát hiện YOLOv11m",
          ["Tham số", "Giá trị", "Lý do lựa chọn"],
          [
              ["Trọng số khởi tạo", "yolo11m.pt (tiền huấn luyện COCO)",
               "Tận dụng học chuyển giao, rút ngắn thời gian hội tụ"],
              ["Số epoch tối đa", "80", "Đủ để hội tụ với quy mô dữ liệu hiện có"],
              ["Kiên nhẫn dừng sớm", "20", "Tránh quá khớp khi chỉ số xác thực bão hòa"],
              ["Kích thước lô", "8", "Giới hạn bởi bộ nhớ GPU ở độ phân giải 832"],
              ["Kích thước ảnh", "832 × 832", "Bảo toàn chi tiết tổn thương kích thước nhỏ"],
              ["Bộ tối ưu", "auto (Ultralytics tự chọn)", "Theo khuyến nghị của thư viện"],
              ["Lịch tốc độ học", "Cosine (cos_lr = true)", "Giảm mượt tốc độ học về cuối quá trình"],
              ["Ngưỡng IoU cho NMS", "0,70", "Giữ lại các tổn thương liền kề nhưng tách biệt"],
              ["Số khung tối đa mỗi ảnh", "300", "Đáp ứng ảnh thán thư có hàng chục tổn thương"],
              ["Tắt mosaic", "10 epoch cuối", "Ổn định phân bố dữ liệu ở giai đoạn tinh chỉnh"],
              ["Độ chính xác hỗn hợp", "Bật (amp = true)", "Tăng tốc huấn luyện, giảm bộ nhớ"],
              ["Hạt giống ngẫu nhiên", "42, deterministic = true", "Bảo đảm khả năng tái lập kết quả"],
          ],
          widths=[4.4, 4.8, 6.8], font_size=10.5)

    # ------------------------------------------------------------------ 3.3
    h("3.3. Trích xuất vùng quan tâm", 2)
    p("Khung bao do bộ phát hiện trả về thường bám sát rìa tổn thương. Tuy nhiên, thông tin về "
      "vùng mô lá bao quanh tổn thương lại có giá trị chẩn đoán đáng kể: quầng vàng bao quanh "
      "đốm là dấu hiệu đặc trưng của đốm vi khuẩn, còn vòng đồng tâm mở rộng là dấu hiệu của đốm "
      "vòng. Vì vậy, mỗi khung được mở rộng một tỷ lệ cố định trước khi cắt.")
    p("Gọi khung gốc có tọa độ (x₁, y₁, x₂, y₂), chiều rộng w = x₂ − x₁ và chiều cao h = y₂ − y₁. "
      "Với hệ số mở rộng ρ = 0,10, khung mở rộng được tính bởi:")
    formula("x₁' = max(0, x₁ − ρ·w/2);   y₁' = max(0, y₁ − ρ·h/2)", "3.1")
    formula("x₂' = min(W, x₂ + ρ·w/2);   y₂' = min(H, y₂ + ρ·h/2)", "3.2")
    p("trong đó W và H là kích thước ảnh gốc. Các phép lấy cực đại và cực tiểu bảo đảm khung mở "
      "rộng không vượt ra ngoài biên ảnh. Những vùng cắt có cạnh nhỏ hơn 8 điểm ảnh bị loại bỏ "
      "vì sau khi nội suy lên 260×260 chúng chỉ chứa nhiễu. Trong thực nghiệm đo thông lượng "
      "trên 291 ảnh, tổng số 1.347 khung được sinh ra và 1.339 vùng cắt hợp lệ được giữ lại, "
      "tương ứng tỷ lệ loại bỏ khoảng 0,6%.")

    # ------------------------------------------------------------------ 3.4
    h("3.4. Giai đoạn hai: phân loại vùng quan tâm bằng EfficientNet-B2", 2)
    p("Bộ phân loại nhận đầu vào là vùng quan tâm đã được nội suy về kích thước 260×260 điểm "
      "ảnh, phù hợp với độ phân giải thiết kế của EfficientNet-B2. Khác với bộ phát hiện, bộ "
      "phân loại làm việc trên đủ năm lớp, bao gồm cả Healthy; các mẫu Healthy được lấy từ các "
      "vùng lá không tổn thương trong bộ dữ liệu gốc.")
    p("Kiến trúc phần đầu phân loại gồm một tầng gộp trung bình toàn cục để nén bản đồ đặc trưng "
      "của xương sống thành một vec-tơ, một tầng dropout với tỷ lệ 0,35 và một tầng kết nối đầy "
      "đủ năm nơ-ron với hàm softmax. Toàn bộ quá trình huấn luyện sử dụng chính sách độ chính "
      "xác hỗn hợp mixed_float16 để tăng tốc trên GPU, với tầng đầu ra được ép về float32 nhằm "
      "bảo đảm ổn định số học của hàm softmax.")

    h("3.4.1. Chiến lược huấn luyện hai pha", 3)
    table("Cấu hình hai pha huấn luyện bộ phân loại EfficientNet-B2",
          ["Hạng mục", "Pha 1 – Đóng băng xương sống", "Pha 2 – Tinh chỉnh"],
          [
              ["Trạng thái xương sống", "Đóng băng hoàn toàn", "Mở khóa 60 tầng cuối"],
              ["Số epoch dự kiến", "8", "20"],
              ["Số epoch thực tế đã chạy", "8", "14 (dừng sớm)"],
              ["Tốc độ học", "1 × 10⁻³", "5 × 10⁻⁵"],
              ["Bộ tối ưu", "Adam", "Adam"],
              ["Hàm mất mát", "Categorical cross-entropy có trọng số lớp",
               "Categorical cross-entropy có trọng số lớp"],
              ["Dừng sớm", "Không áp dụng", "Kiên nhẫn 6 epoch theo val_loss"],
              ["Giảm tốc độ học", "Không áp dụng",
               "Hệ số 0,3 sau 3 epoch không cải thiện, sàn 1 × 10⁻⁶"],
          ],
          widths=[4.4, 5.8, 5.8], font_size=10.5)

    p("Việc pha hai dừng sớm ở epoch thứ mười bốn thay vì chạy đủ hai mươi epoch cho thấy mô "
      "hình đã đạt điểm tối ưu trên tập xác thực và bắt đầu có dấu hiệu quá khớp. Cơ chế dừng "
      "sớm khôi phục lại bộ trọng số tốt nhất, nhờ đó tránh được suy giảm hiệu năng trên tập "
      "kiểm tra.")

    h("3.4.2. Xử lý mất cân bằng lớp", 3)
    p("Phân bố số lượng vùng quan tâm giữa các lớp rất lệch: lớp Anthracnose có 4.416 mẫu huấn "
      "luyện trong khi lớp Healthy chỉ có 160 mẫu, chênh lệch gần hai mươi tám lần. Nếu huấn "
      "luyện trực tiếp, mô hình sẽ có xu hướng dự đoán thiên về lớp đa số. Đề tài áp dụng trọng "
      "số lớp theo công thức (2.3), giá trị cụ thể được trình bày trong Chương 4.")

    h("3.4.3. Tăng cường dữ liệu", 3)
    p("Khối tăng cường dữ liệu được đặt ngay sau tầng đầu vào và chỉ hoạt động ở chế độ huấn "
      "luyện. Bốn phép biến đổi được sử dụng gồm: lật ngang ngẫu nhiên, xoay ngẫu nhiên biên độ "
      "0,05 vòng tương đương khoảng ±18 độ, thu phóng ngẫu nhiên biên độ 0,10 và thay đổi độ "
      "tương phản ngẫu nhiên biên độ 0,10. Biên độ được giữ nhỏ có chủ đích: các phép biến đổi "
      "quá mạnh có thể làm biến dạng cấu trúc vòng đồng tâm của đốm vòng hoặc làm mất quầng vàng "
      "của đốm vi khuẩn, tức là phá hủy chính đặc trưng cần học.")

    # ------------------------------------------------------------------ 3.5
    h("3.5. Tổng hợp kết quả mức ảnh bằng bỏ phiếu có trọng số", 2)
    p("Sau giai đoạn hai, một ảnh có n vùng quan tâm sẽ có n phân phối xác suất trên năm lớp. "
      "Vấn đề đặt ra là quy các dự đoán cục bộ này về một nhãn duy nhất cho toàn ảnh.")
    p("Cách đơn giản nhất là bỏ phiếu theo đa số, tức chọn lớp xuất hiện nhiều nhất. Tuy nhiên "
      "cách này coi mọi vùng quan tâm là ngang nhau, kể cả những vùng mà cả bộ phát hiện lẫn bộ "
      "phân loại đều không chắc chắn. Đề tài sử dụng cơ chế bỏ phiếu có trọng số: mỗi vùng đóng "
      "góp một phiếu có độ lớn bằng tích của độ tin cậy phát hiện và xác suất phân loại.")
    p("Gọi B là tập vùng quan tâm của ảnh, c_i là độ tin cậy của khung thứ i do bộ phát hiện trả "
      "về, và p_i(k) là xác suất mà bộ phân loại gán cho lớp k trên vùng thứ i. Điểm số của lớp "
      "k ở mức ảnh được tính bởi:")
    formula("S(k) = Σ(i ∈ B) c_i · p_i(k)", "3.3")
    p("và nhãn cuối cùng là lớp có điểm số cao nhất:")
    formula("ŷ = argmax(k ∈ {1..5}) S(k)", "3.4")
    p("Cơ chế này có ba ưu điểm. Thứ nhất, một khung có độ tin cậy phát hiện thấp sẽ đóng góp ít "
      "vào quyết định cuối cùng, ngay cả khi bộ phân loại gán cho nó xác suất cao. Thứ hai, một "
      "vùng mà bộ phân loại phân vân giữa hai lớp sẽ phân tán phiếu của mình thay vì áp đặt một "
      "lựa chọn cứng. Thứ ba, khi một ảnh có nhiều tổn thương cùng loại, các phiếu cộng dồn tạo "
      "thành tín hiệu mạnh, phù hợp với trực giác chẩn đoán của chuyên gia.")

    # ------------------------------------------------------------------ 3.6
    h("3.6. Ngưỡng tin cậy thích nghi và nhánh dự phòng", 2)
    p("Một hệ thống chỉ dựa vào bộ phát hiện sẽ thất bại hoàn toàn khi không có khung nào được "
      "trả về. Tình huống này xảy ra trong hai trường hợp trái ngược: lá thực sự khỏe mạnh nên "
      "không có gì để phát hiện, hoặc lá có bệnh nhưng biểu hiện quá mờ nhạt so với ngưỡng tin "
      "cậy đang dùng. Hai trường hợp này đòi hỏi hai cách xử lý khác nhau.")
    p("Giải pháp của đề tài gồm hai lớp phòng vệ. Lớp thứ nhất là hạ ngưỡng tin cậy theo từng "
      "bước: hệ thống bắt đầu ở ngưỡng 0,50; nếu không thu được khung nào, ngưỡng giảm 0,05 và "
      "suy luận lại, lặp cho tới sàn 0,35. Chuỗi ngưỡng thử nghiệm do đó là 0,50 → 0,45 → 0,40 → "
      "0,35. Cách làm này giữ độ chính xác cao cho đa số ảnh trong khi vẫn cho cơ hội với các "
      "ảnh khó.")
    p("Lớp thứ hai là nhánh dự phòng phân loại toàn ảnh. Khi đã hạ tới sàn mà vẫn không có khung "
      "nào, toàn bộ ảnh được đưa trực tiếp vào bộ phân loại EfficientNet-B2. Nếu lớp có xác suất "
      "cao nhất là Healthy, hoặc là một lớp bệnh nhưng với xác suất dưới ngưỡng 0,50, hệ thống "
      "kết luận Healthy — lập luận ở đây là cả bộ phát hiện lẫn bộ phân loại đều không tìm thấy "
      "bằng chứng bệnh đủ thuyết phục. Ngược lại, nếu bộ phân loại khẳng định một lớp bệnh với "
      "xác suất vượt ngưỡng, hệ thống chấp nhận kết luận đó.")
    p("Thiết kế này giải thích vì sao lớp Healthy đạt Precision 0,9412 và Recall 0,9412 dù không "
      "hề được huấn luyện trong giai đoạn phát hiện. Phân tích lỗi ở Chương 5 cho thấy trong "
      "mười lăm ca sai, chỉ có hai ca phát sinh từ nhánh dự phòng này.")

    # ------------------------------------------------------------------ 3.7
    h("3.7. Mô tả thuật toán", 2)
    p("Toàn bộ logic suy luận được tóm tắt trong mã giả dưới đây, tương ứng trực tiếp với hàm "
      "run_hybrid_on_image trong mã nguồn dịch vụ.")
    code_block([
        "Input : anh I; nguong conf_start=0.50, conf_min=0.35, conf_step=0.05;",
        "        he so mo rong rho=0.10; nguong benh toan anh tau=0.50",
        "Output: nhan lop y, do tin cay, danh sach khung",
        "",
        "1  boxes <- []",
        "2  conf  <- conf_start",
        "3  while conf >= conf_min and boxes is empty do",
        "4      boxes <- YOLOv11m(I, imgsz=832, conf=conf, iou=0.70)",
        "5      conf  <- conf - conf_step",
        "6  end while",
        "",
        "7  if boxes is empty then                  // nhanh du phong",
        "8      p_full <- EfficientNetB2(resize(I, 260))",
        "9      k      <- argmax(p_full)",
        "10     if k = Healthy or p_full[k] < tau then return Healthy",
        "11     else return k",
        "12 end if",
        "",
        "13 S <- zeros(5)                           // nhanh chinh",
        "14 for each box b in boxes do",
        "15     b' <- expand(b, rho); clip b' vao bien anh",
        "16     if min(width(b'), height(b')) < 8 then continue",
        "17     roi <- resize(crop(I, b'), 260)",
        "18     p   <- EfficientNetB2(roi)",
        "19     S   <- S + confidence(b) * p        // bo phieu co trong so",
        "20 end for",
        "21 return argmax(S), normalize(S), boxes",
    ])

    # ------------------------------------------------------------------ 3.8
    h("3.8. Tổng hợp siêu tham số suy luận", 2)
    p("Bảng dưới đây liệt kê đầy đủ các siêu tham số của giai đoạn suy luận. Tất cả đều được "
      "hiện thực dưới dạng biến môi trường trong dịch vụ FastAPI, cho phép điều chỉnh mà không "
      "phải sửa mã nguồn.")

    table("Siêu tham số suy luận của hệ thống xếp tầng",
          ["Tham số", "Biến môi trường", "Giá trị", "Vai trò"],
          [
              ["Kích thước ảnh phát hiện", "YOLO_IMGSZ", "832", "Độ phân giải đầu vào của YOLOv11m"],
              ["Ngưỡng IoU cho NMS", "YOLO_IOU", "0,70", "Kiểm soát loại bỏ khung trùng lặp"],
              ["Ngưỡng tin cậy khởi đầu", "YOLO_CONF_START", "0,50", "Ngưỡng dùng cho lần suy luận đầu"],
              ["Ngưỡng tin cậy sàn", "YOLO_CONF_MIN", "0,35", "Giới hạn dưới khi hạ ngưỡng"],
              ["Bước hạ ngưỡng", "YOLO_CONF_STEP", "0,05", "Độ giảm mỗi lần thử lại"],
              ["Ngưỡng bệnh toàn ảnh", "FULL_CNN_DISEASE_MIN_PROB", "0,50",
               "Ngưỡng chấp nhận kết luận bệnh ở nhánh dự phòng"],
              ["Hệ số mở rộng khung", "BBOX_EXPAND_RATIO", "0,10", "Bổ sung ngữ cảnh quanh tổn thương"],
              ["Kích thước cắt tối thiểu", "MIN_CROP_SIZE", "8", "Loại bỏ vùng quá nhỏ"],
              ["Kích thước ảnh phân loại", "CNN_IMG_SIZE", "260", "Độ phân giải đầu vào EfficientNet-B2"],
              ["Phương pháp tổng hợp", "AGG_METHOD", "weighted", "Bỏ phiếu có trọng số theo công thức (3.3)"],
          ],
          widths=[4.4, 4.6, 2.2, 4.8], font_size=10.5, key="sieu_tham_so")

    p("Các giá trị trên được cố định cho mọi thực nghiệm trong Chương 5, bảo đảm tính nhất quán "
      "khi so sánh giữa các tổ hợp mô hình khác nhau.")

    new_page()


build()
