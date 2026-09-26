"""Build the editable SV2026-08 university research report from local evidence."""
from __future__ import annotations

import re
from pathlib import Path

import fitz
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "NghienCuuKhoaHoc" / "BaoCaoTongKet_SV2026-08_BanThao_HoanChinh.docx"
PAPER = ROOT / "docs" / "paper" / "GTSD2026-148-IEEE (1).pdf"

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)
sec.left_margin, sec.right_margin = Cm(3), Cm(2)
sec.header_distance, sec.footer_distance = Cm(1), Cm(1)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(13)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
normal.paragraph_format.line_spacing = 1.4
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.first_line_indent = Cm(0.8)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
for name, size, before, after in [("Title", 18, 0, 12), ("Heading 1", 16, 14, 10), ("Heading 2", 14, 12, 7), ("Heading 3", 13, 8, 5)]:
    s = styles[name]
    s.font.name = "Times New Roman"
    s.font.size = Pt(size)
    s.font.bold = True
    s.font.color.rgb = RGBColor(0, 0, 0)
    s._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    s.paragraph_format.first_line_indent = Cm(0)
    s.paragraph_format.space_before = Pt(before)
    s.paragraph_format.space_after = Pt(after)
    s.paragraph_format.keep_with_next = True
    s.paragraph_format.line_spacing = 1.25

footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer.style = normal
footer.paragraph_format.first_line_indent = Cm(0)
run = footer.add_run()
fld = OxmlElement("w:fldSimple")
fld.set(qn("w:instr"), "PAGE")
run._r.addnext(fld)

figures: list[str] = []
tables: list[str] = []


def p(text: str = "", bold_lead: str | None = None):
    q = doc.add_paragraph(style="Normal")
    if bold_lead and text.startswith(bold_lead):
        q.add_run(bold_lead).bold = True
        q.add_run(text[len(bold_lead):])
    else:
        q.add_run(text)
    return q


def h(text: str, level: int = 1):
    return doc.add_paragraph(text, style=f"Heading {level}")


def new_page():
    doc.add_page_break()


def centered(text: str, size=13, bold=False, after=8):
    q = doc.add_paragraph()
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    q.paragraph_format.first_line_indent = Cm(0)
    q.paragraph_format.space_after = Pt(after)
    r = q.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    return q


def note(text: str):
    q = p("[CẦN BỔ SUNG] " + text)
    q.runs[0].italic = True
    return q


def table(caption: str, header: list[str], rows: list[list[str]], widths: list[float] | None = None):
    tables.append(caption)
    q = doc.add_paragraph()
    q.style = normal
    q.paragraph_format.first_line_indent = Cm(0)
    q.paragraph_format.keep_with_next = True
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    q.add_run(f"Bảng {len(tables)}. {caption}").bold = True
    t = doc.add_table(rows=1, cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, value in enumerate(header):
        c = t.rows[0].cells[i]
        c.text = value
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        if widths:
            c.width = Cm(widths[i])
        for pp in c.paragraphs:
            pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pp.paragraph_format.first_line_indent = Cm(0)
            pp.paragraph_format.space_after = Pt(2)
            for rr in pp.runs:
                rr.bold = True
                rr.font.size = Pt(11)
        tcpr = c._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "E8E8E8")
        tcpr.append(shd)
    trpr = t.rows[0]._tr.get_or_add_trPr()
    header_el = OxmlElement("w:tblHeader")
    header_el.set(qn("w:val"), "true")
    trpr.append(header_el)
    for row in rows:
        cells = t.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if widths:
                cells[i].width = Cm(widths[i])
            for pp in cells[i].paragraphs:
                pp.paragraph_format.first_line_indent = Cm(0)
                pp.paragraph_format.space_after = Pt(1)
                pp.paragraph_format.line_spacing = 1.15
                for rr in pp.runs:
                    rr.font.size = Pt(11)
    for row in t.rows:
        for cell in row.cells:
            tcpr = cell._tc.get_or_add_tcPr()
            borders = tcpr.first_child_found_in("w:tcBorders")
            if borders is None:
                borders = OxmlElement("w:tcBorders")
                tcpr.append(borders)
            for side in ("top", "left", "bottom", "right"):
                el = OxmlElement(f"w:{side}")
                el.set(qn("w:val"), "single")
                el.set(qn("w:sz"), "4")
                el.set(qn("w:color"), "999999")
                borders.append(el)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def figure(rel: str, caption: str, width=14.8):
    path = ROOT / rel
    if not path.exists():
        note(f"Hình: {caption}. Nguồn dự kiến: {rel}.")
        return
    figures.append(caption)
    q = doc.add_paragraph()
    q.paragraph_format.first_line_indent = Cm(0)
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    q.paragraph_format.keep_with_next = True
    q.add_run().add_picture(str(path), width=Cm(width))
    c = doc.add_paragraph()
    c.paragraph_format.first_line_indent = Cm(0)
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.add_run(f"Hình {len(figures)}. {caption}").italic = True
    c.paragraph_format.space_after = Pt(9)


def section(title: str, paragraphs: list[str], level=2):
    h(title, level)
    for text in paragraphs:
        p(text)


def cover(inner=False):
    centered("BỘ GIÁO DỤC VÀ ĐÀO TẠO", 14, True, 2)
    centered("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT THÀNH PHỐ HỒ CHÍ MINH", 14, True, 24)
    centered("BÁO CÁO TỔNG KẾT", 17, True, 4)
    centered("ĐỀ TÀI NGHIÊN CỨU KHOA HỌC CỦA SINH VIÊN", 15, True, 42)
    centered("PHÁT HIỆN VÀ PHÂN LOẠI BỆNH Ở LÁ CÂY ĐU ĐỦ\nSỬ DỤNG MÔ HÌNH YOLOV11 VÀ CNN", 17, True, 14)
    centered("Mã số đề tài: SV2026-08", 14, True, 38)
    if inner:
        p("Thuộc nhóm ngành khoa học: Công nghệ thông tin; ứng dụng trí tuệ nhân tạo trong nông nghiệp.")
        p("Sinh viên chịu trách nhiệm chính: Phạm Đăng Quang — MSSV 23110143.")
        p("Thành viên: Lê Quang Sang — MSSV 23110701; Vũ Minh Hiếu — MSSV 23110218.")
        p("Người hướng dẫn: TS. Bùi Mạnh Quân.")
        note("Điền chính xác lớp, năm học, ngành học, dân tộc và thông tin hành chính theo hồ sơ được phê duyệt; xác nhận nhóm ngành với Phòng KHCN.")
    else:
        centered("Chủ nhiệm đề tài: Phạm Đăng Quang", 14, False, 10)
    centered("TP. Hồ Chí Minh, tháng 9 năm 2026", 13, False, 0)


cover()
new_page()
cover(True)
new_page()
h("MỤC LỤC")
for item in [
    "Thông tin kết quả nghiên cứu của đề tài", "Mở đầu", "Chương 1. Tổng quan và cơ sở lý thuyết",
    "Chương 2. Dữ liệu và thiết kế thực nghiệm", "Chương 3. Phương pháp đề xuất",
    "Chương 4. Kết quả thực nghiệm và thảo luận", "Chương 5. Phân tích sâu về độ tin cậy và giới hạn thực nghiệm",
    "Chương 6. Chương trình máy tính và khả năng ứng dụng", "Chương 7. Kế hoạch kiểm chứng và hướng phát triển",
    "Kết luận và kiến nghị", "Tài liệu tham khảo", "Phụ lục A. Hồ sơ minh chứng sản phẩm",
    "Phụ lục B. Danh mục file kết quả để đối chiếu",
]:
    q = p(item)
    q.paragraph_format.first_line_indent = Cm(0)
new_page()
h("DANH MỤC BẢNG BIỂU")
for item in [
    "Phân bố tập dữ liệu YOLOv11", "Phân bố tập dữ liệu CNN", "Kết quả YOLOv11m theo lớp",
    "So sánh YOLOv11n, s và m", "Kết quả phân loại EfficientNet", "Đánh giá hệ thống hai giai đoạn",
    "So sánh các bộ phân loại", "Hiệu năng theo từng lớp", "Thời gian xử lý",
]:
    p("• " + item)
new_page()
h("DANH MỤC HÌNH")
for item in [
    "Mẫu ảnh của năm lớp", "Quy trình phát hiện và phân loại", "Phân bố nhãn phát hiện",
    "Ma trận nhầm lẫn YOLO", "Đường cong precision–recall", "Đường cong huấn luyện EfficientNet-B2",
    "Ma trận nhầm lẫn phân loại", "Biểu đồ so sánh accuracy và macro F1",
]:
    p("• " + item)
new_page()
h("DANH MỤC CHỮ VIẾT TẮT")
table("Các thuật ngữ viết tắt", ["Ký hiệu", "Nghĩa tiếng Anh", "Giải thích trong báo cáo"], [
    ["AI", "Artificial Intelligence", "Trí tuệ nhân tạo"],
    ["CNN", "Convolutional Neural Network", "Mạng nơ-ron tích chập"],
    ["GPU", "Graphics Processing Unit", "Bộ xử lý đồ họa"],
    ["IoU", "Intersection over Union", "Độ giao trên hợp của hai hộp giới hạn"],
    ["mAP", "mean Average Precision", "Trung bình độ chính xác trung bình"],
    ["NMS", "Non-Maximum Suppression", "Lọc các hộp dự đoán chồng lặp"],
    ["ROI", "Region of Interest", "Vùng ảnh quan tâm"],
    ["YOLO", "You Only Look Once", "Họ mô hình phát hiện đối tượng một lượt"],
], [2.5, 6.2, 9.1])
new_page()
h("THÔNG TIN KẾT QUẢ NGHIÊN CỨU CỦA ĐỀ TÀI")
p("1. Thông tin chung")
p("Tên đề tài: Phát hiện và phân loại bệnh ở lá cây đu đủ sử dụng mô hình YOLOv11 và CNN. Mã số: SV2026-08. Chủ nhiệm: Phạm Đăng Quang, MSSV 23110143. Thành viên: Lê Quang Sang, MSSV 23110701; Vũ Minh Hiếu, MSSV 23110218. Giảng viên hướng dẫn: TS. Bùi Mạnh Quân. Khoa: Công nghệ thông tin.")
p("2. Mục tiêu đề tài")
p("Xây dựng hệ thống hỗ trợ phát hiện vùng biểu hiện bệnh trên lá đu đủ và phân loại ảnh vào năm nhóm: Healthy, RingSpot, Curl, BacterialSpot và Anthracnose. Nghiên cứu kết hợp mô hình phát hiện YOLOv11 với mô hình CNN, kiểm tra chất lượng trên tập dữ liệu BDPapayaLeaf và xây dựng chương trình máy tính minh họa quy trình suy luận.")
p("3. Tính mới và sáng tạo")
p("Đề tài khảo sát quy trình hai giai đoạn: định vị vùng bệnh bằng YOLOv11m, sau đó phân loại vùng ảnh bằng EfficientNet-B2. Điểm đóng góp của thực nghiệm là đánh giá riêng bộ phát hiện, bộ phân loại và toàn bộ quy trình trên các tập kiểm thử xác định; đối chiếu trực tiếp với phương án phân loại ảnh toàn phần và với các CNN khác trong cùng quy trình.")
p("4. Kết quả nghiên cứu")
p("YOLOv11m đạt mAP@0.5 = 77,67% và mAP@0.5:0.95 = 65,20% trên tập kiểm thử phát hiện gồm 257 ảnh bệnh. Quy trình YOLOv11m–EfficientNet-B2 dự đoán đúng 276/291 ảnh kiểm thử, đạt accuracy 94,85%, macro precision 94,92%, macro recall 94,93% và macro F1 94,92%. Các kết quả này được rút ra từ tập dữ liệu nghiên cứu; chưa đại diện cho đánh giá triển khai tại vườn.")
p("5. Đóng góp và khả năng áp dụng")
p("Kết quả cung cấp quy trình thực nghiệm, mô hình và phần mềm minh họa có thể dùng trong đào tạo thị giác máy tính và làm nền cho ứng dụng hỗ trợ quan sát triệu chứng lá đu đủ. Việc ứng dụng ngoài thực tế cần kiểm định thêm trên ảnh từ nhiều vườn, thiết bị và điều kiện ánh sáng khác nhau.")
p("6. Công bố khoa học")
p("Theo thông tin do nhóm cung cấp, bài báo “A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification” đã được chấp nhận đăng. Toàn văn bản thảo được lưu trong thư mục docs/paper của project.")
note("Bổ sung tên hội nghị, đơn vị tổ chức, ISBN/ISSN, đường dẫn công bố và giấy/email chấp nhận đăng; đính kèm bản in minh chứng. Người hướng dẫn ghi phần nhận xét và ký theo PL03 của trường.")
p("Sinh viên chịu trách nhiệm chính: ____________________        Ngày: __________")
p("Nhận xét của người hướng dẫn về đóng góp khoa học của sinh viên: ____________________________________________________________________________________")
p("Người hướng dẫn (ký, ghi rõ họ tên): ____________________")
new_page()

h("MỞ ĐẦU")
section("1. Lý do chọn đề tài", [
    "Đu đủ là cây ăn quả quen thuộc tại nhiều vùng sản xuất. Sức khỏe của bộ lá ảnh hưởng đến quang hợp và khả năng phát triển của cây. Các biểu hiện như đốm, biến dạng hay thay đổi màu sắc có thể là dấu hiệu cần được kiểm tra sớm. Việc nhận biết thủ công phụ thuộc kinh nghiệm, trong khi ảnh chụp ngoài thực tế thay đổi theo ánh sáng, góc nhìn, nền và mức độ bệnh. Vì vậy, công cụ phân tích ảnh có thể hỗ trợ người quan sát sàng lọc ban đầu và lưu lại bằng chứng trực quan.",
    "Đề tài không thay thế kết luận của chuyên gia bảo vệ thực vật. Dữ liệu ảnh chỉ biểu hiện triệu chứng quan sát được, không phải xét nghiệm tác nhân gây bệnh. Trong phạm vi nghiên cứu, tên lớp là nhãn của bộ dữ liệu BDPapayaLeaf; dự đoán của mô hình cần được hiểu là phân loại ảnh theo nhãn đã học. Giới hạn này cần được giữ nhất quán khi mô tả sản phẩm và khả năng ứng dụng.",
    "Những mô hình phân loại toàn ảnh có thể bị ảnh hưởng bởi nền đất, cành, lá khác hoặc vùng ảnh không mang triệu chứng. Mô hình phát hiện đối tượng cho phép định vị vị trí cần quan sát. Kết hợp một bộ phát hiện với một bộ phân loại tạo nên quy trình hai giai đoạn: trước hết tìm vùng nghi ngờ, sau đó phân biệt loại triệu chứng trong vùng đó. Đây là hướng triển khai được lựa chọn trong thuyết minh SV2026-08.",
    "Bài báo đã được nhóm chấp nhận đăng trình bày phương pháp và kết quả cốt lõi trong sáu trang. Báo cáo tổng kết này mở rộng phần thuyết minh phương pháp, trình bày rõ nguồn dữ liệu, cách chia tập, các mô hình so sánh, số liệu theo lớp, phân tích lỗi và thực trạng phần mềm. Nội dung được đối chiếu với các notebook, file CSV và JSON trong project để số liệu có thể truy vết."], 2)
section("2. Mục tiêu nghiên cứu", [
    "Mục tiêu tổng quát là xây dựng và đánh giá một quy trình tự động phát hiện, khoanh vùng và phân loại năm trạng thái lá đu đủ từ ảnh. Quy trình dùng YOLOv11 để định vị vùng có triệu chứng và CNN để quyết định nhãn ảnh. Kết quả mong muốn là một mô hình có số liệu đánh giá rõ ràng cùng chương trình máy tính minh họa suy luận.",
    "Các mục tiêu cụ thể theo BM02 gồm: lựa chọn và chuẩn bị dữ liệu BDPapayaLeaf; huấn luyện YOLOv11 cho bốn lớp bệnh; huấn luyện CNN cho năm lớp bao gồm Healthy; so sánh các biến thể mô hình; đo precision, recall, F1, mAP và phân tích ma trận nhầm lẫn; tích hợp mô hình vào một phần mềm demo. BM02 còn nêu đánh giá tốc độ và khả năng thích nghi với ánh sáng, góc chụp ngoài vườn. Báo cáo này chỉ kết luận theo những phép đo đã có bằng chứng.",
    "Sản phẩm đăng ký với trường gồm báo cáo tổng kết, chương trình máy tính và bài báo toàn văn tại hội thảo có ISBN/ISSN. Vì thế, đánh giá hoàn thành phải xét cả ba sản phẩm. Bài báo không thay thế cuốn báo cáo tổng kết. Chương trình phải có bản có thể chạy và được trình diễn phù hợp với cấu hình có sẵn tại thời điểm nghiệm thu."], 2)
section("3. Đối tượng, phạm vi và câu hỏi nghiên cứu", [
    "Đối tượng là ảnh lá đu đủ thuộc năm trạng thái được gán nhãn: Anthracnose, Bacterial Spot, Curl, Healthy và Ring Spot. YOLO chỉ phát hiện bốn trạng thái bệnh vì ảnh Healthy không có hộp chú thích vùng bệnh. Bộ phân loại CNN nhận cả năm lớp. Phạm vi dữ liệu là bộ BDPapayaLeaf đã được xử lý trong project; không có tập ảnh mới thu thập tại vườn Việt Nam được chứng minh trong hồ sơ hiện có.",
    "Câu hỏi thứ nhất là biến thể YOLOv11 nào cho chất lượng phát hiện phù hợp trên tập ảnh bệnh. Câu hỏi thứ hai là trong các CNN được thử, mô hình nào hỗ trợ phân loại vùng cắt tốt nhất. Câu hỏi thứ ba là liệu quy trình định vị rồi phân loại có cải thiện kết quả so với phân loại ảnh toàn phần trên bộ kiểm thử tương ứng. Câu hỏi cuối cùng là những lỗi nào còn tồn tại và chúng gây hạn chế gì cho ứng dụng thực tế.",
    "Kết quả accuracy của CNN trên các vùng cắt không thể so sánh trực tiếp như cùng một đại lượng với accuracy của hệ thống trên ảnh gốc: đơn vị mẫu và kích thước tập kiểm thử khác nhau. Báo cáo dùng từng phép đo đúng với đối tượng của nó. Phép so sánh quan trọng nhất cho hiệu quả quy trình là phương án hai giai đoạn và phương án EfficientNet-B2 toàn ảnh, cùng đánh giá ở cấp ảnh trên 291 mẫu."], 2)
section("4. Phương pháp và bố cục báo cáo", [
    "Nghiên cứu kết hợp khảo sát tài liệu, tiền xử lý và kiểm tra dữ liệu, huấn luyện mô hình, đánh giá định lượng, phân tích lỗi và triển khai phần mềm. Các file notebook ghi lại quy trình xử lý; báo cáo CSV/JSON lưu đầu ra đánh giá. Các con số chính được lấy từ chính các báo cáo này, còn bài báo đã duyệt là tài liệu đối chiếu cách diễn giải phương pháp.",
    "Chương 1 trình bày bối cảnh và cơ sở lý thuyết. Chương 2 mô tả dữ liệu, chuẩn bị và thiết kế thực nghiệm. Chương 3 giải thích quy trình YOLOv11–EfficientNet-B2 và các phương án đối chứng. Chương 4 trình bày kết quả và so sánh. Chương 5 phân tích sâu sai số và độ tin cậy. Chương 6 ghi nhận chương trình máy tính, mức hoàn thành và kế hoạch kiểm chứng còn thiếu. Kết luận tổng hợp điều đã đạt và kiến nghị."], 2)

new_page()
h("CHƯƠNG 1. TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT")
section("1.1. Bài toán phân tích ảnh lá đu đủ", [
    "Bài toán đầu vào là một ảnh màu chứa lá đu đủ. Đầu ra cuối cùng là một trong năm nhãn của tập dữ liệu. Nếu ảnh có dấu hiệu bệnh, bộ phát hiện còn xuất các hộp giới hạn bao quanh vùng nghi ngờ. Kết quả vì thế có hai tầng thông tin: vị trí cần xem và nhãn tổng hợp ở cấp ảnh. Hai tầng thông tin có cách đánh giá khác nhau; vị trí dùng các chỉ số mAP theo IoU, còn nhãn ảnh dùng accuracy, precision, recall và F1.",
    "Các dấu hiệu thị giác có thể xuất hiện ở nhiều tỉ lệ: một đốm nhỏ, nhiều đốm rải rác hoặc một vùng lá đổi màu rộng. Trên cùng một ảnh, các vùng bệnh có thể chồng lấn về biểu hiện. Nền ảnh có thể gồm đất, các lá khác, thân cây và bóng râm. Vì vậy, một mô hình chỉ dựa vào màu sắc toàn ảnh khó mô tả hết các trường hợp; cấu trúc trích xuất đặc trưng nhiều mức được kỳ vọng phù hợp hơn.",
    "Những nhãn dữ liệu như Ring Spot hay Anthracnose được sử dụng theo bộ ảnh nguồn. Báo cáo không suy diễn rằng mọi ảnh mang nhãn đó đã được xác nhận bằng xét nghiệm thực vật. Khi sử dụng mô hình để hỗ trợ thực tế, ảnh và nhãn dự đoán chỉ là một bằng chứng để người có chuyên môn xem xét thêm."], 2)
figure("readme/workflow.png", "Sơ đồ tổng quan quy trình hai giai đoạn của đề tài", 15.0)
section("1.2. Tổng quan nghiên cứu liên quan", [
    "Các nghiên cứu thị giác máy tính trong nông nghiệp đã áp dụng CNN để nhận dạng lá và quả, đồng thời dùng các phiên bản YOLO để tìm vị trí đối tượng. Nghiên cứu về BDPapayaLeaf cung cấp dữ liệu phục vụ phát hiện và phân loại bệnh lá đu đủ [15]. Công trình về EfficientNet [20] cho thấy khả năng điều chỉnh chiều sâu, chiều rộng và độ phân giải một cách phối hợp. Đây là cơ sở để lựa chọn bộ phân loại EfficientNet-B2.",
    "Bài báo của đề tài điểm lại các hướng phân loại ảnh toàn phần, mô hình CNN dùng học chuyển giao và bộ phát hiện YOLO [11]–[23]. Kết quả giữa các công trình chỉ có thể xem là tham khảo khi dữ liệu, điều kiện chụp, số lớp và cách chia tập khác nhau. Báo cáo tập trung vào phép so sánh nội bộ trong cùng project, với các file kết quả lưu lại rõ ràng.",
    "Một nghiên cứu về trái đu đủ không đồng nghĩa với bài toán lá đu đủ vì đối tượng, triệu chứng và cách gán nhãn khác nhau. Tương tự, thành tích trên ImageNet là thông tin về kiến trúc, không phải độ chính xác của ứng dụng lá đu đủ. Khi thảo luận tài liệu liên quan, báo cáo luôn chỉ ra phạm vi của mỗi kết quả thay vì xếp hạng các con số lấy từ những nghiên cứu khác nhau."], 2)
section("1.3. Mạng nơ-ron tích chập và học chuyển giao", [
    "CNN trích xuất đặc trưng ảnh qua các lớp tích chập, hàm kích hoạt, bước lấy mẫu và lớp phân loại. Các lớp đầu có xu hướng biểu diễn cạnh, màu, họa tiết; các lớp sâu kết hợp chúng thành mẫu phức tạp hơn. Trong bài toán lá, đặc trưng hữu ích có thể là hình dạng đốm, rìa vết bệnh, vùng bạc màu hoặc mức độ xoăn của lá. Mô hình học các đặc trưng đó từ dữ liệu đã gán nhãn thay vì từ quy tắc được lập trình thủ công.",
    "Học chuyển giao khởi tạo mô hình bằng trọng số học trên tập ảnh lớn rồi điều chỉnh theo dữ liệu đích. Cách làm này đặc biệt có ích khi dữ liệu mục tiêu không đủ lớn hoặc phân bố mất cân bằng. Trong project, các kiến trúc EfficientNet-B0, B1, B2 cùng VGG16, ResNet50 và DenseNet121 được huấn luyện hoặc đánh giá để tạo bối cảnh so sánh. Việc gọi chung chúng là CNN phù hợp với thuyết minh BM02; mô hình cuối cùng dùng EfficientNet-B2.",
    "Mất cân bằng lớp là vấn đề đáng chú ý. Nếu huấn luyện bằng cách đếm lỗi như nhau trong khi một lớp có rất nhiều vùng cắt, mô hình có thể ưu tiên lớp phổ biến. Báo cáo bài báo ghi nhận sử dụng trọng số lớp, tăng mẫu và tăng cường ảnh ở giai đoạn phân loại. Trọng số cho lớp ít mẫu cao hơn, khiến lỗi của lớp đó ảnh hưởng mạnh hơn đến hàm mất mát; tuy nhiên biện pháp này không thay thế việc thu thập thêm ảnh độc lập."], 2)
section("1.4. Mô hình EfficientNet-B2", [
    "EfficientNet dùng nguyên lý compound scaling: chiều sâu, chiều rộng và độ phân giải đầu vào được mở rộng đồng thời theo các hệ số xác định [20]. So với tăng riêng một kích thước, cách phối hợp hướng tới sử dụng năng lực tính toán hợp lý hơn. Các khối MBConv dùng tích chập tách kênh và đường nối tắt, cho phép trích xuất đặc trưng với số tham số tương đối hiệu quả.",
    "Trong nghiên cứu này, EfficientNet-B2 nhận ảnh vùng quan tâm đã được cắt và đổi kích thước theo cấu hình huấn luyện. Mạng tạo xác suất cho năm lớp. Một ảnh có thể tạo nhiều vùng cắt; do đó, xác suất của CNN không tự nó là nhãn ảnh. Quy trình tổng hợp các dự đoán vùng sẽ được mô tả ở Chương 3. Sự phân biệt giữa kết quả vùng cắt và kết quả ảnh gốc rất quan trọng để giải thích chênh lệch giữa các bảng số liệu.",
    "Việc chọn B2 không chỉ dựa vào lý thuyết mà còn dựa vào so sánh thực nghiệm trong project. Trên tập kiểm thử CNN gồm 1.836 mẫu, B2 đạt accuracy 96,02% và macro F1 95,69%, nhỉnh hơn B0 và B1 trong các file tổng hợp. Tuy nhiên, tập 1.836 mẫu này có nhiều vùng cắt từ ảnh nguồn; đây là kiểm tra ở cấp mẫu CNN, khác với 291 ảnh của quy trình đầy đủ."], 2)
figure("outputs/cnn/efficientnet_b2/history_accuracy.png", "Diễn biến độ chính xác khi huấn luyện EfficientNet-B2", 14.5)
figure("outputs/cnn/efficientnet_b2/history_loss.png", "Diễn biến hàm mất mát khi huấn luyện EfficientNet-B2", 14.5)
section("1.5. Họ mô hình YOLOv11", [
    "YOLO là nhóm mô hình phát hiện đối tượng một giai đoạn: từ ảnh đầu vào, mạng dự đoán đồng thời vị trí và độ tin cậy của đối tượng. Đầu ra gồm tọa độ hộp giới hạn, nhãn và điểm tin cậy. YOLOv11 có các phiên bản n, s, m với quy mô khác nhau. Bản nhỏ có thể suy luận nhanh hơn, còn bản lớn hơn thường có khả năng biểu diễn cao hơn; điều nào phù hợp với dữ liệu phải được kiểm tra bằng thực nghiệm.",
    "Trong đề tài, YOLOv11 học bốn lớp bệnh. Ảnh Healthy không có vùng bệnh để đóng hộp. Điều này có nghĩa mAP của YOLO không phải độ chính xác phân loại năm lớp. Mô hình có thể không tìm thấy hộp ở ảnh lành, nhưng cũng có thể bỏ sót hộp ở ảnh bệnh; logic dự phòng của hệ thống cần xử lý cả hai tình huống.",
    "Quá trình suy luận YOLO còn có bước chọn ngưỡng tin cậy và loại bỏ hộp chồng lấn. Các ngưỡng này tác động đến số vùng được đưa sang CNN. Một ngưỡng cao giúp giảm vùng giả nhưng có thể bỏ sót triệu chứng; ngưỡng thấp tăng độ nhạy nhưng đưa thêm vùng nhiễu. Project dùng ngưỡng ban đầu 0,50 và có cơ chế thử lại thấp dần đến 0,35 trong một số trường hợp."], 2)
figure("outputs/yolo/yolov11_m/labels.jpg", "Phân bố hộp giới hạn và đặc điểm nhãn ở dữ liệu YOLOv11m", 14.0)
section("1.6. Các chỉ số đánh giá", [
    "Đối với phát hiện, precision đo tỉ lệ hộp dự đoán đúng trong số hộp được dự đoán, recall đo tỉ lệ đối tượng được tìm thấy. Một hộp được coi là khớp khi IoU giữa hộp dự đoán và hộp chuẩn đạt ngưỡng. mAP@0.5 tổng hợp average precision tại IoU 0,5; mAP@0.5:0.95 trung bình trên nhiều ngưỡng từ 0,5 đến 0,95. Chỉ số thứ hai khắt khe hơn về vị trí hộp.",
    "Đối với phân loại, accuracy là số dự đoán đúng chia tổng số mẫu. Precision của một lớp là số dự đoán đúng lớp đó chia số lần mô hình dự đoán lớp đó. Recall của một lớp là số dự đoán đúng chia số mẫu thật thuộc lớp đó. F1 là trung bình điều hòa của precision và recall. Macro average lấy trung bình đều qua các lớp, phù hợp để nhìn thấy tác động ở lớp ít mẫu; weighted average tính theo support của lớp.",
    "Ma trận nhầm lẫn cho thấy từng nhãn thật được dự đoán thành nhãn nào. Nó hỗ trợ phát hiện các cặp biểu hiện dễ nhầm và giúp phân tích lỗi cụ thể hơn accuracy chung. Khi đối chiếu nhiều mô hình, phải giữ cùng tập kiểm thử và cùng đơn vị đánh giá. Một kết quả thu trên 257 ảnh bệnh để phát hiện không thể được trình bày như kết quả của 291 ảnh năm lớp để phân loại."], 2)

new_page()
h("CHƯƠNG 2. DỮ LIỆU VÀ THIẾT KẾ THỰC NGHIỆM")
section("2.1. Nguồn dữ liệu", [
    "Nghiên cứu sử dụng BDPapayaLeaf, bộ dữ liệu ảnh lá đu đủ được nêu trong thuyết minh và trích dẫn ở bài báo [15]. Dữ liệu gồm bốn lớp bệnh Anthracnose, Bacterial Spot, Curl, Ring Spot và lớp Healthy. Repo hiện lưu nhãn YOLO, báo cáo làm sạch và các manifest chia tập; ảnh gốc không được đóng gói trong repo tải về. Vì vậy, số liệu trong báo cáo dựa trên file kết quả đã tạo khi nhóm chạy notebook ở môi trường Google Colab.",
    "Ảnh của các lớp có số lượng và đặc điểm hộp khác nhau. Một ảnh Anthracnose hoặc Ring Spot có thể có nhiều hộp vùng bệnh, trong khi Bacterial Spot hoặc Curl thường có ít hộp hơn theo số liệu kiểm thử. Sự khác biệt này ảnh hưởng đến độ khó của phép phát hiện và tới số vùng cắt tạo cho CNN. Không nên diễn giải số vùng cắt CNN như số ảnh lá độc lập.",
    "Mỗi ảnh cần được liên kết với nhãn lớp và, ở dữ liệu phát hiện, với file tọa độ hộp. Định dạng YOLO lưu chỉ số lớp cùng tọa độ tâm và kích thước hộp đã chuẩn hóa về khoảng 0 đến 1. Các bản manifest trong data/reports/preprocessing giúp kiểm tra ảnh nào thuộc tập huấn luyện, kiểm định hoặc kiểm thử, giảm rủi ro dùng nhầm mẫu giữa các giai đoạn."], 2)
table("Phân bố tập dữ liệu phát hiện YOLOv11 sau chuẩn bị", ["Lớp", "Tổng ảnh", "Train", "Validation", "Test"], [
    ["Anthracnose", "355", "248", "53", "54"], ["Bacterial Spot", "458", "320", "69", "69"],
    ["Curl", "361", "253", "54", "54"], ["Ring Spot", "533", "373", "80", "80"],
    ["Tổng", "1.707", "1.194", "256", "257"]], [5.2, 3.2, 3.2, 3.2, 3.2])
section("2.2. Kiểm tra và làm sạch dữ liệu", [
    "Notebook chuẩn bị dữ liệu tạo các báo cáo kiểm tra ảnh nguồn, tên file, mã băm, ảnh gần trùng và nhãn hộp. Báo cáo tổng hợp ghi nhận số ảnh nguồn theo lớp lần lượt là 355, 458, 585, 228 và 533 cho Anthracnose, BacterialSpot, Curl, Healthy và RingSpot. File tổng hợp cũng ghi 224 ảnh nguồn được loại tự động và 158 nhãn không hợp lệ ở dữ liệu đã làm sạch. Các con số này phản ánh quy trình rà soát dữ liệu, không phải số mẫu dùng cuối cùng cho từng phép thử.",
    "Các kiểm tra trùng tên, SHA-1 và perceptual hash đặc biệt cần thiết khi nhiều ảnh có thể chụp cùng một lá hoặc được xuất lại với thay đổi nhỏ. Nếu ảnh gần trùng rơi vào cả tập huấn luyện và kiểm thử, chỉ số đánh giá sẽ lạc quan. Repo có các file kiểm tra, nhưng để công bố mức độ độc lập sinh học giữa mẫu cần thêm thông tin về cây, vườn và buổi chụp; hiện chưa thấy metadata này.",
    "Sau bước làm sạch, ảnh được đưa vào định dạng YOLO cho bài toán phát hiện và vào cấu trúc thư mục theo lớp cho bài toán CNN. Ảnh lành không có hộp bệnh. Bảng phân bố YOLO cho thấy 1.707 ảnh bệnh, tách 1.194 ảnh huấn luyện, 256 ảnh kiểm định và 257 ảnh kiểm thử. Các phép chia được thực hiện theo lớp nhằm tránh biến động quá lớn về tỉ lệ lớp giữa các tập."], 2)
section("2.3. Tập dữ liệu cho CNN", [
    "Bộ dữ liệu CNN bao gồm các vùng quan tâm được chuẩn bị từ ảnh bệnh và ảnh toàn phần đối với Healthy. Mỗi vùng cắt là một mẫu huấn luyện CNN, vì vậy tổng số mẫu lớn hơn số ảnh nguồn. Tổng số theo báo cáo là 11.111 mẫu, gồm 7.562 train, 1.713 validation và 1.836 test. Sự mất cân bằng rất rõ: Anthracnose và Ring Spot có nhiều vùng cắt hơn Healthy, Curl và Bacterial Spot.",
    "Để đối phó sự mất cân bằng, nhóm dùng hàm mất mát có trọng số lớp và tăng cường dữ liệu. Theo bài báo, trọng số ước tính từ tần suất huấn luyện là 0,3425 cho Anthracnose, 4,7263 cho Bacterial Spot, 5,9543 cho Curl, 9,4525 cho Healthy và 0,6270 cho Ring Spot. Các giá trị cao dành cho lớp ít mẫu làm cho một lỗi ở lớp đó có ảnh hưởng lớn hơn trong bước cập nhật tham số.",
    "Tăng cường ảnh có thể làm mô hình tiếp xúc với nhiều biến thiên màu, hướng và hình học trong quá trình học. Tuy nhiên, các phép biến đổi phải phù hợp ngữ nghĩa của bệnh: thay đổi quá mạnh có thể làm mất dấu hiệu lá hoặc tạo ảnh phi thực tế. Mọi ảnh tăng cường dùng để huấn luyện phải được tạo từ tập huấn luyện; không dùng biến thể của ảnh kiểm thử để chọn tham số."], 2)
table("Phân bố dữ liệu phân loại CNN theo mẫu ảnh/vùng cắt", ["Lớp", "Tổng mẫu", "Train", "Validation", "Test"], [
    ["Anthracnose", "6.502", "4.416", "1.046", "1.040"], ["Bacterial Spot", "458", "320", "69", "69"],
    ["Curl", "362", "254", "54", "54"], ["Healthy", "228", "160", "34", "34"],
    ["Ring Spot", "3.561", "2.412", "510", "639"], ["Tổng", "11.111", "7.562", "1.713", "1.836"]], [5.2, 3.2, 3.2, 3.2, 3.2])
section("2.4. Tập kiểm thử cuối cùng ở cấp ảnh", [
    "Phép đánh giá hệ thống hoàn chỉnh dùng 291 ảnh gốc: 257 ảnh bệnh từ tập kiểm thử YOLO cộng với 34 ảnh Healthy. Đây là tập năm lớp để tính độ chính xác cuối cùng của việc phân loại ảnh. Một ảnh có thể có nhiều hộp và nhiều vùng cắt, nhưng ở phép đánh giá này mỗi ảnh chỉ đóng góp một dự đoán cuối cùng. Nhờ vậy, 276 dự đoán đúng trong 291 ảnh tương đương accuracy 94,85%.",
    "Sự khác biệt giữa 1.836 mẫu CNN và 291 ảnh hệ thống cần được nêu trong mọi bảng và biểu đồ. Nếu lấy điểm CNN 96,02% rồi so trực tiếp với điểm hệ thống 94,85% mà không nêu đơn vị mẫu, người đọc có thể hiểu sai. Phép kiểm thử hệ thống phản ánh cả lỗi phát hiện, lỗi cắt vùng, lỗi CNN và cách hợp nhất vùng; phép kiểm thử CNN riêng chỉ phản ánh bộ phân loại trên dữ liệu đã chuẩn bị.",
    "Tập 291 ảnh vẫn chỉ là một phần dữ liệu BDPapayaLeaf. Nó chưa đo đầy đủ khả năng tổng quát trên camera điện thoại khác, mùa vụ khác hay nền vườn Việt Nam. Vì vậy, kết quả cuối cùng là kết quả kiểm thử trong điều kiện dữ liệu nghiên cứu, không phải chứng nhận độ chính xác ngoài hiện trường."], 2)
section("2.5. Ví dụ năm nhãn ảnh", [
    "Các ảnh ví dụ sau được lấy từ thư mục readme của project. Chúng giúp người đọc nhận biết trực quan năm nhóm nhãn; không đại diện cho toàn bộ biến thiên của mỗi lớp. Ảnh ví dụ không được dùng làm bằng chứng định lượng. Các đặc trưng mầu sắc, vết đốm hay hình dạng có thể biến đổi mạnh theo góc chụp và mức bệnh.",
    "Báo cáo cần lưu nguồn ảnh gốc và quyền sử dụng khi nộp bản cuối. Các ảnh minh họa đã tồn tại trong project, còn thông tin chi tiết về người chụp và địa điểm chưa có trong file hiện tại. Nếu có ảnh chụp trực tiếp của nhóm, nên thêm một bảng mô tả điều kiện chụp và chỉ dùng chúng trong đánh giá ngoài tập khi có nhãn xác nhận."], 2)
for filename, label in [("Anthracnose.jpg", "Anthracnose"), ("BacterialSpot.jpg", "Bacterial Spot"), ("Curl.jpg", "Curl"), ("Healthy.jpg", "Healthy"), ("RingSpot.jpg", "Ring Spot")]:
    figure("readme/" + filename, f"Ảnh minh họa lớp {label} trong project", 9.0)
section("2.6. Thiết kế thực nghiệm và tái lập", [
    "Quy trình thực nghiệm được chia thành ba cấp. Cấp thứ nhất so sánh YOLOv11n, YOLOv11s và YOLOv11m trên bốn lớp bệnh. Cấp thứ hai so sánh EfficientNet-B0, B1, B2 và các CNN đối chứng trên dữ liệu phân loại. Cấp thứ ba kết hợp cùng YOLOv11m với các CNN để đánh giá ảnh cuối, đồng thời đo đối chứng EfficientNet-B2 trên ảnh toàn phần.",
    "Repo lưu các notebook theo thứ tự chuẩn bị dữ liệu, huấn luyện, đánh giá và xuất mô hình. File outputs/README.md liệt kê vị trí báo cáo kết quả. Các checkpoint .pt và .keras có sẵn cục bộ; đường dẫn trong JSON còn ghi vị trí Google Drive khi chạy Colab, nên cần chỉnh đường dẫn nếu tái lập ở máy khác. Để tái tạo toàn bộ phép thử, cần khôi phục ảnh gốc BDPapayaLeaf do chúng không nằm trong repo.",
    "Thử nghiệm tốc độ phải được báo cùng thiết bị, cấu hình và cách đo. File throughput của project đo xử lý 291 ảnh cho bốn cặp mô hình; đây là phép đo tổng thể trong môi trường notebook tại thời điểm tạo file, không tự động suy ra tốc độ trên điện thoại. Chương 4 sẽ trình bày con số này cùng giới hạn so sánh."], 2)
section("2.7. Quan hệ giữa ảnh nguồn, hộp và vùng cắt", [
    "Một ảnh nguồn là đơn vị quan sát khi đánh giá quy trình cuối. Một hộp là một vùng được chú thích hoặc dự đoán trên ảnh. Một vùng cắt là phần ảnh được đưa vào CNN. Ba đơn vị này có quan hệ một-nhiều: một ảnh có thể có nhiều hộp, và số vùng cắt sinh ra phụ thuộc số hộp được chọn. Điều này giải thích vì sao tập YOLO 1.707 ảnh bệnh và tập CNN 11.111 mẫu có quy mô rất khác nhau mà vẫn đến từ cùng một nguồn dữ liệu.",
    "Khi tạo tập CNN, việc cắt theo hộp chuẩn cho dữ liệu huấn luyện giúp mạng học đặc điểm của vùng triệu chứng. Khi chạy hệ thống thật, vùng cắt dựa trên hộp dự đoán của YOLO, nên chất lượng đầu vào CNN kém ổn định hơn. Chênh lệch giữa hai nguồn vùng cắt là một dạng khác biệt phân bố ngay bên trong quy trình. Nó là lý do không thể lấy accuracy 96,02% của CNN độc lập để suy ra accuracy của toàn hệ thống.",
    "Có ảnh nhiều hộp vì bệnh biểu hiện thành nhiều đốm nhỏ; có ảnh chỉ một hộp bao vùng rộng. Nếu mỗi hộp được xem là một mẫu độc lập trong việc tính độ chắc chắn, số lượng bằng chứng sẽ bị thổi phồng. Khi phân tích đặc điểm dữ liệu, báo cáo dùng số ảnh để mô tả phạm vi thu thập và dùng số hộp để mô tả gánh nặng phát hiện. Khi tính nhãn cuối, báo cáo quay lại một nhãn trên một ảnh.",
    "Để minh họa chính xác quan hệ này trong bản hoàn thiện, nhóm nên chọn một ảnh từ tập test, vẽ hộp chuẩn và hộp YOLO, trưng ra hai hoặc ba vùng cắt cùng điểm CNN và nhãn ảnh cuối. Hình như vậy có giá trị phương pháp cao hơn một sơ đồ chung. Repo hiện lưu ảnh dự đoán YOLO và kết quả CSV, nhưng chưa có toàn bộ ảnh nguồn để tạo một minh họa ghép thống nhất trong báo cáo."], 2)
figure("outputs/yolo/yolov11_m/val_batch0_pred.jpg", "Ví dụ hộp dự đoán YOLOv11m trên ảnh kiểm định", 14.5)
figure("outputs/yolo/yolov11_m/val_batch0_labels.jpg", "Hộp nhãn chuẩn tương ứng của ảnh kiểm định", 14.5)

new_page()
h("CHƯƠNG 3. PHƯƠNG PHÁP ĐỀ XUẤT")
section("3.1. Kiến trúc hệ thống", [
    "Quy trình nhận một ảnh lá, chạy YOLOv11m để tìm vùng nghi ngờ, cắt những vùng được chọn, đưa từng vùng qua EfficientNet-B2 và tổng hợp thành nhãn ảnh. Nếu không có hộp ở ngưỡng đầu, hệ thống kiểm tra ảnh toàn phần bằng CNN để quyết định Healthy hay thử lại với ngưỡng phát hiện thấp hơn. Thiết kế này nhằm tránh xem mọi ảnh không có hộp là ảnh lành, vì YOLO có thể bỏ sót vùng bệnh.",
    "Hai thành phần có nhiệm vụ tách bạch. YOLO chỉ học các hộp của bốn lớp bệnh, phục vụ định vị. CNN phân biệt năm trạng thái trong vùng ảnh hoặc ảnh toàn phần khi cần. Nhãn phát hiện và nhãn cuối có thể không giống nhau, vì bộ phân loại sử dụng chi tiết trong vùng cắt để quyết định. Một kết quả được trả về tốt nhất nên hiển thị cả hộp, điểm tin cậy phát hiện, xác suất phân loại và nhãn ảnh.",
    "Cấu trúc hai giai đoạn cũng làm lộ các điểm có thể lỗi: YOLO bỏ sót hộp, hộp cắt thiếu dấu hiệu, CNN nhầm lớp, hoặc luật tổng hợp chọn sai nhãn khi một ảnh có nhiều vùng. Việc phân tích riêng từng khâu giúp tìm hướng cải thiện rõ hơn so với chỉ nhìn vào accuracy của hệ thống."], 2)
figure("readme/workflow.png", "Luồng xử lý từ ảnh đầu vào đến nhãn ảnh", 15.0)
section("3.2. Chuẩn bị đầu vào và vùng quan tâm", [
    "Trước khi phát hiện, ảnh được chuyển tới định dạng và kích thước đầu vào theo cấu hình YOLO trong notebook. Tọa độ hộp đầu ra được quy đổi về ảnh gốc. Vùng cắt cho CNN được mở rộng thêm 10% ở mỗi cạnh theo tham số lưu trong summary.json, sau đó giới hạn trong khung ảnh. Bước mở rộng giúp giữ một phần bối cảnh xung quanh vết bệnh thay vì cắt sát đến mức mất rìa triệu chứng.",
    "Nếu ảnh chứa nhiều hộp, mỗi hộp tạo một vùng quan tâm. Điều này tăng khối lượng suy luận nhưng cũng cho phép xử lý các ảnh có nhiều vùng bệnh. Khi hộp quá nhỏ hoặc vượt mép ảnh, phần mềm cần kiểm tra kích thước hợp lệ để tránh lỗi đổi kích thước. Số hộp được phát hiện có thể thay đổi theo ngưỡng tin cậy; vì vậy, mọi phép so sánh mô hình ở cấp hệ thống phải dùng cùng một chính sách ngưỡng.",
    "Một ảnh Healthy theo nhãn chuẩn không có hộp bệnh. Nhưng trong sử dụng, việc không có hộp không đủ để kết luận ảnh lành. Chính sách dự phòng của project đưa ảnh toàn phần cho EfficientNet-B2, kiểm tra ngưỡng xác suất rồi quyết định có thử lại YOLO không. Đây là một quyết định kỹ thuật quan trọng và cần được mô tả chính xác trong báo cáo cũng như mã nguồn triển khai."], 2)
section("3.3. Huấn luyện và lựa chọn YOLOv11", [
    "Ba kích cỡ n, s và m được huấn luyện và kiểm tra với cùng bài toán định vị bốn lớp. Số liệu trong outputs/yolo/reports/final_yolo_comparison.csv cho thấy YOLOv11m có mAP@0.5 cao nhất là 0,7767 và mAP@0.5:0.95 là 0,6520. Bản s đạt lần lượt 0,7657 và 0,6446; bản n đạt 0,7471 và 0,6126. Vì mục tiêu nghiên cứu ưu tiên chất lượng định vị để cung cấp vùng cắt cho CNN, nhóm chọn bản m.",
    "Lựa chọn này có chi phí thời gian: báo cáo đánh giá YOLO ghi thời gian suy luận khoảng 29,66 ms cho bản m, so với 10,83 ms của bản s và 7,24 ms của bản n trong phép đo YOLO riêng. Các con số đo trong một môi trường thử nghiệm; tốc độ hệ thống đầy đủ còn phụ thuộc số vùng cắt và bộ phân loại. Không thể gọi quy trình là thời gian thực trên điện thoại chỉ từ bảng thời gian YOLO.",
    "Ở mức lớp, Anthracnose và Ring Spot khó định vị hơn Bacterial Spot và Curl. Ma trận nhầm lẫn cùng biểu đồ precision–recall giúp kiểm tra mức độ phân biệt. Việc tăng kích cỡ mô hình không tự giải quyết hết sự chênh lệch này; cách gán nhãn, hình dạng vết bệnh, số hộp trên ảnh và điều kiện chụp đều có thể góp phần."], 2)
table("So sánh ba biến thể YOLOv11 trên tập kiểm thử phát hiện", ["Mô hình", "Precision", "Recall", "mAP@0.5", "mAP@0.5:0.95", "Suy luận (ms)"], [
    ["YOLOv11n", "74,61%", "75,63%", "74,71%", "61,26%", "7,24"],
    ["YOLOv11s", "81,32%", "80,89%", "76,57%", "64,46%", "10,83"],
    ["YOLOv11m", "80,24%", "81,62%", "77,67%", "65,20%", "29,66"]], [3.0, 2.5, 2.5, 3.0, 3.5, 3.3])
figure("outputs/yolo/test_evaluations/yolov11_m/BoxPR_curve.png", "Đường cong precision–recall của YOLOv11m trên tập kiểm thử", 14.5)
section("3.4. Huấn luyện và lựa chọn CNN", [
    "Các CNN được huấn luyện trên dữ liệu phân loại năm lớp. Bảng tổng hợp cho thấy EfficientNet-B2 đạt accuracy 96,02% trên 1.836 mẫu CNN và macro F1 95,69%. EfficientNet-B1 đạt 95,97% accuracy, macro F1 95,52%; B0 đạt 95,59% accuracy, macro F1 94,05%. Chênh lệch giữa B1 và B2 về accuracy khá nhỏ, nhưng B2 có kết quả macro F1 cao nhất trong ba biến thể EfficientNet được ghi nhận.",
    "So sánh ở cấp vùng cắt chỉ là một bước chọn mô hình. Khi ghép với YOLO, tác động của hộp bị bỏ sót hoặc cắt chưa tốt có thể làm thay đổi xếp hạng. Do đó, sau khi chọn một số CNN tiềm năng, nhóm còn đánh giá quy trình đầy đủ với cùng YOLOv11m và cùng 291 ảnh kiểm thử. Đây là bước cần thiết để lựa chọn sản phẩm cuối cùng.",
    "Các biểu đồ huấn luyện lưu trong outputs/cnn/efficientnet_b2 cho phép rà soát xu thế accuracy và loss theo epoch. Báo cáo không suy đoán nguyên nhân của từng dao động khi chưa có log chi tiết kèm điều kiện huấn luyện. Việc dùng checkpoint có kết quả tốt nhất trên validation là hợp lý, nhưng test chỉ được dùng để báo cáo cuối, không nên tối ưu lặp đi lặp lại theo test."], 2)
table("Kết quả ba biến thể EfficientNet trên tập kiểm thử CNN 1.836 mẫu", ["Mô hình", "Accuracy", "Macro precision", "Macro recall", "Macro F1"], [
    ["EfficientNet-B0", "95,59%", "93,51%", "94,68%", "94,05%"],
    ["EfficientNet-B1", "95,97%", "94,69%", "96,42%", "95,52%"],
    ["EfficientNet-B2", "96,02%", "95,98%", "95,59%", "95,69%"]], [4.4, 3.35, 3.35, 3.35, 3.35])
section("3.5. Quy tắc suy luận và hợp nhất", [
    "Theo cấu hình đánh giá hệ thống, ngưỡng YOLO khởi đầu là 0,50, ngưỡng thấp nhất là 0,35 và bước giảm là 0,05. Nếu không tìm thấy hộp ở mức đầu, CNN toàn ảnh được dùng để kiểm tra. Trường hợp nhãn toàn ảnh là Healthy hoặc xác suất lớp bệnh không đạt 0,50 sẽ được trả về Healthy; trường hợp còn nghi bệnh sẽ thử phát hiện lại ở các ngưỡng thấp hơn. Luật này là một heuristic thực nghiệm, không phải xác suất chẩn đoán được hiệu chuẩn.",
    "Với nhiều vùng cắt, hệ thống tính điểm đóng góp từ độ tin cậy của YOLO nhân với xác suất CNN cho lớp dự đoán của vùng. Các điểm được cộng theo lớp để chọn nhãn ảnh. Cách cộng điểm này ưu tiên các lớp xuất hiện ở nhiều vùng và những vùng có độ tin cậy cao. Nó cũng có thể thiên lệch về lớp tạo nhiều hộp, nên cần phân tích khi ứng dụng vào ảnh có phân bố tổn thương rất khác dữ liệu huấn luyện.",
    "Thông số mở rộng hộp 0,10, ngưỡng bệnh toàn ảnh 0,50 và phương thức hợp nhất weighted được lưu trong outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/summary.json. Báo cáo dùng đúng các thông số đó khi diễn giải kết quả 94,85%. Nếu sau này ứng dụng Android thay đổi thuật toán hoặc ngưỡng, phải đánh giá lại thay vì mặc nhiên gắn kết quả cũ cho phiên bản mới."], 2)
section("3.6. Thiết lập đối chứng", [
    "Đối chứng thứ nhất là EfficientNet-B2 phân loại toàn ảnh, không sử dụng YOLO. Trên cùng tập 291 ảnh, mô hình này đạt accuracy 92,78% và macro F1 92,93%. Đối chứng thứ hai giữ YOLOv11m ở giai đoạn đầu và thay CNN bằng VGG16, DenseNet121 hoặc ResNet50. Cách thay một thành phần giúp quan sát ảnh hưởng của bộ phân loại trong một quy trình tương tự.",
    "Các phương án có thể khác nhau về thời gian suy luận và yêu cầu bộ nhớ. Kết quả tốt nhất về accuracy không nhất thiết là lựa chọn tối ưu trên phần cứng hạn chế. Vì BM02 có mục tiêu ứng dụng web hoặc mobile, báo cáo phải trình bày song song chất lượng và tốc độ, đồng thời phân biệt chỉ số trong notebook với số đo trên thiết bị triển khai thực tế.",
    "Phép so sánh với bài báo bên ngoài chỉ được dùng để đặt kết quả vào bối cảnh. Khác biệt về nguồn dữ liệu, nhãn, cách phân chia và chuẩn đánh giá khiến việc khẳng định vượt trội tuyệt đối thiếu cơ sở. Ưu tiên của báo cáo là đối chứng nội bộ đã có file kết quả để người đọc kiểm chứng."], 2)

new_page()
h("CHƯƠNG 4. KẾT QUẢ THỰC NGHIỆM VÀ THẢO LUẬN")
section("4.1. Kết quả phát hiện vùng bệnh", [
    "YOLOv11m đạt precision trung bình 80,24%, recall 81,62%, mAP@0.5 77,67% và mAP@0.5:0.95 65,20% trên tập kiểm thử phát hiện. Sự khác nhau giữa hai chỉ số mAP cho thấy yêu cầu hộp khớp chặt hơn làm kết quả giảm. Điều này quan trọng với giai đoạn CNN, vì hộp cắt lệch có thể làm mất một phần triệu chứng hoặc đưa thêm nền không liên quan.",
    "Bacterial Spot và Curl có mAP@0.5 lần lượt 99,34% và 99,48% trong file kết quả theo lớp; Anthracnose chỉ 51,51% và Ring Spot 60,35%. Không nên mô tả YOLOv11m là đồng đều trên bốn lớp. Hai lớp khó còn có nhiều hộp trên mỗi ảnh trong tập test, khiến việc khớp đúng tất cả tổn thương khó hơn. Cần rà soát ảnh dự đoán và nhãn để xác định cụ thể mức đóng góp của hộp nhỏ, nhiều đốm và tính không nhất quán của gán nhãn.",
    "Đánh giá theo ảnh cuối có thể vẫn đạt cao dù một số hộp bị bỏ sót, bởi hệ thống chỉ cần đủ thông tin để chọn đúng nhãn ảnh. Vì thế, mAP định vị và accuracy phân loại bổ sung cho nhau. Trong một ứng dụng hỗ trợ chỉ ra mọi vùng bệnh, mAP thấp của Anthracnose và Ring Spot là hạn chế đáng kể, dù nhãn toàn ảnh đúng."], 2)
table("Chỉ số phát hiện theo từng lớp của YOLOv11m", ["Lớp", "Ảnh", "Số hộp", "Precision", "Recall", "mAP@0.5", "mAP@0.5:0.95"], [
    ["Anthracnose", "54", "1.054", "57,76%", "62,14%", "51,51%", "31,86%"],
    ["Bacterial Spot", "69", "69", "95,83%", "100%", "99,34%", "91,51%"],
    ["Curl", "54", "54", "98,18%", "100%", "99,48%", "94,83%"],
    ["Ring Spot", "80", "639", "69,20%", "64,32%", "60,35%", "42,61%"]], [3.2, 1.5, 2.0, 2.6, 2.4, 2.9, 3.2])
figure("outputs/yolo/test_evaluations/yolov11_m/confusion_matrix.png", "Ma trận nhầm lẫn của YOLOv11m trong phép phát hiện", 14.0)
figure("outputs/yolo/test_evaluations/yolov11_m/BoxF1_curve.png", "Quan hệ F1 và ngưỡng tin cậy của YOLOv11m", 14.0)
section("4.2. Kết quả bộ phân loại EfficientNet-B2", [
    "Trên tập 1.836 mẫu phân loại, EfficientNet-B2 đạt accuracy 96,02%, macro precision 95,98%, macro recall 95,59% và macro F1 95,69%. Đây là phép đánh giá mô hình CNN độc lập với dữ liệu vùng cắt được chuẩn bị sẵn. Kết quả cho thấy khả năng phân biệt năm nhãn trên đầu vào hợp lệ, nhưng không bao gồm nguy cơ YOLO bỏ sót hoặc tạo hộp không chính xác.",
    "Các lớp ít mẫu như Healthy và Curl được xử lý bằng trọng số lớp, nhưng vẫn cần xem chỉ số theo lớp và ma trận nhầm lẫn. Một macro F1 cao hơn accuracy cân bằng giữa các lớp trong một số trường hợp, song không cho biết mọi lớp đều như nhau. Ngoài ra, nếu nhiều vùng cắt được lấy từ cùng ảnh nguồn, mức độc lập giữa các mẫu thấp hơn cách đếm đơn thuần; báo cáo không coi 1.836 vùng cắt là 1.836 cây lá riêng biệt.",
    "Việc đánh giá CNN riêng là hữu ích để phát hiện vấn đề ở giai đoạn phân loại. Nếu CNN độc lập tốt nhưng quy trình cuối thấp, nguồn lỗi có thể nằm ở bộ phát hiện, hộp cắt hoặc luật hợp nhất. Nếu CNN độc lập đã kém ở một lớp, cần cải thiện dữ liệu hoặc kiến trúc trước khi tối ưu hệ thống."], 2)
figure("outputs/cnn/efficientnet_b2/test_confusion_matrix.png", "Ma trận nhầm lẫn của EfficientNet-B2 trên tập mẫu CNN", 14.0)
section("4.3. Kết quả hệ thống hai giai đoạn", [
    "Phép thử cuối cùng trên 291 ảnh gồm 257 ảnh bệnh và 34 ảnh Healthy. Hệ thống YOLOv11m–EfficientNet-B2 dự đoán đúng 276 ảnh, sai 15 ảnh. Accuracy là 94,85%, macro precision 94,92%, macro recall 94,93% và macro F1 94,92%. Các con số được lưu trong summary.json và classification_report.csv của thư mục pipeline_evaluation/yolov11_m__efficientnet_b2.",
    "Theo lớp, Curl có F1 98,15%, Bacterial Spot 95,59%, Healthy 94,12%, Anthracnose 93,58% và Ring Spot 93,17%. Hỗ trợ mỗi lớp lần lượt là 54, 69, 34, 54 và 80 ảnh theo thứ tự Curl, Bacterial Spot, Healthy, Anthracnose, Ring Spot. Những lớp có ít ảnh kiểm thử hơn có khoảng bất định lớn hơn; báo cáo giữ nguyên support để người đọc tự đánh giá độ chắc chắn.",
    "Ma trận nhầm lẫn tập trung ở đường chéo, phù hợp với accuracy cao. Tuy vậy, mười lăm lỗi vẫn có ý nghĩa vì mục tiêu ứng dụng là gợi ý sớm triệu chứng. Một nhầm lẫn ảnh bệnh sang Healthy có thể gây bỏ qua kiểm tra tiếp; một nhầm lẫn giữa hai bệnh có thể đưa người dùng tới quyết định xử lý không phù hợp. Báo cáo vì thế trình bày ví dụ lỗi và nêu rõ sản phẩm chỉ có giá trị hỗ trợ."], 2)
table("Hiệu năng phân loại theo lớp của hệ thống YOLOv11m–EfficientNet-B2", ["Lớp", "Precision", "Recall", "F1", "Số ảnh"], [
    ["Anthracnose", "92,73%", "94,44%", "93,58%", "54"],
    ["Bacterial Spot", "97,01%", "94,20%", "95,59%", "69"],
    ["Curl", "98,15%", "98,15%", "98,15%", "54"],
    ["Healthy", "94,12%", "94,12%", "94,12%", "34"],
    ["Ring Spot", "92,59%", "93,75%", "93,17%", "80"]], [5.0, 3.2, 3.2, 3.2, 3.2])
figure("outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/confusion_matrix.png", "Ma trận nhầm lẫn của hệ thống trên 291 ảnh kiểm thử", 14.5)
section("4.4. So sánh với mô hình toàn ảnh và CNN thay thế", [
    "Mô hình EfficientNet-B2 toàn ảnh đạt accuracy 92,78% và macro F1 92,93% trên tập ảnh 291 mẫu. Quy trình hai giai đoạn đạt 94,85% và 94,92%, tăng tương ứng 2,07 và 1,99 điểm phần trăm trong phép thử này. Chênh lệch gợi ý lợi ích của việc tập trung vào vùng triệu chứng. Tuy nhiên, từ kết quả này chưa thể kết luận cơ chế vùng cắt luôn tốt hơn trên mọi điều kiện dữ liệu; cần đánh giá thêm bằng tập độc lập ngoài nguồn BDPapayaLeaf.",
    "Khi giữ YOLOv11m ở giai đoạn đầu, thay VGG16 cho accuracy 93,47%, DenseNet121 đạt 94,16%, ResNet50 94,50% và EfficientNet-B2 94,85%. Mức chênh lệch giữa B2 và ResNet50 chỉ 0,35 điểm phần trăm, tương đương một ảnh trong bộ 291 ảnh. Vì vậy, nhận định B2 đứng đầu trong phép thử là đúng, nhưng không nên nói ưu thế lớn hoặc đã được khẳng định thống kê khi chưa phân tích độ bất định.",
    "Các macro F1 tương ứng là 93,28%, 94,09%, 94,26% và 94,92%. Chỉ số này đặt trọng số ngang nhau cho các lớp, cho thấy B2 cũng có lợi thế trên thước đo cân bằng lớp. Dù vậy, lựa chọn triển khai trên điện thoại có thể ưu tiên mô hình nhanh hơn nếu độ trễ của B2 quá cao; đánh giá tốc độ ở mục sau hỗ trợ quyết định đó."], 2)
table("So sánh các mô hình phân loại cuối ở cấp ảnh trên 291 mẫu", ["Cấu hình", "Accuracy", "Macro precision", "Macro recall", "Macro F1"], [
    ["EfficientNet-B2 toàn ảnh", "92,78%", "93,17%", "92,86%", "92,93%"],
    ["YOLOv11m + VGG16", "93,47%", "92,88%", "94,23%", "93,28%"],
    ["YOLOv11m + DenseNet121", "94,16%", "93,72%", "94,73%", "94,09%"],
    ["YOLOv11m + ResNet50", "94,50%", "93,93%", "94,76%", "94,26%"],
    ["YOLOv11m + EfficientNet-B2", "94,85%", "94,92%", "94,93%", "94,92%"]], [6.0, 2.9, 2.9, 2.9, 2.9])
figure("outputs/pipeline_evaluation/comparison_accuracy.png", "So sánh accuracy của các quy trình được thử nghiệm", 14.5)
figure("outputs/pipeline_evaluation/comparison_macro_f1.png", "So sánh macro F1 của các quy trình được thử nghiệm", 14.5)
section("4.5. Phân tích lỗi", [
    "Các file error_cases.csv và error_predictions.csv lưu những ảnh phân loại sai trong đánh giá hệ thống. Một số cặp lỗi xuất hiện giữa các lớp bệnh có đặc điểm thị giác gần nhau, đặc biệt khi vết bệnh nhỏ, nhiều vùng chồng lấn hoặc nền ảnh phức tạp. Việc xem từng ảnh lỗi là cần thiết để phân biệt lỗi xuất phát từ dữ liệu, YOLO, CNN hay chính sách hợp nhất.",
    "Một nhóm lỗi quan trọng là dự đoán Healthy cho ảnh bệnh. Nếu YOLO không tìm thấy hộp ở ngưỡng ban đầu và CNN toàn ảnh đánh giá xác suất bệnh thấp, quy trình có thể dừng ở Healthy. Chính sách thử lại ngưỡng thấp hơn được thiết kế nhằm giảm tình huống này, nhưng chưa triệt tiêu mọi lỗi. Một nhóm khác là dự đoán nhầm giữa Ring Spot, Anthracnose và Bacterial Spot khi triệu chứng có màu và cấu trúc tương tự trên ảnh.",
    "Đối với từng ảnh lỗi, báo cáo nghiệm thu nên chọn một số ví dụ có chú thích: nhãn thật, nhãn dự đoán, điểm YOLO, điểm CNN và vị trí hộp. Các ảnh đã được xuất trong outputs/pipeline_evaluation và outputs/yolo. Những ví dụ này giúp hội đồng nhìn thấy giới hạn của phương pháp, đồng thời là cơ sở định hướng thu thêm dữ liệu. Không nên chỉ trình bày ảnh dự đoán đúng."], 2)
note("Bổ sung 2–4 ảnh lỗi tiêu biểu đã được GVHD kiểm tra từ outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/error_cases.csv và ảnh gốc tương ứng. Repo hiện không chứa toàn bộ ảnh gốc để chèn đúng từng trường hợp.")
section("4.6. Thời gian xử lý và tính khả thi", [
    "File model_throughput_20260703_155451.csv đo cả quy trình cho 291 ảnh. Cặp YOLOv11m–EfficientNet-B2 mất 283,28 giây, tương ứng trung bình khoảng 973,48 ms/ảnh và 1,03 ảnh/giây trong phép đo này. ResNet50, VGG16 và DenseNet121 có thời gian trung bình lần lượt khoảng 475,40, 470,09 và 510,96 ms/ảnh. B2 cho accuracy cao nhất nhưng có độ trễ cao nhất trong bốn cặp được đo.",
    "Thời gian YOLO riêng ở bảng trước và thời gian hệ thống không đo cùng phạm vi xử lý. Hệ thống còn cần cắt vùng, chạy CNN nhiều lần theo số hộp và tổng hợp kết quả. File benchmark ghi tổng cộng 1.347 hộp và 1.339 vùng cắt hợp lệ cho mỗi cấu hình, cùng 10 lần thử lại ngưỡng tin cậy. Số vùng cắt nhiều giải thích vì sao thời gian cấp ảnh có thể cao hơn thời gian chạy một lần YOLO.",
    "Chưa có số liệu độ trễ và mức dùng bộ nhớ trên thiết bị Android thật. Vì thế, không kết luận ứng dụng Android đáp ứng thời gian thực. Nếu mục tiêu là demo tại hội đồng, cần chọn cấu hình đủ ổn định, đo ít nhất một số ảnh trên chính thiết bị sẽ dùng và lưu thông tin thiết bị, phiên bản mô hình, thời gian khởi tạo và thời gian suy luận."], 2)
table("Thời gian xử lý toàn quy trình theo benchmark trong project", ["Cấu hình", "291 ảnh (giây)", "Trung bình (ms/ảnh)", "Ảnh/giây"], [
    ["YOLOv11m + VGG16", "136,80", "470,09", "2,13"],
    ["YOLOv11m + ResNet50", "138,34", "475,40", "2,10"],
    ["YOLOv11m + DenseNet121", "148,69", "510,96", "1,96"],
    ["YOLOv11m + EfficientNet-B2", "283,28", "973,48", "1,03"]], [7.0, 3.2, 4.5, 3.1])
section("4.7. Đánh giá mức đáp ứng mục tiêu BM02", [
    "Mục tiêu chuẩn bị dữ liệu, huấn luyện YOLOv11 và CNN, so sánh và đánh giá bằng các chỉ số định lượng đã có bằng chứng trong notebook và outputs. Mục tiêu đạt độ chính xác phân loại cao được hỗ trợ bởi kết quả 94,85% trên 291 ảnh kiểm thử. Mục tiêu triển khai chương trình máy tính có mã web/API và mã Android; mức hoàn thành, khả năng chạy độc lập và khả năng trình diễn của từng phần được mô tả ở Chương 5.",
    "Mục tiêu đánh giá khả năng thích nghi khi ánh sáng hoặc góc chụp thay đổi ở vườn trồng thực tế chưa có bộ thử nghiệm riêng được ghi nhận trong tài liệu hiện có. Các ảnh BDPapayaLeaf có biến thiên tự nhiên, nhưng điều đó không thay thế thử nghiệm hiện trường có thiết kế. Phần này cần được ghi là giới hạn và kế hoạch bổ sung, không chuyển thành kết quả đạt được.",
    "Báo cáo cũng cần phân biệt kết quả khoa học với mức độ hoàn thiện sản phẩm. Bài báo đã được chấp nhận theo thông tin nhóm cung cấp; tuy nhiên minh chứng chấp nhận đăng và thông tin ISBN/ISSN phải bổ sung trong hồ sơ cuối. Phần mềm web/API có thể là bản demo hiện hành. Android đã có mã và APK thử nghiệm, nhưng thư mục assets chưa chứa các mô hình suy luận; không ghi Android là sản phẩm hoàn chỉnh tại thời điểm soạn báo cáo."], 2)
section("4.8. Diễn giải tổng hợp các chỉ số", [
    "Mỗi chỉ số trong báo cáo trả lời một câu hỏi cụ thể. mAP@0.5 đo khả năng tìm vùng bệnh với ngưỡng giao vừa phải; mAP@0.5:0.95 kiểm tra vị trí hộp chặt hơn. Accuracy cấp ảnh đo tỷ lệ dự đoán nhãn cuối đúng. Macro F1 cho phép các lớp ít ảnh có tiếng nói tương đương lớp nhiều ảnh. Thời gian trung bình và phân vị phản ánh chi phí xử lý. Một mô hình chỉ thật sự phù hợp nếu cân bằng được các khía cạnh gắn với mục tiêu sử dụng.",
    "Với mục tiêu nghiên cứu chứng minh quy trình hai giai đoạn, cấu hình YOLOv11m–EfficientNet-B2 có kết quả phân loại cao nhất trong nhóm đã thử. Với mục tiêu phát hiện mọi đốm bệnh, mAP theo lớp của Anthracnose và Ring Spot cho thấy chưa thể coi hệ thống đã giải quyết xong bài toán định vị. Với mục tiêu chạy trên điện thoại, benchmark gần một giây mỗi ảnh ở môi trường notebook và thiếu phép thử Android là hai hạn chế cần xử lý.",
    "Các chỉ số cao không bảo đảm thông tin về độ nghiêm trọng của bệnh. Bộ dữ liệu và mô hình hiện tại dự đoán nhãn, không ước lượng tỷ lệ diện tích lá bị tổn thương, giai đoạn bệnh hoặc khuyến nghị xử lý. Nếu giao diện hiển thị các nội dung này trong tương lai, cần có dữ liệu gán nhãn và phương pháp đánh giá riêng. Báo cáo giới hạn kết luận vào năm nhãn phân loại và bốn lớp phát hiện đã được thực nghiệm.",
    "Sự khác biệt giữa lớp Healthy trong CNN và bốn lớp YOLO là một điểm thiết kế cơ bản. Một ảnh không có hộp có thể là ảnh lành hoặc một ca bỏ sót, nên luật dự phòng có vai trò quan trọng. Hai ảnh Ring Spot bị phân loại Healthy trong ma trận cuối cho thấy luật dự phòng chưa hoàn hảo. Phần thảo luận này hỗ trợ hội đồng đánh giá cả thành công lẫn giới hạn thực tế của đề tài."], 2)
figure("outputs/pipeline_evaluation/comparison_macro_recall.png", "So sánh macro recall của các quy trình trong project", 14.5)
figure("outputs/pipeline_evaluation/comparison_weighted_f1.png", "So sánh weighted F1 của các quy trình trong project", 14.5)

new_page()
h("CHƯƠNG 5. PHÂN TÍCH SÂU VỀ ĐỘ TIN CẬY VÀ GIỚI HẠN THỰC NGHIỆM")
section("5.1. Đọc ma trận nhầm lẫn ở cấp ảnh", [
    "Ma trận nhầm lẫn của hệ thống hai giai đoạn có tổng 291 ảnh. Đường chéo gồm 51 Anthracnose, 65 Bacterial Spot, 53 Curl, 32 Healthy và 75 Ring Spot được dự đoán đúng. Tổng là 276 ảnh, trùng với accuracy trong summary.json. Việc cộng lại từ ma trận là một bước kiểm tra độc lập hữu ích khi đưa số liệu vào báo cáo; nó bảo đảm rằng biểu đồ, bảng theo lớp và chỉ số tổng cùng nói về một tập kiểm thử.",
    "Trong 54 ảnh Anthracnose, có 3 ảnh bị dự đoán Ring Spot. Trong 69 ảnh Bacterial Spot, có 1 ảnh nhầm Anthracnose, 1 ảnh nhầm Curl và 2 ảnh nhầm Ring Spot. Lớp Curl có 1 ảnh nhầm Bacterial Spot. Trong 34 ảnh Healthy, 1 ảnh nhầm Bacterial Spot và 1 ảnh nhầm Ring Spot. Trong 80 ảnh Ring Spot, 3 ảnh nhầm Anthracnose và 2 ảnh nhầm Healthy. Các con số này là nội dung trực tiếp của confusion_matrix.csv, không phải ước lượng từ hình.",
    "Lỗi giữa Anthracnose và Ring Spot chiếm sáu trên mười lăm ảnh sai nếu tính cả hai chiều. Từ ma trận có thể xác định hiện tượng nhầm lẫn, nhưng không thể khẳng định nguyên nhân chỉ bằng bảng số. Cần mở ảnh nguồn, hộp chuẩn và hộp dự đoán để xem vết bệnh có nhỏ, chồng lấn hay bị che hay không. Nếu ảnh thực sự có nhiều triệu chứng nhưng nhãn dữ liệu chỉ cho một lớp, đánh giá một nhãn sẽ ghi nhận lỗi dù đầu ra có thể chứa thông tin có ích.",
    "Hai ảnh Ring Spot bị dự đoán Healthy là loại sai đáng chú ý vì hệ thống không còn đưa cảnh báo bệnh. Ngược lại, hai ảnh Healthy bị dự đoán thành bệnh làm phát sinh cảnh báo không cần thiết. Tùy bối cảnh sử dụng, hai loại sai có hậu quả khác nhau; một chỉ số accuracy chung không phản ánh sự bất đối xứng này. Trong triển khai thực tế, ngưỡng cảnh báo nên được chọn bằng dữ liệu độc lập và trao đổi với chuyên gia nông học."], 2)
table("Số ảnh phân loại sai theo nhãn thật và nhãn dự đoán", ["Nhãn thật", "Dự đoán sai", "Số ảnh", "Ý nghĩa kiểm tra"], [
    ["Anthracnose", "Ring Spot", "3", "Xem vùng đốm nhỏ và hộp cắt"],
    ["Bacterial Spot", "Anthracnose / Curl / Ring Spot", "1 / 1 / 2", "Xem biểu hiện pha trộn và luật bỏ phiếu"],
    ["Curl", "Bacterial Spot", "1", "Xem chất lượng ảnh toàn lá"],
    ["Healthy", "Bacterial Spot / Ring Spot", "1 / 1", "Kiểm tra phát hiện dương tính giả"],
    ["Ring Spot", "Anthracnose / Healthy", "3 / 2", "Ưu tiên xem trường hợp bỏ sót bệnh"]], [3.2, 5.7, 2.2, 6.7])
section("5.2. Phân tích lỗi theo giai đoạn", [
    "File error_cases.csv lưu các trường reason, num_boxes, conf_used và các dự đoán vùng. Chúng cho phép phân loại lỗi ở mức vận hành mà không chỉ đoán theo nhãn cuối. Trường hợp reason bằng no_yolo_box_after_conf_retry cho thấy hệ thống đã hạ ngưỡng YOLO đến 0,35 mà vẫn không có hộp; ảnh bệnh có thể trở thành Healthy. Trường hợp yolo_boxes_cnn_weighted_vote nghĩa là có hộp nhưng điểm tổng hợp từ CNN dẫn đến nhãn sai.",
    "Ví dụ, một ảnh Bacterial Spot trong file lỗi có bốn vùng, ba vùng được CNN nhận là Anthracnose và một vùng là Bacterial Spot. Điểm cộng của Anthracnose cao hơn nên nhãn ảnh thành Anthracnose, dù một vùng lớn được nhận đúng Bacterial Spot. Tình huống này minh họa nhược điểm của quy tắc cộng điểm: nhiều hộp nhỏ cùng nhãn có thể thắng một hộp lớn. Nó gợi ý thử cơ chế gộp hộp hoặc cho trọng số theo diện tích, nhưng đề tài chưa có phép kiểm chứng phương án đó.",
    "Một ảnh Bacterial Spot khác có một vùng Bacterial Spot được CNN dự đoán đúng và một vùng Ring Spot được dự đoán sai. Điểm của Ring Spot lớn hơn chút ít, nên nhãn cuối là Ring Spot. Đây là lỗi rất khác trường hợp YOLO không phát hiện. Nếu chỉ tăng độ nhạy YOLO, lỗi bỏ phiếu có thể còn tăng khi hệ thống sinh thêm nhiều hộp không liên quan. Cải thiện phải dựa trên đúng cơ chế lỗi.",
    "Một số ảnh Healthy bị dự đoán bệnh ngay khi YOLO tạo hộp có độ tin cậy cao. Trong trường hợp này, chính sách kiểm tra ảnh toàn phần khi không có hộp không được kích hoạt. Việc bổ sung một nhánh kiểm định Healthy độc lập hoặc ngưỡng hai phía có thể giúp giảm cảnh báo giả, nhưng cần đánh giá trên một tập mới. Báo cáo chỉ nêu đây là hướng thử, không ghi là kết quả đã triển khai.",
    "Các file CSV chứa đường dẫn Colab tới ảnh gốc. Nếu nhóm còn dữ liệu trên Google Drive, nên trích 3–5 ví dụ nêu trên, chú thích chính xác nhãn thật, nhãn vùng và điểm cuối. Nếu không còn ảnh gốc, không nên tạo lại hình bằng ảnh tương tự chỉ để minh họa lỗi cụ thể. Bảng số lỗi và phân tích từ log vẫn có giá trị, miễn là giới hạn về kiểm tra trực quan được nêu rõ."], 2)
section("5.3. Kiểm tra tính nhất quán của các phép đo", [
    "Một dự án có nhiều notebook dễ gặp lỗi đưa kết quả ở các thời điểm hoặc tập thử khác nhau vào cùng bảng. Trong báo cáo này, kết quả YOLO được lấy từ thư mục test_evaluations của từng biến thể, kết quả CNN từ final_cnn_comparison.csv, kết quả quy trình từ summary.json và baseline cùng tập ảnh từ thư mục cnn_full_image_baselines. Tên file và cỡ mẫu được ghi trong Phụ lục B để người đọc truy lại.",
    "Bộ phát hiện đánh giá 257 ảnh bệnh, trong khi bảng chỉ số YOLO cũng có cột số lượng hộp. Anthracnose có 1.054 hộp trên 54 ảnh test và Ring Spot có 639 hộp trên 80 ảnh test. Không dùng tổng hộp làm mẫu số để tính accuracy cấp ảnh. Ở giai đoạn CNN, 1.836 là số ảnh/vùng cắt, khác 1.707 ảnh YOLO và 291 ảnh quy trình cuối. Những số này cùng đúng khi đặt vào đúng cấp xử lý.",
    "Accuracy 94,85% là 276 chia 291. Độ chính xác của baseline toàn ảnh 92,78% tương ứng khoảng 270 ảnh đúng, nên mức hơn 2,07 điểm phần trăm tương đương khoảng sáu ảnh trong một tập nhỏ. Bảng so sánh với ResNet50 cho chênh 0,35 điểm phần trăm, tương đương một ảnh. Diễn giải bằng số ảnh giúp tránh ngôn ngữ cường điệu khi mức chênh rất nhỏ.",
    "Trong bản PDF bài báo có một ô bảng dùng 0.9492 ở cột mang nhãn phần trăm. Báo cáo trường trình bày thống nhất 94,92%, đúng với summary.json. Tương tự, giá trị macro recall của baseline làm tròn từ file nguồn phải được ghi nhất quán theo quy tắc hai chữ số thập phân. Những điều chỉnh này là thống nhất định dạng số liệu, không thay đổi phép thử."], 2)
section("5.4. Kiểm soát nguy cơ rò rỉ dữ liệu", [
    "Notebook tiền xử lý mô tả việc chia ảnh bệnh theo train, validation và test trước khi tạo vùng cắt cho CNN, nhằm giữ các vùng từ cùng ảnh nguồn trong cùng một tập. Đây là một bước bảo vệ quan trọng: nếu các vùng cắt từ cùng ảnh được phân tán sang các tập khác nhau, CNN có thể học những đặc điểm riêng của ảnh rồi được kiểm tra trên vùng gần trùng của chính ảnh đó. Kết quả khi ấy không phản ánh tổng quát hóa tới ảnh mới.",
    "Báo cáo audit có kiểm tra SHA-1 và perceptual hash giữa các lớp. Nó ghi 448 ảnh xung đột SHA-1 khác lớp và 224 ảnh nguồn loại tự động. Các số này cần được giải thích cùng notebook xử lý vì xung đột ban đầu không có nghĩa còn rò rỉ trong tập cuối. Danh sách manifest sau làm sạch và kiểm tra split cuối là bằng chứng mạnh hơn để kết luận về bộ dữ liệu dùng huấn luyện.",
    "Ngay cả khi không còn ảnh trùng giữa train và test, những ảnh chụp cùng cây hoặc cùng buổi có thể vẫn giống nhau. Không có định danh cây/vườn trong dữ liệu hiện tại để xác minh mức độc lập này. Do đó, kết quả test nên gọi là hiệu năng trên tập kiểm thử nội bộ BDPapayaLeaf. Một đánh giá theo vườn hoặc theo thiết bị chụp là bước cần thiết nếu muốn chứng minh khả năng chuyển sang môi trường mới.",
    "Khi cập nhật dữ liệu, quy tắc chia tập phải được đóng băng trước lúc thử mô hình mới. Nếu nhóm chọn nhiều ngưỡng, nhiều kiến trúc và nhiều cách hợp nhất dựa trên chính tập test 291 ảnh, tập test dần trở thành tập điều chỉnh. Lúc đó cần thu một tập khóa mới để báo cáo kết quả cuối. Báo cáo nghiệm thu hiện tại chỉ trình bày các kết quả đã có và tránh khẳng định độ chắc chắn thống kê vượt bằng chứng."], 2)
section("5.5. Độ bất định và ý nghĩa của chênh lệch nhỏ", [
    "Một tỉ lệ đúng quan sát trên 291 ảnh là ước lượng cho phân bố ảnh tương tự tập kiểm thử. Nó thay đổi nếu chọn một mẫu kiểm thử khác. Các lớp có 34 đến 80 ảnh càng nhạy với một hoặc hai mẫu sai: thêm một lỗi ở Healthy làm recall của lớp thay đổi gần 2,94 điểm phần trăm; thêm một lỗi ở Ring Spot làm thay đổi 1,25 điểm. Do đó, phần thảo luận phải giữ cỡ mẫu theo lớp khi kết luận.",
    "Chênh 0,35 điểm phần trăm giữa EfficientNet-B2 và ResNet50 trong cùng quy trình là một ảnh trên 291. Không có kiểm định thống kê ghép cặp hoặc lặp lại nhiều seed trong hồ sơ hiện tại. Vì vậy, báo cáo chỉ nói B2 đạt điểm cao nhất trong phép đánh giá đã thực hiện, không khẳng định nó vượt trội ổn định trên mọi bộ mẫu.",
    "Chênh 2,07 điểm phần trăm so với baseline toàn ảnh lớn hơn nhưng vẫn cần xem ảnh nào được sửa đúng và ảnh nào mới bị sai. Một phép so sánh ghép cặp ở cấp từng ảnh sẽ hữu ích: đếm số ảnh cả hai đúng, cả hai sai, chỉ cascade đúng và chỉ baseline đúng. File dự đoán của từng mô hình có thể hỗ trợ phân tích này nếu đường dẫn ảnh và nhãn được ghép chính xác. Khi chưa tính, báo cáo giữ kết luận ở mức chênh kết quả quan sát.",
    "Độ tin cậy của điểm xác suất CNN cũng cần kiểm tra. Xác suất softmax cao không đảm bảo dự đoán đúng, đặc biệt với ảnh ngoài phân bố. Một số ảnh lỗi trong CSV có cnn_conf vượt 0,99 cho nhãn sai. Điều này cho thấy không nên trình bày 99% xác suất như 99% chắc chắn về bệnh. Nếu triển khai cho người dùng, cần khảo sát hiệu chuẩn xác suất và cơ chế cảnh báo khi ảnh nằm ngoài dữ liệu học."], 2)
section("5.6. Tốc độ, số hộp và chi phí tính toán", [
    "Benchmark cho hệ thống dùng cùng 291 ảnh nhưng số vùng cắt có thể lớn hơn rất nhiều. File throughput ghi 1.347 hộp và 1.339 vùng hợp lệ. Trung bình mỗi ảnh tạo khoảng 4,60 hộp, dù phân bố không đều: ảnh Healthy thường không có hộp, trong khi ảnh nhiều đốm tạo nhiều hộp. Do CNN phải chạy từng vùng, thời gian cấp ảnh phụ thuộc số hộp nhiều hơn số ảnh đơn thuần.",
    "Cặp EfficientNet-B2 có median khoảng 683,58 ms/ảnh, p90 khoảng 1.694,48 ms và p95 khoảng 2.434,80 ms trong file benchmark. Trung bình 973,48 ms cao hơn median vì có một số ảnh rất chậm, phù hợp với giả thuyết nhiều vùng cắt hoặc thử lại ngưỡng. ResNet50 có trung bình khoảng 475,40 ms và p95 khoảng 1.606,96 ms. Những percentile phản ánh trải nghiệm chờ của người dùng rõ hơn trung bình một mình.",
    "Các phép đo này ở môi trường notebook, gồm thời gian xử lý ảnh và dự đoán theo mã tại thời điểm đo. Chưa có so sánh cùng điều kiện trên server triển khai, trình duyệt và điện thoại. Khi báo cáo tốc độ trên thiết bị mới, phải ghi cách xử lý ảnh, số luồng, CPU/GPU, batch size, số lần warm-up và cách thống kê. Không thể dùng thời gian YOLO đơn lẻ 29,66 ms để quảng bá toàn ứng dụng xử lý trong 30 ms.",
    "Một hướng tối ưu có thể thử là gộp các vùng cắt thành batch, giới hạn số hộp được chuyển sang CNN hoặc chọn mô hình CNN nhẹ hơn. Mỗi thay đổi đều có thể tác động đến accuracy, đặc biệt ở ảnh có nhiều đốm nhỏ. Do đó, cải thiện tốc độ cần đi cùng phép đánh giá lại 291 ảnh và tập ngoài nguồn, tránh tối ưu theo thời gian mà làm tăng nguy cơ bỏ sót bệnh."], 2)
table("Phân vị thời gian xử lý từ benchmark 291 ảnh", ["Cấu hình", "Median (ms)", "P90 (ms)", "P95 (ms)", "Trung bình (ms)"], [
    ["YOLOv11m + VGG16", "197,32", "988,32", "1.561,23", "470,09"],
    ["YOLOv11m + ResNet50", "194,44", "1.043,13", "1.606,96", "475,40"],
    ["YOLOv11m + DenseNet121", "212,42", "1.039,70", "1.984,42", "510,96"],
    ["YOLOv11m + EfficientNet-B2", "683,58", "1.694,48", "2.434,80", "973,48"]], [6.0, 2.8, 2.8, 2.8, 3.4])
section("5.7. Thiết lập huấn luyện và khả năng tái lập", [
    "File args.yaml của YOLOv11m lưu cấu hình cụ thể: trọng số khởi tạo yolo11m.pt, 80 epoch tối đa, patience 20, batch 8, ảnh đầu vào 832 pixel, seed 42 và tùy chọn deterministic. Cấu hình có cosine learning rate, đóng mosaic ở 10 epoch cuối và dùng mixed precision. Đây là chi tiết cần đưa vào báo cáo để người đọc hiểu điều kiện tạo checkpoint, dù số epoch thực sự hoàn tất nên kiểm tra thêm trong results.csv.",
    "Notebook EfficientNet-B2 dùng ảnh 260 × 260 pixel, batch 32 và seed 42. Giai đoạn đầu có tối đa 8 epoch, learning rate 1×10⁻³; giai đoạn hai có tối đa 20 epoch, learning rate 5×10⁻⁵, mở 60 lớp cuối để fine-tune và dropout 0,35. Early stopping patience bằng 6, giảm learning rate sau 3 epoch không cải thiện. Việc dùng hai giai đoạn giúp trước hết ổn định đầu phân loại rồi điều chỉnh một phần backbone.",
    "Những tham số này là cấu hình notebook, không nhất thiết chứng minh mọi epoch đã chạy đủ. File history_stage1.csv, history_stage2.csv và stage*_done.json cho biết quá trình thực tế. Trong bản báo cáo nghiệm thu, nên lưu kèm phiên bản thư viện, phiên bản CUDA/GPU, thời điểm chạy và checksum checkpoint. Khi mô hình được xuất sang TFLite hoặc NCNN, bản xuất cần có mã phiên bản riêng vì kết quả số có thể thay đổi.",
    "Một người tái lập cần có ảnh nguồn, nhãn, notebook đúng phiên bản, môi trường Python và file cấu hình. Repo hiện có nhãn, báo cáo tiền xử lý và mô hình, nhưng không đóng gói toàn bộ ảnh gốc. Vì vậy, khả năng tái lập của người ngoài phụ thuộc quyền truy cập BDPapayaLeaf và việc khôi phục đường dẫn trong Colab. Báo cáo ghi rõ điều này thay vì nói toàn bộ thí nghiệm có thể chạy ngay từ bản repo hiện tại."], 2)
table("Một số tham số huấn luyện chính có trong project", ["Thành phần", "Thông số", "Giá trị"], [
    ["YOLOv11m", "Kích thước ảnh / batch", "832 px / 8"],
    ["YOLOv11m", "Epoch tối đa / patience", "80 / 20"],
    ["YOLOv11m", "Seed", "42"],
    ["EfficientNet-B2", "Kích thước ảnh / batch", "260 × 260 px / 32"],
    ["EfficientNet-B2", "Epoch giai đoạn 1 / 2", "8 / 20 tối đa"],
    ["EfficientNet-B2", "Learning rate giai đoạn 1 / 2", "1×10⁻³ / 5×10⁻⁵"],
    ["EfficientNet-B2", "Số lớp fine-tune / dropout", "60 lớp cuối / 0,35"]], [5.2, 6.5, 6.1])
section("5.8. Điều kiện để đánh giá ngoài vườn", [
    "BM02 nêu mục tiêu đánh giá khả năng thích nghi với ánh sáng và góc chụp ở vườn thực tế. Để kiểm tra mục tiêu này một cách có cơ sở, cần thiết kế một tập ảnh mới trước khi chọn mô hình và ngưỡng. Tập ảnh nên có nhiều điện thoại, nhiều giờ trong ngày, nền đất hoặc tán lá khác nhau, độ gần xa khác nhau và lá ở nhiều mức triệu chứng. Cần ghi mã cây, địa điểm và ngày chụp để tránh dùng những ảnh gần như giống nhau ở cả quá trình điều chỉnh và kiểm tra.",
    "Nhãn thực địa cần được kiểm tra bởi người có chuyên môn phù hợp. Nếu một ảnh không thể xác định chắc một bệnh duy nhất, nên gắn trạng thái không chắc hoặc nhiều nhãn thay vì ép vào một trong năm lớp. Một bộ test ngoài vườn nên báo cả tỉ lệ ảnh bị từ chối, số ảnh không có lá, lỗi tải ảnh và thời gian xử lý. Những số liệu này quan trọng cho phần mềm nhưng chưa hiện diện trong bộ kiểm thử nghiên cứu.",
    "Trên tập mới, cần giữ mô hình cố định rồi báo ma trận nhầm lẫn, precision, recall, F1 theo lớp, mAP nếu có hộp chuẩn và thời gian trên thiết bị định triển khai. Nếu kết quả thấp hơn tập BDPapayaLeaf, cần phân tích ảnh lỗi, so sánh phân bố và quyết định thu thêm dữ liệu hay tinh chỉnh. Không nên chỉnh mô hình theo tập test mới rồi vẫn gọi đó là kết quả kiểm thử độc lập.",
    "Cho đến khi quy trình này hoàn tất, báo cáo chỉ nêu khả năng ứng dụng tiềm năng, không khẳng định mô hình đã được xác nhận hoạt động ổn định ngoài vườn. Khoảng trống này là phần cần hoàn thiện trong giai đoạn phát triển tiếp, không làm mất giá trị của kết quả kiểm thử nội bộ đã báo cáo."], 2)
section("5.9. Hai trường hợp sai điển hình từ nhật ký dự đoán", [
    "Trường hợp thứ nhất là ảnh có nhãn thật Bacterial Spot nhưng hệ thống trả Ring Spot. Nhật ký dự đoán cho thấy ảnh có bốn hộp ở ngưỡng YOLO 0,50. Ba vùng cắt được CNN nhận là Ring Spot và một vùng được nhận là Bacterial Spot. Tổng điểm theo luật bỏ phiếu là khoảng 2,158 cho Ring Spot và 0,681 cho Bacterial Spot. Vì luật chọn lớp có tổng điểm cao nhất, kết quả ảnh sai dù một hộp lớn vẫn được nhận đúng lớp gốc.",
    "Trường hợp này làm rõ một đặc tính của phương pháp: số vùng cùng nhãn có thể tác động mạnh đến nhãn cuối. Không thể sửa lỗi chỉ bằng tăng độ chính xác của CNN đối với hộp đúng, vì hộp đúng đã có xác suất lớp Bacterial Spot rất cao. Cần kiểm tra vì sao ba hộp còn lại hướng sang Ring Spot: chúng có thể là đốm thực sự giống Ring Spot, vùng nhiễu bị YOLO giữ lại, hoặc một ảnh có nhiều kiểu biểu hiện nhưng nhãn cấp ảnh chỉ ghi Bacterial Spot. Ảnh nguồn sẽ quyết định cách giải thích.",
    "Một biến thể nghiên cứu là chỉ dùng vùng có diện tích lớn nhất hoặc dùng tối đa một số hộp sau khi lọc. Tuy nhiên, cách đó có thể bỏ sót bệnh khi vùng lớn là nền hoặc vết tổn thương không điển hình. Một biến thể khác là lấy trung bình điểm từng lớp thay vì cộng, giảm tác động của số hộp. Cả hai chỉ là giả thuyết cải tiến; báo cáo hiện tại không có bảng thực nghiệm cho chúng và không ghi chúng là giải pháp đã chứng minh.",
    "Trường hợp thứ hai là ảnh Ring Spot bị trả Healthy vì không có hộp sau khi hạ ngưỡng YOLO tới 0,35. File lỗi ghi reason no_yolo_box_after_conf_retry. CNN toàn ảnh trước đó cho nhãn Bacterial Spot với xác suất cao, nhưng theo nhánh suy luận đã thiết kế, khi các ngưỡng YOLO vẫn không tạo hộp, kết quả cuối được trả Healthy. Trường hợp này cho thấy một ảnh có tín hiệu bệnh ở CNN vẫn có thể bị mất cảnh báo do quyết định của khâu phát hiện.",
    "Ảnh Ring Spot khác bị trả Healthy ngay tại ngưỡng 0,50 khi CNN toàn ảnh nhận Healthy với xác suất khoảng 0,983. Hai trường hợp cùng tạo lỗi âm tính nhưng cơ chế khác nhau: một trường hợp bất đồng giữa CNN toàn ảnh và YOLO; trường hợp kia cả hai nhánh đều không tìm ra dấu hiệu đủ mạnh. Tách hai kiểu lỗi giúp chọn phép thử tiếp theo: thay luật không hộp cho trường hợp thứ nhất và thu thêm ảnh khó/điều chỉnh mô hình cho trường hợp thứ hai.",
    "Nhật ký còn có một ảnh Healthy bị gán Bacterial Spot vì YOLO phát hộp gần như toàn ảnh với độ tin cậy cao, CNN trên vùng này cho Bacterial Spot khoảng 0,831. Đây là lỗi dương tính giả ngay ở khâu phát hiện, không phải lỗi không có hộp. Tình huống này nhắc rằng độ tin cậy YOLO cao không bảo đảm hộp đúng trên dữ liệu ngoài lớp bệnh; phần mềm nên có chiến lược kiểm tra Healthy ở ảnh có hộp bất thường lớn.",
    "Các phân tích trên dùng số từ error_cases.csv và không thay thế quan sát ảnh gốc. File CSV lưu đường dẫn ảnh trong Colab nhưng repo hiện không chứa toàn bộ ảnh test. Trước khi in bản cuối, nếu nhóm có ảnh trên Google Drive, nên chèn ảnh của ít nhất một trường hợp bỏ sót bệnh và một trường hợp bỏ phiếu sai, cùng hộp và điểm của từng vùng. Nếu không lấy được ảnh, giữ bảng log và ghi rõ giới hạn kiểm tra trực quan."], 2)
table("Tóm tắt ba cơ chế lỗi được ghi trong file error_cases", ["Nhãn thật", "Nhãn cuối", "Thông tin log", "Vấn đề cần kiểm tra"], [
    ["Bacterial Spot", "Ring Spot", "4 hộp; tổng điểm Ring Spot 2,158 > Bacterial Spot 0,681", "Luật cộng điểm và chất lượng hộp nhỏ"],
    ["Ring Spot", "Healthy", "Không có hộp đến ngưỡng 0,35; CNN toàn ảnh cho nhãn bệnh", "Nhánh dự phòng khi YOLO bỏ sót"],
    ["Healthy", "Bacterial Spot", "YOLO tạo hộp gần toàn ảnh; CNN nhận Bacterial Spot", "Dương tính giả ở ảnh lành"]], [3.3, 3.3, 6.1, 5.1])

new_page()
h("CHƯƠNG 6. CHƯƠNG TRÌNH MÁY TÍNH VÀ KHẢ NĂNG ỨNG DỤNG")
section("6.1. Cấu trúc chương trình", [
    "Project gồm notebook nghiên cứu, thư mục outputs lưu mô hình và kết quả, dịch vụ API bằng FastAPI, giao diện web dùng Gradio và mã ứng dụng Android. Notebook 01 chuẩn bị dữ liệu; notebook 02 huấn luyện YOLOv11; notebook 03–05 huấn luyện EfficientNet; notebook 06 đánh giá quy trình; notebook 07 đo throughput; notebook 08 dùng để xuất mô hình cho Android. Cấu trúc này tách giai đoạn nghiên cứu khỏi giai đoạn phục vụ dự đoán.",
    "API nhận ảnh qua endpoint /predict, gọi mô hình phát hiện và phân loại, rồi trả kết quả gồm nhãn tổng hợp và thông tin vùng bệnh. Giao diện web gửi ảnh tới API và hiển thị kết quả. Các checkpoint .pt và .keras có sẵn trong outputs ở máy hiện tại; khi triển khai trên máy khác, cần đặt đúng đường dẫn và cài dependencies. Một bản demo nên có ảnh mẫu, hướng dẫn chạy và thông báo rõ đây là công cụ hỗ trợ nghiên cứu.",
    "Phần mềm không nên trình bày dự đoán như chẩn đoán xác nhận. Khi điểm tin cậy thấp hoặc ảnh kém chất lượng, giao diện nên khuyến nghị chụp lại và tham khảo người có chuyên môn. Dữ liệu đầu vào có thể chứa nền và vật thể ngoài lá; tiền kiểm ảnh hợp lệ là hướng cải thiện tiếp theo. Tài liệu vận hành cần ghi phiên bản mô hình và ngày xuất checkpoint để kết quả có thể truy vết."], 2)
section("6.2. Giao diện web và API", [
    "Mã api/src/index.py và web/app.py hiện diện trong repo. API có các đường dẫn /health, /models và /predict theo tài liệu api/README.md. Giao diện web dùng endpoint này để gửi file ảnh và hiển thị nhãn chuẩn hóa, xác suất cùng các dòng thông tin của vùng cắt. Đây là một bản triển khai có thể dùng để minh họa sản phẩm chương trình máy tính nếu cài đặt đúng môi trường và kiểm tra demo trước nghiệm thu.",
    "Bản báo cáo cuối nên có ảnh chụp màn hình thực tế của giao diện trong ba trường hợp: ảnh lành, ảnh bệnh phát hiện đúng và một ảnh khó. Mỗi ảnh chụp cần chỉ ra tên file hoặc mã ảnh, nhãn chuẩn và dự đoán. Project hiện có mã nguồn và kết quả mô hình, nhưng chưa có bộ ảnh chụp màn hình được xác nhận là phiên bản demo cuối. Do đó, báo cáo dành chỗ chèn minh chứng sau khi nhóm chốt giao diện.",
    "Để trình bày trước hội đồng, cần kiểm tra API khởi động được, mô hình tải đúng, trang web kết nối tới endpoint, thời gian phản hồi phù hợp và ảnh minh họa không chứa thông tin cá nhân. Nên chuẩn bị một bộ ảnh offline đề phòng mạng không ổn định. Đây là hoạt động xác nhận sản phẩm, khác với đánh giá học thuật trên tập test."], 2)
note("Chèn ảnh chụp màn hình giao diện web/API phiên bản dùng khi nghiệm thu và ghi cấu hình máy chạy demo.")
section("6.3. Tình trạng ứng dụng Android", [
    "Repo có dự án Android, một APK debug và notebook xuất mô hình. README của Android mô tả luồng suy luận dự kiến tương ứng với notebook đánh giá: YOLOv11m tìm hộp, EfficientNet-B2 phân loại vùng cắt, và luật dự phòng cho ảnh không có hộp. Tuy nhiên, thư mục AndroidApp/app/src/main/assets mới có README_MODELS.md, chưa có ba file yolo11m_papaya.param, yolo11m_papaya.bin và efficientnet_b2_papaya_float16.tflite cần cho suy luận offline.",
    "Do thiếu các file mô hình trong assets, sự tồn tại của APK debug chưa chứng minh ứng dụng Android dự đoán được ảnh. README cũng cho biết ứng dụng sẽ báo thiếu mô hình cho đến khi đủ ba file. Vì vậy, báo cáo đánh dấu Android là phần đang hoàn thiện, không dùng ảnh APK hiện tại làm minh chứng hoàn thành mục tiêu mobile. Các bước tiếp theo là chạy notebook xuất mô hình, đưa file vào assets, build lại, so sánh dự đoán Android với Python và đo thời gian trên thiết bị thật.",
    "Khi hoàn tất, nhóm cần lưu phiên bản APK, model, cấu hình xử lý ảnh, hệ điều hành, chip, RAM và kích thước ảnh đầu vào. Kiểm tra tối thiểu nên có ảnh Healthy, từng lớp bệnh, ảnh không tìm thấy hộp và ảnh có nhiều vùng. Kết quả trên Android có thể khác Python vì khác backend và độ chính xác số học, nên phải đo thay vì mặc nhiên kế thừa accuracy 94,85%."], 2)
note("Sau khi Android hoàn thành: chèn ảnh màn hình, bảng thời gian suy luận trên thiết bị, đối chiếu kết quả với 291 ảnh hoặc một tập kiểm thử cố định và mô tả sai khác nếu có.")
section("6.4. Khả năng ứng dụng và giới hạn", [
    "Trong phạm vi đã đo, sản phẩm có thể dùng để minh họa cách kết hợp phát hiện đối tượng với phân loại ảnh trong đào tạo và nghiên cứu nông nghiệp thông minh. Một người dùng có thể tải ảnh lá lên giao diện để xem vùng nghi ngờ cùng nhãn gợi ý. Cách sử dụng hợp lý là hỗ trợ quan sát ban đầu, theo dõi hoặc chọn ảnh cần chuyên gia xem lại. Không sử dụng nhãn tự động làm căn cứ duy nhất để mua hoặc phun thuốc.",
    "Giới hạn lớn nhất là phụ thuộc dữ liệu nguồn. Bộ kiểm thử cuối có 291 ảnh, lấy từ cùng hệ dữ liệu đã dùng để xây dựng nghiên cứu, chứ chưa phải bộ ảnh ngoài vườn được thu thập độc lập. Bệnh ở giai đoạn sớm, ảnh mờ, che khuất, đồng nhiễm hoặc điều kiện ánh sáng khác có thể làm hiệu năng giảm. Việc gán nhãn của bộ dữ liệu và độ chính xác hộp cũng có thể giới hạn trần hiệu năng của mô hình.",
    "Trước khi công bố một sản phẩm dùng trong vườn, cần thu ảnh nhiều địa điểm, mùa, giống, thiết bị và ánh sáng; có quy trình xác nhận nhãn bởi chuyên gia; giữ tập kiểm thử độc lập theo cây/vườn; đo độ nhạy với ảnh ngoài phân bố và độ tin cậy xác suất. Nếu dự kiến triển khai trên Android, cần cân bằng lại accuracy, độ trễ và bộ nhớ sau khi chuyển đổi mô hình."], 2)
section("6.5. Hợp đồng dữ liệu giữa giao diện và API", [
    "Giao diện web không chạy trực tiếp notebook huấn luyện. Nó gửi file ảnh tới API và nhận kết quả đã được chuẩn hóa. Việc tách hai phần giúp giao diện thay đổi độc lập với mô hình, đồng thời cho phép một thiết bị khác gọi cùng endpoint. Với mỗi yêu cầu, API cần kiểm tra file hợp lệ, mở ảnh, thực hiện các bước tiền xử lý theo phiên bản mô hình, chạy suy luận, gom kết quả và trả thông tin có thể hiểu được cho người dùng.",
    "Một bản phản hồi hữu ích không chỉ có nhãn cuối. Nó nên chứa trạng thái xử lý, nhãn, điểm tổng hợp, danh sách hộp, điểm YOLO và điểm CNN theo từng vùng. Những trường này giúp kiểm tra khi người dùng thắc mắc vì sao một ảnh được gán nhãn Ring Spot thay vì Anthracnose. Đối với báo cáo nghiệm thu, một ảnh chụp giao diện nên hiển thị chính ảnh đầu vào, hộp vùng bệnh và một bảng kết quả ngắn, tránh che mất đối tượng cần quan sát.",
    "Các nhãn nội bộ trong dữ liệu là BacterialSpot, Curl và RingSpot; giao diện chuẩn hóa thành Bacterial Spot, Leaf Curl và Ring Spot. Sự thay đổi tên hiển thị không được làm đổi thứ tự lớp của đầu ra CNN. Khi xuất mô hình hoặc tích hợp Android, cần giữ một file nhãn thống nhất, kiểm tra bằng ảnh có nhãn chuẩn của cả năm lớp và tránh sắp xếp lớp theo thứ tự bảng chữ cái nếu checkpoint dùng một thứ tự khác.",
    "Một yêu cầu ảnh có thể thất bại vì file không đọc được, mô hình chưa tải, thiếu bộ nhớ hoặc thời gian chờ quá lâu. Mã giao diện cần báo lỗi dễ hiểu, còn API cần ghi log kỹ thuật phục vụ nhóm sửa lỗi. Các lỗi hệ thống không được trả thành Healthy, vì như vậy người dùng có thể hiểu sự cố phần mềm là kết luận không có bệnh. Một bộ demo nên thử riêng nhánh lỗi trước khi trình bày."], 2)
section("6.6. Quy trình kiểm tra sản phẩm phần mềm", [
    "Kiểm tra chức năng bắt đầu từ một ảnh mẫu của từng lớp. Nhóm ghi lại đường dẫn ảnh, kích thước đầu vào, nhãn chuẩn, nhãn dự đoán, số hộp và thời gian chạy. Sau đó thử ảnh không có lá, file không phải ảnh, ảnh rất lớn và ảnh mờ. Trường hợp ảnh Healthy cần đặc biệt kiểm tra vì YOLO không học hộp cho lớp này; kết quả phải đi qua nhánh dự phòng đúng cách.",
    "Kiểm tra tái lập dùng cùng ảnh, cùng checkpoint và cùng cấu hình để so sánh notebook 06, API và giao diện web. Nếu ba nơi cho nhãn khác nhau, cần kiểm tra thứ tự lớp, cách đổi màu RGB/BGR, kích thước ảnh, chuẩn hóa đầu vào, ngưỡng YOLO và công thức gộp điểm. Việc demo thành công trên vài ảnh chỉ chứng minh luồng chức năng; nó không thay thế phép đánh giá trên toàn bộ 291 ảnh kiểm thử.",
    "Một vòng kiểm tra thực hành trước hội đồng gồm: khởi động API khi không có Internet, xác nhận checkpoint được đọc từ ổ đĩa, mở web trên trình duyệt, đưa từng ảnh vào, lưu ảnh màn hình và tắt dịch vụ an toàn. Nếu muốn trình diễn Android, cần cài APK đã đóng gói model và thử camera/tải ảnh trên điện thoại thật. Bản APK có sẵn hiện chưa đủ điều kiện này vì file mô hình xuất chưa nằm trong assets.",
    "Bảng kiểm sản phẩm không nhằm tuyên bố các bước chưa thực hiện đã hoàn thành. Nó cung cấp tiêu chí nghiệm thu cho nhóm: tên phép thử, dữ liệu vào, kết quả mong đợi, kết quả quan sát và bằng chứng. Chỉ sau khi điền kết quả quan sát mới chuyển mục từ chờ xác minh sang đạt. Cách ghi này giúp báo cáo tổng kết trung thực dù một nhánh triển khai còn đang phát triển."], 2)
table("Các phép kiểm tra cần ghi nhận cho phần mềm", ["Phép kiểm tra", "Bằng chứng cần lưu", "Trạng thái hiện tại"], [
    ["API khởi động và nạp mô hình", "Log /health, /models và phiên bản checkpoint", "Cần xác nhận trước nghiệm thu"],
    ["Ảnh từng lớp qua web", "Ảnh chụp màn hình và nhãn chuẩn", "Cần bổ sung"],
    ["Ảnh không hợp lệ", "Thông báo lỗi của web/API", "Cần bổ sung"],
    ["Đối chiếu 291 ảnh", "CSV dự đoán cùng cấu hình", "Có ở notebook; kiểm tra lại trên bản demo"],
    ["Android offline", "APK kèm model, ảnh kết quả, thời gian chạy", "Chưa hoàn thành"]], [5.5, 7.2, 5.1])
section("6.7. Quy tắc công bố kết quả trên giao diện", [
    "Một nhãn dự đoán từ ảnh không nên được diễn đạt như kết luận bệnh lý chắc chắn. Giao diện nên dùng cách nói “mô hình gợi ý” hoặc “ảnh giống lớp”, đồng thời hiển thị vị trí hộp để người dùng tự xem. Nếu ảnh thiếu nét, bị che hoặc không có lá đu đủ, hệ thống nên từ chối hoặc đề nghị chụp lại thay vì cố gắng đưa một trong năm nhãn bằng mọi giá.",
    "Điểm tin cậy CNN là đầu ra của mô hình; nó chưa được kiểm định như xác suất mắc bệnh ngoài thực tế. Những ví dụ sai trong error_cases.csv có điểm rất cao cho nhãn sai. Vì vậy, hiển thị phần trăm mà không giải thích có thể tạo cảm giác chắc chắn quá mức. Bản demo hội đồng có thể hiển thị điểm để minh họa thuật toán, nhưng phần giải thích phải nêu rõ giới hạn này.",
    "Việc lưu ảnh người dùng trên server cần có chính sách rõ ràng. Ảnh vườn có thể chứa thông tin vị trí hoặc con người ngoài ý muốn. Nếu chỉ cần suy luận, có thể xử lý tạm rồi xóa sau khi trả kết quả; nếu lưu để nghiên cứu, cần ghi nguồn và quyền sử dụng. Project hiện chưa có tài liệu chính sách dữ liệu cho một triển khai công khai, vì vậy báo cáo không mô tả hệ thống như dịch vụ đã sẵn sàng cho người dùng đại trà."], 2)
section("6.8. Đối chiếu sản phẩm đăng ký và bằng chứng cần nộp", [
    "Danh sách đăng ký đề tài SV2026-08 nêu ba sản phẩm: chương trình máy tính, báo cáo tổng kết và bài báo toàn văn tại hội thảo khoa học có ISBN/ISSN. Với chương trình máy tính, bằng chứng gồm mã nguồn, checkpoint và bản demo chạy được. Với báo cáo tổng kết, bằng chứng là cuốn đóng quyển theo phụ lục trường, có chữ ký của GVHD. Với bài báo, bằng chứng là toàn văn, giấy chấp nhận và thông tin hội thảo/xuất bản.",
    "Bản báo cáo tổng kết này sử dụng kết quả từ bài báo đã được duyệt, đồng thời giải thích chi tiết hơn về dữ liệu, phương pháp, kết quả và giới hạn. Nó không thay thế giấy chấp nhận đăng hay hợp đồng đã phê duyệt. Phần phụ lục cuối cuốn dành cho các minh chứng phải được nhóm điền đủ trước khi in và nộp. Một poster A3 được gấp và đóng ở cuối báo cáo theo phụ lục của trường; bản A1 dùng khi trình bày tại buổi nghiệm thu theo hướng dẫn BM07A.",
    "Bản cuối cần được GVHD rà soát sự thống nhất giữa BM02, bài báo, phần mềm và báo cáo. Những mục chưa có bằng chứng phải giữ ở trạng thái chưa hoàn thành hoặc chuyển thành kế hoạch sau nghiệm thu nếu trường cho phép. Nhóm cần kiểm tra tên đề tài, mã SV2026-08, tên thành viên, tên cơ quan, thuật ngữ YOLOv11 và EfficientNet-B2 trên tất cả minh chứng để tránh không thống nhất trong hồ sơ."], 2)

new_page()
h("CHƯƠNG 7. KẾ HOẠCH KIỂM CHỨNG VÀ HƯỚNG PHÁT TRIỂN")
section("7.1. Củng cố dữ liệu và nhãn", [
    "Kết quả hiện có cho thấy Anthracnose và Ring Spot là hai lớp cần chú ý ở khâu định vị. Hướng đầu tiên là rà soát nhãn hộp của các ảnh có mAP thấp hoặc nhiều hộp: hộp có bao đúng triệu chứng không, có bỏ qua đốm nhỏ không, và các ảnh cùng một kiểu triệu chứng có được gán nhãn nhất quán không. Việc sửa nhãn nên có nhật ký thay đổi và kiểm tra chéo giữa ít nhất hai người để giảm thiên lệch cá nhân.",
    "Thu thêm ảnh nên ưu tiên những trường hợp hệ thống sai thay vì chỉ tăng số ảnh dễ. Ví dụ cần ảnh bệnh giai đoạn sớm, tổn thương nhỏ, lá nhiều đốm, nền rối, bóng đổ và ảnh chụp thiết bị khác. Đối với Healthy, cần nhiều ảnh lá lành có biến thiên tự nhiên về tuổi, ánh sáng và dinh dưỡng để giảm báo động giả. Nếu chỉ thêm biến thể số từ cùng ảnh nguồn, số mẫu có thể tăng nhưng mức đa dạng sinh học không tăng tương ứng.",
    "Một thiết kế dữ liệu chặt hơn nên lưu mã cây, vườn, ngày chụp, camera, điều kiện sáng và cách xác nhận nhãn. Việc chia train, validation và test theo cây hoặc vườn sẽ khó hơn chia ngẫu nhiên theo file ảnh, nhưng đo được khả năng chuyển sang đối tượng mới rõ hơn. Những ảnh không chắc nhãn có thể được giữ trong tập rà soát thay vì ép vào lớp gần nhất."], 2)
section("7.2. Thử nghiệm biến thể của luật hợp nhất", [
    "Quy tắc hiện tại cộng điểm YOLO confidence × CNN confidence theo lớp. File lỗi cho thấy khi có nhiều hộp nhỏ cùng một nhãn sai, tổng của chúng có thể thắng hộp đúng. Một phép thử đối chứng có thể so sánh phương pháp hiện tại với lấy điểm lớn nhất, trung bình điểm theo lớp, trọng số theo diện tích hộp hoặc gộp các hộp gần nhau. Mỗi biến thể cần được định nghĩa trước trên tập validation, sau đó mới đánh giá trên tập test độc lập.",
    "Điểm của YOLO và CNN đến từ hai mô hình khác nhau, nên phép nhân không tự động là xác suất chung đã hiệu chuẩn. Có thể khảo sát chuẩn hóa hoặc hiệu chuẩn điểm, nhưng phải giữ mô hình và công thức cố định trước khi kiểm tra ngoài nguồn. Cải thiện accuracy trên 291 ảnh hiện tại không đủ bằng chứng nếu những ngưỡng mới được chọn chính từ 291 ảnh đó.",
    "Nhánh không có hộp cũng cần thử riêng. Một lựa chọn là luôn chạy CNN toàn ảnh cùng lúc để có một đối chứng, rồi quyết định bằng ngưỡng kép. Một lựa chọn khác là yêu cầu người dùng chụp lại khi độ tin cậy thấp. Các phương án này có tác động tới tốc độ và tỷ lệ từ chối, nên không chỉ so sánh accuracy mà cần đo cả recall bệnh, số báo động giả và thời gian xử lý."], 2)
section("7.3. Đánh giá tốc độ và chuyển đổi mô hình", [
    "Nếu mục tiêu là điện thoại, đầu tiên cần hoàn tất notebook 08 để xuất YOLOv11m sang NCNN và EfficientNet-B2 sang TFLite. Sau khi đưa file vào assets, kiểm tra thứ tự lớp và chuẩn hóa pixel bằng một bộ ảnh cố định. Kết quả Python và Android nên được so sánh cả ở mức hộp, xác suất vùng và nhãn cuối. Độ lệch nhỏ do số học có thể chấp nhận được, nhưng lỗi đổi thứ tự lớp hoặc đổi màu ảnh sẽ tạo sai khác lớn.",
    "Tiếp theo đo tốc độ trên thiết bị thật. Bảng đo cần ghi thời gian nạp mô hình, thời gian YOLO, số hộp, thời gian CNN, thời gian tổng và bộ nhớ đỉnh. Phải báo median và phân vị cao bên cạnh trung bình, vì ảnh có nhiều đốm có thể mất nhiều thời gian hơn ảnh đơn giản. Thiết bị demo nên được ghi rõ tên và cấu hình; không dùng benchmark notebook như thay thế số liệu điện thoại.",
    "Nếu độ trễ quá cao, có thể thử bản YOLOv11s hoặc n, giảm số vùng cắt, chạy CNN theo batch hoặc chọn CNN nhỏ hơn. Bảng so sánh YOLO cho thấy n và s nhanh hơn m trong phép đo đơn lẻ nhưng m có mAP tốt hơn. Mỗi thay đổi của giai đoạn phát hiện cần được đánh giá lại ở cấp hệ thống, bởi mAP tốt hơn không phải lúc nào cũng chuyển thành accuracy cao hơn theo cùng một mức."], 2)
section("7.4. Thiết kế phép thử thực địa", [
    "Một phép thử ngoài vườn nên bắt đầu bằng câu hỏi sử dụng rõ ràng: sàng lọc ảnh cần kiểm tra thêm, hay gợi ý lớp triệu chứng cho từng lá. Sau đó xác định cách chọn vườn, số cây, số ảnh mỗi cây và người xác nhận nhãn. Nếu ảnh từ một cây xuất hiện ở nhiều tập, độ chính xác có thể phản ánh sự giống nhau của nền và lá hơn là khả năng nhận ra bệnh trên cây mới.",
    "Các điều kiện ánh sáng nên được ghi bằng nhóm dễ hiểu như sáng trực tiếp, bóng râm, chiều tối và ánh sáng không đều. Góc chụp có thể phân biệt chính diện, nghiêng và che khuất một phần. Camera và khoảng cách chụp cũng cần ghi. Kết quả đánh giá sẽ có bảng theo nhóm điều kiện, cho phép xác định hệ thống yếu ở đâu thay vì chỉ có một số chung.",
    "Một số ảnh ngoài vườn có thể không thuộc năm nhãn huấn luyện hoặc có nhiều bệnh cùng lúc. Phép thử cần ghi rõ cách xử lý những ảnh này: loại khỏi đánh giá năm lớp, gắn nhãn không xác định, hay chuyển cho chuyên gia. Không nên ép chúng vào nhãn gần nhất rồi diễn giải sai số như lỗi thuần túy của mô hình. Một ứng dụng thực tế cần biết khi nào nên từ chối dự đoán.",
    "Nếu thu thập ảnh mới trước hạn nghiệm thu là bất khả thi, báo cáo giữ kế hoạch này ở phần kiến nghị. Không điền số liệu giả hay sử dụng ảnh từ Internet không rõ nguồn để tạo một bảng thử ngoài vườn. Hội đồng có thể đánh giá cao một giới hạn được mô tả trung thực và một thiết kế kiểm chứng rõ ràng hơn một kết quả không truy vết được."], 2)
section("7.5. Lộ trình hoàn thiện hồ sơ nghiệm thu", [
    "Trước khi nộp cuốn báo cáo, nhóm cần kiểm tra lại toàn bộ bảng và biểu đồ với file nguồn. Các hình đã chèn trong bản thảo được lấy từ outputs và readme; mỗi hình cần được xem ở bản in để bảo đảm chữ trong biểu đồ vẫn đọc được. Những vị trí có dấu CẦN BỔ SUNG cần được giải quyết một lần cuối: điền minh chứng thật hoặc giữ nguyên một ghi chú trung thực nếu nội dung chưa hoàn thành.",
    "Thông tin hành chính ở bìa và PL03 phải đúng với thuyết minh và hợp đồng đã ký. Danh mục bảng, hình và mục lục cần cập nhật số trang sau khi thêm ảnh, giấy chấp nhận và poster. Giảng viên hướng dẫn nên đọc bản hoàn chỉnh, nhận xét đóng góp của sinh viên trên PL03 và ký theo yêu cầu trường. Một bản in thử giúp phát hiện trang trắng, chữ bị cắt và hình nhỏ quá mức.",
    "Phần mềm demo nên chuẩn bị trước buổi nghiệm thu với một quy trình chạy ngắn, ảnh mẫu offline và bản dự phòng khi mạng không ổn định. Minh chứng bài báo gồm toàn văn, giấy chấp nhận, tên hội nghị, ISBN/ISSN và đường dẫn nếu đã có. Poster khổ A1 để trình bày và bản A3 để đóng cuối cuốn phải cùng một số liệu với báo cáo. Sau nghiệm thu, nhóm cập nhật tài liệu theo góp ý của hội đồng và thực hiện thủ tục thanh toán theo thông báo của Phòng KHCN."], 2)
section("7.6. Những câu hỏi có thể kiểm tra trực tiếp tại hội đồng", [
    "Một câu hỏi quan trọng là vì sao chọn YOLOv11m thay vì bản n hoặc s. Trả lời bằng bảng mAP và chi phí thời gian: bản m có mAP@0.5 cao nhất 77,67% trong ba bản, nhưng suy luận YOLO riêng chậm hơn. Sau đó giải thích lựa chọn này ưu tiên chất lượng vùng quan tâm cho bài toán nghiên cứu, còn triển khai trên thiết bị hạn chế vẫn cần cân nhắc bản nhỏ.",
    "Một câu hỏi khác là tại sao accuracy CNN 96,02% cao hơn accuracy hệ thống 94,85%. Hai phép thử dùng đơn vị khác nhau: 1.836 mẫu vùng cắt so với 291 ảnh gốc. Hệ thống còn chịu lỗi của YOLO và luật hợp nhất. Trả lời rõ điều này tránh tạo cảm giác số liệu mâu thuẫn và cho thấy nhóm hiểu đúng thiết kế thực nghiệm.",
    "Hội đồng cũng có thể hỏi liệu 94,85% đã chứng minh dùng được ngoài vườn. Câu trả lời dựa trên bằng chứng là chưa: kết quả lấy từ tập test nội bộ BDPapayaLeaf, chưa có khảo sát độc lập theo vườn và thiết bị. Giá trị của công trình hiện tại là một phương pháp và bản mẫu có kết quả tốt trong phạm vi dữ liệu; hướng phát triển là kiểm chứng ngoài hiện trường.",
    "Về sản phẩm Android, cần nói đúng trạng thái hiện thời. Repo có mã ứng dụng và APK debug, nhưng thiếu các file mô hình cần thiết trong assets nên chưa có bằng chứng suy luận offline hoàn chỉnh. Nếu trước nghiệm thu nhóm hoàn tất, nên cập nhật báo cáo bằng ảnh màn hình và số đo trên thiết bị; nếu không, dùng web/API làm chương trình minh họa và nêu Android là công việc tiếp theo."], 2)

new_page()
h("KẾT LUẬN VÀ KIẾN NGHỊ")
p("Nghiên cứu SV2026-08 đã xây dựng quy trình hai giai đoạn để phân tích ảnh lá đu đủ: YOLOv11m định vị vùng có dấu hiệu bệnh và EfficientNet-B2 phân loại vùng đó vào năm nhãn. Trong phạm vi BDPapayaLeaf, bộ phát hiện đạt mAP@0.5 77,67% và mAP@0.5:0.95 65,20%. Toàn bộ quy trình dự đoán đúng 276/291 ảnh kiểm thử, đạt accuracy 94,85% và macro F1 94,92%. So với EfficientNet-B2 phân loại ảnh toàn phần trên cùng 291 ảnh, accuracy của quy trình hai giai đoạn cao hơn 2,07 điểm phần trăm.")
p("Kết quả còn không đồng đều ở khâu định vị: Anthracnose và Ring Spot có mAP thấp hơn hai lớp bệnh còn lại. Quy trình cuối còn 15 ảnh phân loại sai. Thời gian đo trong notebook cho cặp YOLOv11m–EfficientNet-B2 xấp xỉ 973 ms/ảnh, cao hơn các cặp dùng VGG16, ResNet50 và DenseNet121. Những giới hạn này cho thấy lựa chọn mô hình cần căn cứ vào nhu cầu thực tế, đặc biệt nếu vận hành trên điện thoại.")
p("Về sản phẩm, mã nguồn nghiên cứu, checkpoint, báo cáo số liệu, API và giao diện web đã hiện diện trong project. Ứng dụng Android đang ở giai đoạn tích hợp mô hình, nên chưa được coi là kết quả triển khai hoàn chỉnh. Bài báo khoa học đã được nhóm thông báo chấp nhận đăng; hồ sơ nghiệm thu cần bổ sung giấy chấp nhận và thông tin hội thảo theo yêu cầu của trường.")
p("Kiến nghị tiếp theo là kiểm thử trên ảnh mới từ nhiều vườn và camera, đánh giá độ ổn định theo ánh sáng và góc chụp, nghiên cứu giảm bỏ sót các hộp nhỏ, và đo lại kết quả sau khi chuyển mô hình sang Android. Các kết quả kiểm thử bổ sung cần được thêm vào báo cáo bằng bảng có nguồn dữ liệu, cỡ mẫu, cách gán nhãn và cấu hình chạy rõ ràng.")

new_page()
h("TÀI LIỆU THAM KHẢO")
paper = fitz.open(PAPER)
ref_text = paper[-1].get_text().split("REFERENCES", 1)[-1]
parts = re.split(r"(?=\[\d+\])", ref_text)
for part in parts:
    s = " ".join(part.split())
    if re.match(r"^\[\d+\]", s):
        q = p(s)
        q.paragraph_format.first_line_indent = Cm(-0.5)
        q.paragraph_format.left_indent = Cm(0.5)

new_page()
h("PHỤ LỤC A. HỒ SƠ MINH CHỨNG SẢN PHẨM")
p("A.1. Toàn văn bài báo: “A Two-Stage Deep Learning Cascade Framework for Robust Papaya Leaf Disease Detection and Classification”, bản thảo 6 trang lưu tại docs/paper/GTSD2026-148-IEEE (1).pdf. In toàn văn và đóng sau phần tài liệu tham khảo hoặc đính kèm theo yêu cầu của Phòng KHCN.")
note("Chèn giấy/email chấp nhận đăng, tên hội nghị và minh chứng ISBN/ISSN; kiểm tra thống nhất tên tác giả, cơ quan và mã tài trợ SV2026-08 với bản công bố cuối.")
p("A.2. Sản phẩm phần mềm: mã nguồn trong api/, web/, notebooks/ và AndroidApp/; checkpoint trong outputs/yolo/yolov11_m/weights/ và outputs/cnn/efficientnet_b2/. Chuẩn bị bản trình diễn web/API hoặc bản Android đã hoàn thiện cùng hướng dẫn vận hành.")
note("Chèn bản sao thuyết minh BM02 và hợp đồng đã phê duyệt theo mục 3.14 của Phụ lục hướng dẫn; chèn poster A3 đã gấp vào cuối cuốn báo cáo.")
new_page()
h("PHỤ LỤC B. DANH MỤC FILE KẾT QUẢ ĐỂ ĐỐI CHIẾU")
for entry in [
    "data/reports/preprocessing/21_notebook* — số lượng và cách chia dữ liệu.",
    "outputs/yolo/reports/final_yolo_comparison.csv — so sánh các biến thể YOLO.",
    "outputs/yolo/test_evaluations/yolov11_m/per_class_metrics_test.csv — chỉ số phát hiện theo lớp.",
    "outputs/cnn/reports/final_cnn_comparison.csv — so sánh EfficientNet.",
    "outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/summary.json — chỉ số hệ thống cuối.",
    "outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/classification_report.csv — chỉ số theo lớp.",
    "outputs/pipeline_evaluation_baselines/all_pipeline_summary_baselines_sorted.csv — đối chứng CNN.",
    "outputs/Performance_Benchmark/model_throughput_20260703_155451.csv — tốc độ xử lý.",
]:
    p(entry)

OUT.parent.mkdir(exist_ok=True)
doc.save(OUT)
print(OUT)
print("figures", len(figures), "tables", len(tables), "paragraphs", len(doc.paragraphs))
