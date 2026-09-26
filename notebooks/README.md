# Notebook Guide

The main notebooks are ordered by the project workflow:

| Order | Notebook | Purpose |
| ---: | --- | --- |
| 1 | `01_data_preparation.ipynb` | Clean source data and build YOLO/CNN splits |
| 2 | `02_train_yolov11_detector.ipynb` | Train YOLOv11 disease-region detectors |
| 3 | `03_train_efficientnet_b0_classifier.ipynb` | Train EfficientNetB0 classifier |
| 4 | `04_train_efficientnet_b1_classifier.ipynb` | Train EfficientNetB1 classifier |
| 5 | `05_train_efficientnet_b2_classifier.ipynb` | Train EfficientNetB2 classifier |
| 6 | `06_evaluate_yolov11_efficientnet_cascade.ipynb` | Evaluate the YOLOv11 + EfficientNet cascade |
| 7 | `07_benchmark_model_throughput_colab.ipynb` | Benchmark cascade inference throughput on the notebook 06 test set |
| 8 | `08_export_android_models_colab.ipynb` | Export YOLOv11m to NCNN and EfficientNet-B2 to TFLite for the Android app |

Baseline notebooks are stored in `baselines/`:

| Notebook | Purpose |
| --- | --- |
| `train_densenet121_classifier.ipynb` | CNN baseline with DenseNet121 |
| `train_resnet50_classifier.ipynb` | CNN baseline with ResNet50 |
| `train_vgg16_classifier.ipynb` | CNN baseline with VGG16 |
| `train_full_image_efficientnet_b2_baseline.ipynb` | CNN-only baseline on full images |
| `evaluate_yolov11_cnn_baselines.ipynb` | Cascade evaluation with baseline CNN backbones |

These notebooks were exported from Google Colab and still use Colab/Google Drive paths. Update `PROJECT_ROOT`, `PREP_ROOT`, and model output paths before running them in another environment.
