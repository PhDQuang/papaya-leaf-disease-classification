# Experiment Results

This page summarizes the main metrics kept in `outputs/`.

## YOLO Detector Comparison

Source: `outputs/yolo/reports/final_yolo_comparison.csv`

| Detector | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | Inference ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| YOLOv11m | 0.8024 | 0.8162 | 0.7767 | 0.6520 | 29.66 |
| YOLOv11s | 0.8132 | 0.8089 | 0.7657 | 0.6446 | 10.83 |
| YOLOv11n | 0.7461 | 0.7563 | 0.7471 | 0.6126 | 7.24 |

YOLOv11m was selected for the final cascade because it gave the best mAP@0.5 and mAP@0.5:0.95 among the tested detector variants.

## Full Cascade and Baseline Comparison

Sources:

- `outputs/cnn_full_image_baselines/efficientnet_b2_full_image/test_summary.json`
- `outputs/pipeline_evaluation/all_pipeline_summary_sorted.csv`
- `outputs/pipeline_evaluation_baselines/all_pipeline_summary_baselines_sorted.csv`

| Model | Accuracy | Macro precision | Macro recall | Macro F1 |
| --- | ---: | ---: | ---: | ---: |
| EfficientNetB2 full-image baseline | 0.9278 | 0.9317 | 0.9286 | 0.9293 |
| YOLOv11m + VGG16 | 0.9347 | 0.9288 | 0.9423 | 0.9328 |
| YOLOv11m + DenseNet121 | 0.9416 | 0.9372 | 0.9473 | 0.9409 |
| YOLOv11m + ResNet50 | 0.9450 | 0.9393 | 0.9476 | 0.9426 |
| YOLOv11m + EfficientNetB2 | 0.9485 | 0.9492 | 0.9493 | 0.9492 |

The final YOLOv11m + EfficientNetB2 cascade correctly predicted 276 out of 291 test images.

## Class-Level Metrics for Final Cascade

Source: `outputs/pipeline_evaluation/yolov11_m__efficientnet_b2/classification_report.csv`

| Class | Precision | Recall | F1-score | Support |
| --- | ---: | ---: | ---: | ---: |
| Anthracnose | 0.9273 | 0.9444 | 0.9358 | 54 |
| Bacterial Spot | 0.9701 | 0.9420 | 0.9559 | 69 |
| Leaf Curl | 0.9815 | 0.9815 | 0.9815 | 54 |
| Healthy | 0.9412 | 0.9412 | 0.9412 | 34 |
| Ring Spot | 0.9259 | 0.9375 | 0.9317 | 80 |

## Notes

Some JSON and CSV files still contain original Colab paths in metadata, for example `/content/drive/MyDrive/...`. These paths document the training environment and do not affect the stored metrics.
