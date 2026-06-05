# Papaya Leaf API

FastAPI inference service for the YOLOv11m -> EfficientNetB2 cascade.

## Run locally

```powershell
cd api
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.index:app --host 0.0.0.0 --port 8000
```

Open:

- `GET http://localhost:8000/health`
- `GET http://localhost:8000/models`
- `POST http://localhost:8000/predict` with form-data field `file`

Example:

```powershell
Invoke-RestMethod `
  -Uri http://localhost:8000/predict `
  -Method Post `
  -Form @{ file = Get-Item "path\to\leaf.jpg" }
```

## Model files

By default the API uses these local paths:

- YOLOv11m: `outputs/yolo/yolov11_m/weights/best.pt`
- EfficientNetB2: `outputs/cnn/efficientnet_b2/best_model.keras`

If either file is missing, the API downloads it from Google Drive using the file IDs already configured in `src/index.py`.

Useful environment variables:

```powershell
$env:YOLO_MODEL_PATH="C:\path\to\best.pt"
$env:CNN_MODEL_PATH="C:\path\to\best_model.keras"
$env:YOLO_DRIVE_SOURCE="11AGUogBofR0hayelb804A_2SqZwGmwCW"
$env:CNN_DRIVE_SOURCE="1pxd6ORKrs7qhEDsfaTlLKWqMWnLKi0cj"
$env:MODEL_AUTO_DOWNLOAD="true"
$env:LOAD_MODELS_ON_STARTUP="true"
```

The Google Drive files must be shared as "Anyone with the link".

## Docker

Build from the `api` folder:

```powershell
docker build -t papaya-leaf-api .
docker run --rm -p 8000:8000 papaya-leaf-api
```
