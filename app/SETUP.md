# Thiết lập Android

## Yêu cầu

- Node.js 22 trở lên, JDK 21, Android Studio/SDK và NDK.
- Thiết bị Android hoặc emulator có ít nhất vài GB bộ nhớ trống. Bản debug chứa bốn ABI cùng TensorFlow Select TF Ops nên khá lớn.
- Các model đã nằm trong `app/models/`; không cần tải model khi chạy ứng dụng.

## Chạy bản phát triển

Trong PowerShell:

```powershell
cd app
npm install
npx expo prebuild --platform android
npx expo run:android
```

`prebuild` đồng bộ package Android từ `app.json` và tự liên kết module `modules/papaya-inference`. Sau khi thay model hoặc mã Kotlin/C++, hãy build lại bằng `npx expo run:android`; Expo Go không chứa module native này. Bản debug dùng Metro khi phát triển, nên điện thoại cần kết nối với máy tính đang chạy Metro.

## Tạo bản chạy độc lập

Từ `app/android`:

```powershell
./gradlew.bat :app:assembleRelease
```

APK release chứa JavaScript, model NCNN, model TFLite và các thư viện native; phân tích ảnh không cần Internet. Trước khi phát hành, cần cấu hình khóa ký release của riêng bạn và kiểm tra trên điện thoại thật. Các bản phân phối theo ABI sẽ nhỏ hơn APK debug gộp bốn ABI.

## Kiểm tra

```powershell
cd app
npx expo lint
npx tsc --noEmit
```

Nếu `npx expo run:android` báo không tìm thấy Android SDK, đặt biến `ANDROID_HOME` tới thư mục SDK (thường là `%LOCALAPPDATA%\Android\Sdk`) rồi mở lại terminal. Xem thêm [README.md](README.md) và [models/README.md](models/README.md).
