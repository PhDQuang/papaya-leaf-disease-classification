"""CHƯƠNG 6. CHƯƠNG TRÌNH ỨNG DỤNG VÀ KHẢ NĂNG TRIỂN KHAI."""
from __future__ import annotations

from .core import bullet, code_block, h, h_center, new_page, note, p, ref, table


def build() -> None:
    h_center("CHƯƠNG 6. CHƯƠNG TRÌNH ỨNG DỤNG VÀ KHẢ NĂNG TRIỂN KHAI", 1)

    # ------------------------------------------------------------------ 6.1
    h("6.1. Kiến trúc phần mềm tổng thể", 2)
    p("Sản phẩm phần mềm của đề tài được thiết kế theo kiến trúc phân tầng, tách bạch rõ giữa "
      "tầng mô hình, tầng dịch vụ và tầng giao diện. Cách tổ chức này cho phép mỗi tầng phát "
      "triển và kiểm thử độc lập, đồng thời hỗ trợ nhiều loại giao diện người dùng khác nhau "
      "trên cùng một lõi suy luận.")

    table("Các thành phần phần mềm của hệ thống",
          ["Thành phần", "Thư mục mã nguồn", "Công nghệ", "Chức năng"],
          [
              ["Lõi suy luận", "api/src/", "PyTorch, TensorFlow",
               "Nạp mô hình, thực thi logic xếp tầng"],
              ["Dịch vụ REST", "api/", "FastAPI, Uvicorn",
               "Cung cấp điểm cuối HTTP cho các máy khách"],
              ["Giao diện web", "web/", "Gradio",
               "Giao diện tải ảnh và hiển thị kết quả cho người dùng cuối"],
              ["Điều phối container", "docker-compose.yml", "Docker Compose",
               "Khởi chạy đồng thời dịch vụ và giao diện"],
              ["Hạ tầng", "infra/", "Terraform",
               "Mô tả hạ tầng triển khai dưới dạng mã"],
              ["Ứng dụng di động", "AndroidApp/", "Android, ncnn",
               "Suy luận trực tiếp trên thiết bị (đang phát triển)"],
              ["Sổ tay thực nghiệm", "notebooks/", "Jupyter",
               "Tái lập toàn bộ quy trình huấn luyện và đánh giá"],
          ],
          widths=[3.4, 3.6, 3.2, 5.8], font_size=10.5)

    # ------------------------------------------------------------------ 6.2
    h("6.2. Dịch vụ suy luận FastAPI", 2)
    p("Dịch vụ REST là thành phần trung tâm, hiện thực đúng thuật toán đã mô tả ở mục 3.7. Dịch "
      "vụ cung cấp bốn điểm cuối.")

    table("Các điểm cuối của dịch vụ REST",
          ["Điểm cuối", "Phương thức", "Đầu vào", "Đầu ra"],
          [
              ["/", "GET", "—", "Thông tin cơ bản về dịch vụ"],
              ["/health", "GET", "—", "Trạng thái hoạt động, phục vụ giám sát"],
              ["/models", "GET", "—", "Thông tin về mô hình đang nạp và cấu hình suy luận"],
              ["/predict", "POST", "Tệp ảnh (multipart/form-data)",
               "Nhãn dự đoán, độ tin cậy, phân phối xác suất năm lớp, danh sách khung phát hiện"],
          ],
          widths=[2.6, 2.4, 5.0, 6.0], font_size=10.5)

    p("Toàn bộ siêu tham số suy luận được hiện thực dưới dạng biến môi trường (xem lại Bảng "
      + ref("sieu_tham_so") + "), "
      "cho phép điều chỉnh hành vi hệ thống mà không phải biên dịch lại hay sửa mã nguồn. Đây là "
      "thực hành quan trọng khi triển khai: người vận hành có thể nới lỏng ngưỡng tin cậy trong "
      "mùa dịch để tăng độ nhạy, hoặc siết chặt lại để giảm cảnh báo nhầm.")

    h("6.2.1. Cơ chế quản lý mô hình", 3)
    p("Hai tệp trọng số của hệ thống có dung lượng lớn nên không được đưa vào kho mã nguồn. Dịch "
      "vụ hiện thực cơ chế tự động tải mô hình từ kho lưu trữ đám mây trong lần khởi động đầu "
      "tiên và lưu vào một ổ đĩa gắn ngoài. Nhờ vậy, các lần khởi động lại container sau đó "
      "không phải tải lại.")
    p("Mô hình được nạp theo cơ chế lười: thay vì nạp ngay khi dịch vụ khởi động, mô hình chỉ "
      "được nạp vào lần đầu tiên có yêu cầu dự đoán. Thiết kế này rút ngắn thời gian khởi động "
      "container xuống còn vài giây, giúp dịch vụ vượt qua các bước kiểm tra sức khỏe của nền "
      "tảng điều phối trước khi phải gánh chi phí nạp mô hình khoảng mười chín giây.")

    h("6.2.2. Ví dụ sử dụng", 3)
    code_block([
        "# Gui mot anh la den dich vu va nhan ket qua chan doan",
        "curl -X POST http://localhost:8000/predict \\",
        "     -F \"file=@sample_leaf.jpg\"",
        "",
        "# Ket qua tra ve co dang:",
        "{",
        "  \"predicted_class\": \"Anthracnose\",",
        "  \"confidence\": 0.9412,",
        "  \"probabilities\": {",
        "    \"Anthracnose\": 0.9412, \"BacterialSpot\": 0.0201,",
        "    \"Curl\": 0.0043, \"Healthy\": 0.0067, \"RingSpot\": 0.0277",
        "  },",
        "  \"num_boxes\": 12,",
        "  \"boxes\": [ ... ]",
        "}",
    ])
    note("Thay khối JSON minh họa ở trên bằng kết quả thực tế chụp từ một lần gọi API, để phần "
         "minh chứng sản phẩm phản ánh đúng đầu ra của hệ thống.")

    # ------------------------------------------------------------------ 6.3
    h("6.3. Giao diện web", 2)
    p("Giao diện web được xây dựng bằng thư viện Gradio, giao tiếp với dịch vụ REST qua mạng nội "
      "bộ của Docker. Người dùng chỉ cần tải lên một ảnh lá; hệ thống trả về nhãn bệnh, độ tin "
      "cậy, biểu đồ xác suất của năm lớp và ảnh có chú thích các khung tổn thương được phát "
      "hiện.")
    p("Việc hiển thị khung tổn thương là một lựa chọn thiết kế có chủ đích nhằm tăng tính giải "
      "thích được của hệ thống. Người dùng không chỉ nhận một nhãn mà còn thấy được hệ thống căn "
      "cứ vào vùng nào của lá; điều này giúp họ tự đối chiếu bằng mắt thường và tăng mức độ tin "
      "tưởng vào kết quả.")

    note("Chèn ảnh chụp màn hình giao diện web tại đây, gồm ít nhất ba ảnh: (a) màn hình chính "
         "trước khi tải ảnh; (b) kết quả chẩn đoán một lá bệnh kèm khung phát hiện và biểu đồ xác "
         "suất; (c) kết quả chẩn đoán một lá khỏe mạnh. Chạy lệnh docker compose up rồi truy cập "
         "http://localhost:7860 để chụp.")

    note("Chèn ảnh chụp màn hình trang tài liệu API tự sinh tại http://localhost:8000/docs, thể "
         "hiện đầy đủ bốn điểm cuối và lược đồ dữ liệu trả về.")

    # ------------------------------------------------------------------ 6.4
    h("6.4. Đóng gói và triển khai bằng Docker", 2)
    p("Toàn bộ hệ thống được đóng gói thành hai container độc lập, điều phối bằng Docker "
      "Compose. Cách làm này loại bỏ hoàn toàn vấn đề khác biệt môi trường giữa máy phát triển "
      "và máy triển khai, đồng thời cho phép mở rộng theo chiều ngang khi cần.")

    table("Cấu hình hai dịch vụ container của hệ thống",
          ["Hạng mục", "Dịch vụ api", "Dịch vụ web"],
          [
              ["Tên container", "papaya-leaf-api", "papaya-leaf-web"],
              ["Cổng", "8000", "7860"],
              ["Công nghệ", "FastAPI + Uvicorn", "Gradio"],
              ["Nguồn xây dựng", "./api", "./web"],
              ["Biến môi trường chính",
               "YOLO_MODEL_PATH, CNN_MODEL_PATH, MODEL_AUTO_DOWNLOAD, LOAD_MODELS_ON_STARTUP",
               "FASTAPI_URL, GRADIO_SERVER_NAME, GRADIO_SERVER_PORT, REQUEST_TIMEOUT_SECONDS"],
              ["Ổ đĩa gắn ngoài", "model-cache:/app/models (lưu trọng số mô hình)", "Không"],
              ["Phụ thuộc", "Không", "Phụ thuộc dịch vụ api qua mạng nội bộ"],
          ],
          widths=[3.6, 6.2, 6.2], font_size=10.5)

    p("Lệnh khởi chạy toàn bộ hệ thống chỉ gồm một dòng:")
    code_block([
        "docker compose up --build",
        "",
        "# Sau khi khoi chay:",
        "#   Giao dien web : http://localhost:7860",
        "#   Tai lieu API  : http://localhost:8000/docs",
    ])

    p("Bên cạnh Docker Compose dành cho triển khai cục bộ, thư mục infra chứa các tệp mô tả hạ "
      "tầng bằng Terraform, cho phép dựng môi trường triển khai trên nền tảng đám mây một cách "
      "tự động và có thể lặp lại.")

    # ------------------------------------------------------------------ 6.5
    h("6.5. Ứng dụng di động Android", 2)
    p("Mục tiêu cụ thể thứ năm đăng ký trong thuyết minh là triển khai mô hình lên nền tảng Web "
      "hoặc Mobile để trình diễn khả năng nhận dạng thời gian thực. Mục tiêu này đã được hoàn "
      "thành thông qua nền tảng Web trình bày ở các mục trên. Nhánh triển khai trên thiết bị di "
      "động là phần mở rộng tự nguyện, hiện đang trong quá trình phát triển và chưa hoàn tất "
      "tại thời điểm viết báo cáo.")

    h("6.5.1. Hiện trạng", 3)
    p("Khung dự án Android đã được khởi tạo tại thư mục AndroidApp với định hướng sử dụng thư "
      "viện suy luận ncnn để chạy mô hình trực tiếp trên thiết bị, không phụ thuộc kết nối mạng. "
      "Sổ tay 08 đã được chuẩn bị để thực hiện bước chuyển đổi định dạng mô hình. Tuy nhiên, các "
      "tệp trọng số đã chuyển đổi chưa được đưa vào thư mục tài nguyên của ứng dụng, do đó chưa "
      "thể đo được hiệu năng suy luận trên thiết bị thực.")

    h("6.5.2. Kế hoạch hoàn thiện", 3)
    for line in [
        "Chuyển đổi YOLOv11m sang định dạng ncnn hoặc TFLite và lượng tử hóa về số nguyên 8 bit "
        "để giảm kích thước và tăng tốc độ.",
        "Chuyển đổi EfficientNet-B2 sang TFLite, khảo sát phương án thay bằng EfficientNet-B0 "
        "hoặc YOLOv11n nếu ràng buộc tài nguyên thiết bị đòi hỏi; kết quả ở mục 5.3.1 cho thấy "
        "tổ hợp YOLOv11n + EfficientNet-B2 chỉ kém cấu hình tốt nhất 1,04 điểm phần trăm.",
        "Hiện thực lại logic xếp tầng, bao gồm cơ chế hạ ngưỡng thích nghi và bỏ phiếu có trọng "
        "số, bằng Kotlin trên thiết bị.",
        "Xây dựng giao diện chụp ảnh và hiển thị kết quả, hỗ trợ chế độ ngoại tuyến.",
        "Đo thời gian suy luận, mức tiêu thụ bộ nhớ và mức tiêu thụ pin trên ít nhất ba mẫu thiết "
        "bị thuộc các phân khúc khác nhau.",
        "Đối chiếu độ chính xác của phiên bản trên thiết bị với phiên bản máy chủ để định lượng "
        "mức suy giảm do lượng tử hóa.",
    ]:
        bullet(line)

    note("Phần 6.5 sẽ được hoàn thiện sau khi nhánh Android hoàn tất. Khi đó cần bổ sung: "
         "(a) ảnh chụp màn hình ứng dụng trên thiết bị thực; (b) bảng đo thời gian suy luận trên "
         "thiết bị theo từng mẫu máy; (c) bảng so sánh độ chính xác giữa phiên bản trên thiết bị "
         "và phiên bản máy chủ; (d) sơ đồ kiến trúc ứng dụng di động. Nếu tới thời điểm nghiệm "
         "thu nhánh này vẫn chưa hoàn tất, giữ nguyên phần trình bày hiện trạng và kế hoạch như "
         "trên, vì mục tiêu đăng ký trong thuyết minh là Web hoặc Mobile và nhánh Web đã hoàn "
         "thành đầy đủ.")

    # ------------------------------------------------------------------ 6.6
    h("6.6. Khả năng ứng dụng thực tế", 2)
    p("Hệ thống ở trạng thái hiện tại đã sẵn sàng cho ba kịch bản sử dụng.")
    p("Kịch bản thứ nhất là công cụ hỗ trợ nông hộ. Người nông dân chụp ảnh lá nghi ngờ bằng "
      "điện thoại, tải lên giao diện web và nhận chẩn đoán trong khoảng một giây. Rào cản kỹ "
      "thuật gần như bằng không vì thao tác chỉ gồm chụp ảnh và tải lên.")
    p("Kịch bản thứ hai là công cụ sàng lọc cho cán bộ khuyến nông. Với độ chính xác 94,85%, hệ "
      "thống có thể xử lý nhanh khối lượng lớn ảnh khảo sát, khoanh vùng các trường hợp cần "
      "chuyên gia xem xét trực tiếp, qua đó giải phóng thời gian của lực lượng chuyên môn vốn "
      "hạn chế.")
    p("Kịch bản thứ ba là học liệu và nền tảng nghiên cứu. Mã nguồn, sổ tay thực nghiệm và toàn "
      "bộ kết quả trung gian được tổ chức đầy đủ, cho phép sinh viên các khóa sau tái lập kết "
      "quả, thay thế từng thành phần để thử nghiệm ý tưởng mới, hoặc mở rộng sang cây trồng "
      "khác mà không phải xây dựng lại từ đầu.")
    p("Về điều kiện triển khai, dịch vụ chạy được trên máy chủ chỉ có CPU với thời gian phản hồi "
      "dưới một giây mỗi ảnh; khi có GPU, thời gian này giảm đáng kể. Yêu cầu tối thiểu là "
      "khoảng 4 GB bộ nhớ và 2 GB dung lượng lưu trữ cho trọng số mô hình.")

    new_page()


build()
