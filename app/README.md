# Papaya Leaf AI (Android)

Ứng dụng Expo/React Native phân tích lá đu đủ hoàn toàn trên thiết bị Android. Có thể chụp hoặc chọn ảnh, chạy YOLO11m để tìm vùng bệnh, dùng EfficientNet-B2 phân loại từng vùng, xem bounding box theo màu nhãn, và lưu ảnh đã đánh dấu cùng lịch sử trong bộ nhớ máy. Người dùng cũng có thể gán nhãn thủ công.

## Chạy ứng dụng

Mở PowerShell trong thư mục `app`:

```powershell
npm install
npx expo run:android
```

Cần Android SDK, NDK và thiết bị hoặc emulator. Sau khi thêm hoặc thay model, phải build lại native app. **Expo Go không chạy được module NCNN/TFLite này.** Bản debug cần Metro khi phát triển; bản release chứa JavaScript và model nên có thể chạy không cần Internet.

## Model

Các file xuất từ `../papaya_android_models` đã nằm trong `models/`. Module native ở `modules/papaya-inference/` dùng NCNN cho YOLO và TensorFlow Lite kèm Select TF Ops cho EfficientNet. Ngưỡng, thứ tự nhãn và kích thước đầu vào ở `models/papaya_android_config.json`; xem [models/README.md](models/README.md) để thay model.

YOLO chạy một lần với ngưỡng thấp nhất, sau đó ứng dụng áp dụng ngưỡng ban đầu 0.5 và các ngưỡng thử lại 0.45/0.4/0.35 theo cấu hình. Kết quả được NMS, cắt vùng, phân loại, và trả về box theo tọa độ chuẩn hóa của ảnh gốc. `Healthy` không có box. Mọi tính toán và dữ liệu lịch sử đều ở máy; ứng dụng không tải ảnh lên máy chủ.

## Kiểm tra

```powershell
npx expo lint
npx tsc --noEmit
cd android
./gradlew.bat :app:assembleDebug
```

Ảnh gốc, ảnh đã vẽ box và metadata lịch sử được lưu trong bộ nhớ ứng dụng. Nếu xóa dữ liệu ứng dụng, lịch sử cũng bị xóa.
