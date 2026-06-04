# Output Artifacts

This directory stores trained model artifacts, metrics, plots, and prediction reports.

## Layout

| Folder | Contents |
| --- | --- |
| `cnn/` | EfficientNetB0/B1/B2 classifier training outputs |
| `cnn_baselines/` | DenseNet121, ResNet50, VGG16, and VGG19 baseline outputs |
| `cnn_full_image_baselines/` | CNN-only full-image baseline outputs |
| `yolo/` | YOLOv11 detector training outputs and test evaluations |
| `pipeline_evaluation/` | YOLOv11 + EfficientNet cascade results |
| `pipeline_evaluation_baselines/` | YOLOv11 + baseline CNN cascade results |

## GitHub Upload Note

Checkpoint files such as `*.keras` and `*.pt` are ignored by `.gitignore`. Several checkpoints exceed normal GitHub file-size limits, especially the ResNet50 `.keras` files.

Metrics, confusion matrices, history CSVs, and comparison plots can be committed normally. If model weights need to be published, use Git LFS or attach them to a GitHub Release.
