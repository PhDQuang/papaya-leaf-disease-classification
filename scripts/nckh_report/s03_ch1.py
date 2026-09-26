"""CHƯƠNG 1. TỔNG QUAN BÀI TOÁN."""
from __future__ import annotations

from .core import bullet, figure, figure_row, h, h_center, new_page, p, table


def build() -> None:
    h_center("CHƯƠNG 1. TỔNG QUAN BÀI TOÁN PHÁT HIỆN VÀ PHÂN LOẠI BỆNH TRÊN LÁ CÂY ĐU ĐỦ", 1)

    h("1.1. Vai trò của cây đu đủ và tác động của dịch bệnh", 2)
    p("Đu đủ (Carica papaya) là cây ăn quả nhiệt đới có chu kỳ khai thác ngắn, cho thu hoạch chỉ "
      "sau khoảng tám đến mười tháng trồng, năng suất cao và giá trị dinh dưỡng lớn nhờ hàm "
      "lượng vitamin A, vitamin C và enzyme papain. Tại Việt Nam, cây được trồng rộng rãi ở đồng "
      "bằng sông Cửu Long, Đông Nam Bộ và một số tỉnh miền Trung, vừa phục vụ tiêu dùng nội địa "
      "vừa tham gia xuất khẩu.")
    p("Tuy vậy, đu đủ là cây rất mẫn cảm với dịch bệnh. Lá là bộ phận biểu hiện triệu chứng sớm "
      "nhất và rõ nhất, do đó theo dõi tình trạng lá là biện pháp giám sát dịch bệnh hiệu quả "
      "về chi phí. Khi bệnh lan rộng tới thân và quả, thiệt hại thường đã không thể khắc phục. "
      "Vì vậy, bài toán đặt ra là phát hiện và định danh chính xác biểu hiện bệnh trên lá ở giai "
      "đoạn càng sớm càng tốt.")
    p("Thực tế sản xuất cho thấy ba hạn chế của quy trình chẩn đoán hiện hành. Một là sự phụ "
      "thuộc vào chuyên gia bảo vệ thực vật, lực lượng vốn mỏng so với diện tích canh tác. Hai "
      "là độ trễ: từ lúc phát hiện triệu chứng tới lúc có kết luận có thể mất nhiều ngày. Ba là "
      "tính chủ quan: hai cán bộ khác nhau có thể đưa ra hai kết luận khác nhau trên cùng một "
      "mẫu lá, đặc biệt với các bệnh có triệu chứng chồng lấn.")

    h("1.2. Năm trạng thái bệnh lý được nghiên cứu", 2)
    p("Đề tài xác định năm trạng thái của lá đu đủ, gồm một trạng thái khỏe mạnh và bốn nhóm "
      "bệnh phổ biến. Đặc điểm hình thái của từng trạng thái được tóm tắt trong bảng dưới đây, "
      "sau đó minh họa bằng ảnh thực tế lấy từ bộ dữ liệu.")

    table("Đặc điểm hình thái của năm trạng thái lá đu đủ",
          ["Trạng thái", "Tác nhân", "Biểu hiện đặc trưng trên lá", "Thách thức nhận dạng"],
          [
              ["Healthy (Khỏe mạnh)", "—",
               "Phiến lá xanh đều, gân lá rõ, không có đốm hay biến dạng",
               "Dễ nhầm với lá bệnh giai đoạn rất sớm hoặc lá bị cháy nắng"],
              ["Anthracnose (Thán thư)", "Nấm Colletotrichum spp.",
               "Đốm nâu sẫm lõm, viền sẫm màu, tâm đốm có thể hoại tử và thủng",
               "Số lượng đốm rất lớn trên một lá, kích thước nhỏ, phân bố rải rác"],
              ["RingSpot (Đốm vòng)", "Papaya ringspot virus (PRSV)",
               "Đốm tròn đồng tâm dạng vòng, lá khảm vàng loang lổ, có thể biến dạng",
               "Vòng đồng tâm mờ, dễ nhầm với thán thư giai đoạn đầu"],
              ["BacterialSpot (Đốm vi khuẩn)", "Vi khuẩn Xanthomonas spp.",
               "Đốm nhỏ ngậm nước, quầng vàng bao quanh, về sau khô và chuyển nâu",
               "Kích thước đốm rất nhỏ, dễ bị mất khi giảm độ phân giải ảnh"],
              ["Curl (Xoăn lá)", "Virus gây xoăn lá, truyền qua bọ phấn",
               "Mép lá cuộn lên, phiến lá nhăn nhúm, gân lá dày và nổi rõ, lá nhỏ lại",
               "Biểu hiện ở mức toàn cục, không tập trung thành đốm cục bộ"],
          ],
          widths=[3.2, 3.0, 5.4, 4.4], font_size=10.5)

    figure_row([
        ("readme/Healthy.jpg", "Healthy"),
        ("readme/Anthracnose.jpg", "Anthracnose"),
        ("readme/RingSpot.jpg", "RingSpot"),
    ], "Ảnh minh họa ba trạng thái Healthy, Anthracnose và RingSpot trong bộ dữ liệu BDPapayaLeaf",
        width=4.6)

    figure_row([
        ("readme/BacterialSpot.jpg", "BacterialSpot"),
        ("readme/Curl.jpg", "Curl"),
    ], "Ảnh minh họa hai trạng thái BacterialSpot và Curl trong bộ dữ liệu BDPapayaLeaf",
        width=5.6)

    p("Quan sát các ảnh trên có thể thấy rõ đặc thù của bài toán. Với Anthracnose và "
      "BacterialSpot, thông tin chẩn đoán nằm ở những vùng tổn thương rất nhỏ so với toàn bộ "
      "phiến lá; nếu đưa nguyên ảnh vào một mạng phân loại và thu nhỏ về 224×224 điểm ảnh, phần "
      "lớn chi tiết này sẽ bị mất. Ngược lại, với Curl, biểu hiện là biến dạng hình thái ở mức "
      "toàn cục, không thể nắm bắt qua một vùng cục bộ đơn lẻ. Đây chính là lý do đề tài lựa "
      "chọn kiến trúc xếp tầng có cả nhánh vùng quan tâm và nhánh toàn ảnh dự phòng.")

    h("1.3. Phát biểu bài toán", 2)
    p("Bài toán được phát biểu như sau. Cho một ảnh màu I chụp lá đu đủ, hệ thống cần trả về "
      "một nhãn y thuộc tập năm lớp đã nêu, kèm theo độ tin cậy và, nếu có, danh sách các khung "
      "bao quanh vùng tổn thương được phát hiện. Về mặt hình thức, đây là bài toán phân loại đa "
      "lớp ở mức ảnh, nhưng được giải quyết thông qua một bài toán trung gian là phát hiện đối "
      "tượng ở mức vùng.")
    p("Hai đầu ra của hệ thống phục vụ hai mục đích khác nhau. Nhãn lớp phục vụ ra quyết định "
      "canh tác. Các khung bao quanh phục vụ khả năng giải thích: người dùng có thể nhìn thấy hệ "
      "thống đang căn cứ vào vùng nào của lá để đưa ra kết luận, thay vì nhận một nhãn không có "
      "cơ sở trực quan.")

    h("1.4. Những thách thức kỹ thuật chính", 2)
    for line in [
        "Tổn thương nhỏ và dày đặc: một ảnh lá thán thư trong tập kiểm tra có thể chứa hàng chục "
        "đốm bệnh, dẫn tới 1.054 thực thể trên chỉ 54 ảnh.",
        "Chồng lấn về biểu hiện giữa các lớp: thán thư và đốm vòng ở giai đoạn sớm đều là các đốm "
        "nâu nhỏ, chỉ khác nhau ở cấu trúc vòng đồng tâm rất khó nhận biết.",
        "Mất cân bằng dữ liệu nghiêm trọng: số vùng quan tâm của lớp Anthracnose gấp hơn hai mươi "
        "lần lớp Healthy trong tập huấn luyện của giai đoạn phân loại.",
        "Biến thiên điều kiện chụp: ảnh trong bộ dữ liệu được thu thập ngoài đồng ruộng với ánh "
        "sáng, góc chụp và nền khác nhau.",
        "Ràng buộc triển khai: hệ thống phải chạy được trên phần cứng phổ thông và trả kết quả "
        "trong thời gian người dùng chấp nhận được.",
    ]:
        bullet(line)

    h("1.5. Định hướng giải pháp của đề tài", 2)
    p("Xuất phát từ các thách thức trên, đề tài đề xuất tách bài toán thành hai giai đoạn chuyên "
      "biệt. Giai đoạn thứ nhất dùng bộ phát hiện YOLOv11 để trả lời câu hỏi tổn thương nằm ở "
      "đâu, qua đó tự động loại bỏ phần lớn nền và giữ lại các vùng có giá trị chẩn đoán ở độ "
      "phân giải gốc. Giai đoạn thứ hai dùng mạng EfficientNet để trả lời câu hỏi tổn thương đó "
      "thuộc bệnh nào, với đầu vào là các vùng đã được cắt ra. Kết quả mức ảnh được tổng hợp từ "
      "các dự đoán mức vùng bằng cơ chế bỏ phiếu có trọng số.")
    p("Cách phân rã này mang lại ba lợi ích. Thứ nhất, bộ phân loại làm việc trên ảnh đã được "
      "phóng to vùng quan tâm nên chi tiết tổn thương được bảo toàn. Thứ hai, mỗi ảnh gốc sinh "
      "ra nhiều mẫu huấn luyện ở mức vùng, giúp tăng đáng kể lượng dữ liệu cho giai đoạn hai. "
      "Thứ ba, kiến trúc mô-đun cho phép thay thế độc lập từng thành phần, thuận lợi cho việc so "
      "sánh và nâng cấp.")

    figure("readme/workflow.png",
           "Sơ đồ tổng quan quy trình nghiên cứu của đề tài, từ chuẩn bị dữ liệu, huấn luyện hai "
           "giai đoạn, đánh giá xếp tầng đến triển khai ứng dụng", width=15.0)

    new_page()


build()
