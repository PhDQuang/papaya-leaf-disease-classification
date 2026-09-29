# Android model assets

These six files are bundled into the Android APK by `modules/papaya-inference/android/build.gradle`. They were copied from the repository's `papaya_android_models/` export:

| File | Runtime | Purpose |
| --- | --- | --- |
| `yolo11m_papaya.param`, `yolo11m_papaya.bin` | NCNN | Four disease boxes, input 832 × 832 |
| `efficientnet_b2_papaya_float16.tflite` | TensorFlow Lite + Select TF Ops | Five class classifier, float32 RGB input 260 × 260 in the 0–255 range |
| `papaya_android_config.json` | Android module | Class order and cascade thresholds |
| `papaya_yolo_labels.txt`, `papaya_cnn_labels.txt` | Reference | Exported label order |

The TFLite file includes Flex operations. The local Expo module therefore bundles both `tensorflow-lite` and `tensorflow-lite-select-tf-ops`; removing the latter will break model loading. The NCNN Android SDK lives under `modules/papaya-inference/android/third_party/ncnn` and is used for CPU inference. Its license is included there.

When replacing a model, update the corresponding files here and rebuild the Android app. JavaScript hot reload cannot replace bundled native assets. Keep the input shapes, output shapes, NCNN layer names (`in0`, `out0`), class order, and config in sync with the new export.
