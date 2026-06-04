# Dataset Notes

## Classes

The project uses five final classification classes:

| Class | Used by YOLO detector | Used by CNN classifier |
| --- | --- | --- |
| Anthracnose | Yes | Yes |
| Bacterial Spot | Yes | Yes |
| Leaf Curl | Yes | Yes |
| Ring Spot | Yes | Yes |
| Healthy | No | Yes |

Healthy leaves do not have disease bounding boxes, so they are included in the CNN classification stage but not in YOLO detection training.

## Local Annotation Dump

YOLO label files are stored in `data/annotations/yolo_bbox/`.

| Folder | Label files |
| --- | ---: |
| `anthracnose/` | 355 |
| `bacterial_spot/` | 458 |
| `leaf_curl/` | 364 |
| `ring_spot/` | 533 |

The individual label filenames intentionally preserve their original stems, for example `Anthracnose(1).txt`. YOLO image-label pairing depends on matching filename stems, so the annotation files were not renamed individually.

## Preprocessing Reports

`data/reports/preprocessing/` contains the data audit and split artifacts generated during dataset preparation, including image manifests, label manifests, duplicate checks, warning reports, and final CNN/YOLO split manifests.

## Recreating the Full Training Data

The original image files are not included in this repository. To rerun the project end to end:

1. Download or restore the BDPapayaLeaf images.
2. Place raw data under a local `data/raw/` folder or adjust the Colab notebooks to your dataset path.
3. Run `notebooks/01_data_preparation.ipynb` to regenerate detection and classification splits.
4. Continue with YOLO and CNN training notebooks.
