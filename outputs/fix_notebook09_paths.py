import json
from pathlib import Path

path = Path('notebooks/09_export_annotated_error_cases_colab.ipynb')
nb = json.loads(path.read_text(encoding='utf-8'))
def update(i, old, new):
    text = ''.join(nb['cells'][i]['source'])
    assert old in text, (i, old)
    nb['cells'][i]['source'] = text.replace(old, new).splitlines(keepends=True)

update(3, 'def annotate(row, idx):', '''def resolve_image_path(row):
    """Preserve the dataset location recorded during evaluation."""
    original = Path(str(row["image_path"]).replace("\\\\", "/"))
    candidates = []
    parts = original.parts
    if "prepared_data_v1" in parts:
        candidates.append(PROJECT_ROOT.joinpath(*parts[parts.index("prepared_data_v1"):]))
    candidates.append(original)
    if row["true_class"] == "Healthy":
        candidates.append(PROJECT_ROOT / "prepared_data_v1" / "cnn_dataset" /
                          "test" / "Healthy" / original.name)
    else:
        candidates.append(Path(IMAGES_DIR) / original.name)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("Thiếu ảnh gốc: " + original.name +
                            "\\nĐã tìm:\\n" + "\\n".join(map(str, candidates)))

def annotate(row, idx):''')
update(3, 'src = os.path.join(IMAGES_DIR, os.path.basename(row["image_path"]))',
       'src = resolve_image_path(row)')
update(4, 'shutil.rmtree(OUT_DIR, ignore_errors=True)', '''# Validate all original images before replacing any exported results.
missing = []
for _, row in df.iterrows():
    try:
        resolve_image_path(row)
    except FileNotFoundError as exc:
        missing.append(str(exc))
if missing:
    raise FileNotFoundError("Không thể xuất đủ 15 ca.\\n\\n" + "\\n\\n".join(missing))

shutil.rmtree(OUT_DIR, ignore_errors=True)''')
update(6, 'zip_base = "/content/annotated_errors_effb2"', '''case_files = list(Path(OUT_DIR).glob("ca*_gt-*_pred-*.png"))
required = ["hinh_5_5_2_1_gt-Healthy_pred-BacterialSpot.png",
            "hinh_5_5_2_2_gt-BacterialSpot_pred-Curl.png", "bang_anh_15_ca_sai.png"]
if len(case_files) != 15 or not all((Path(OUT_DIR) / name).is_file() for name in required):
    raise RuntimeError("Kết quả chưa đủ 15 ca và hình báo cáo. Chạy lại cell 4 và 5.")

zip_base = "/content/annotated_errors_effb2"''')
update(0, '1. Google Drive đã gắn, có thư mục `Papaya_Leaf_Disease_Classification/prepared_data_v1/yolo_dataset/images/test/`.',
       '1. Google Drive đã gắn, có ảnh bệnh trong `prepared_data_v1/yolo_dataset/images/test/` và ảnh lá khỏe trong `prepared_data_v1/cnn_dataset/test/Healthy/` của dự án.')
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('Updated', path)
