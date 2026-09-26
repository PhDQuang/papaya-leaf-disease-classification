# Hướng Dẫn Thiết Lập Môi Trường Phát Triển & Chạy WIM Mobile

Tài liệu này hướng dẫn chi tiết cách thiết lập môi trường máy tính để tải về, biên dịch mã nguồn native và khởi chạy ứng dụng **WIM Mobile** trên cả hai nền tảng:
- **I. Android** (Máy tính Windows hoặc macOS)
- **II. iOS** (Máy tính macOS với Xcode)

---

# I. THIẾT LẬP MÔI TRƯỜNG ANDROID (WINDOWS)

## 1. Yêu Cầu Tiên Quyết (Prerequisites)

1. **Node.js**: Node.js **v22.13.x hoặc mới hơn** theo yêu cầu của Expo SDK 57 & `npm`.
   - Kiểm tra: `node -v` và `npm -v`.
2. **Android Studio**:
   - Tải từ trang chủ: [developer.android.com/studio](https://developer.android.com/studio).
   - Trong quá trình cài đặt, tích chọn: **Android SDK**, **Android SDK Platform**, và **Android Virtual Device (AVD)**.
3. **Java Development Kit (JDK 21 LTS)**:
   - **Khuyến nghị**: Cài đặt **Eclipse Temurin JDK 21 (Adoptium)**.
   - *Lưu ý quan trọng*: Hệ sinh thái Android Gradle Plugin (AGP) hiện tại tương thích ổn định nhất với JDK 17 hoặc JDK 21. **Không sử dụng JDK 25 hay JDK 26** vì sẽ gặp lỗi không tương thích phiên bản class file khi build Gradle.
   - Cài nhanh trên Windows PowerShell:
     ```powershell
     winget install EclipseAdoptium.Temurin.21.jdk
     ```

---

## 2. Cấu Hình Biến Môi Trường (Environment Variables)

Để terminal và Gradle nhận diện được Android SDK và JDK, cần thiết lập các biến môi trường sau trên Windows.

Mở **PowerShell** và chạy các lệnh dưới đây (chỉ cần chạy 1 lần):

```powershell
# 1. Thiết lập ANDROID_HOME (thường nằm ở AppData)
[Environment]::SetEnvironmentVariable("ANDROID_HOME", "$env:LOCALAPPDATA\Android\Sdk", "User")

# 2. Thiết lập JAVA_HOME trỏ tới Eclipse Temurin JDK 21
[Environment]::SetEnvironmentVariable("JAVA_HOME", "C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot", "User")

# 3. Thêm platform-tools (adb) và emulator vào biến PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$sdkPaths = "$env:LOCALAPPDATA\Android\Sdk\platform-tools;$env:LOCALAPPDATA\Android\Sdk\emulator"
if ($userPath -notlike "*platform-tools*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$sdkPaths", "User")
}
```

> **Sau khi chạy lệnh**: Hãy **tắt và mở lại VSCode/Terminal** để nạp biến môi trường mới.
> Kiểm tra lại bằng lệnh:
> ```powershell
> adb --version
> java -version
> ```

---

## 3. Thiết Lập & Khởi Động Máy Ảo Android (AVD)

1. Mở **Android Studio** -> Vào menu **Device Manager**.
2. Nhấn **Create Device** (chọn *Medium Phone* hoặc *Pixel 7/8*).
3. Chọn System Image (khuyến nghị Android 14 hoặc Android 15/16 - API 34+ với Google Play/Google APIs).
4. Đặt tên thiết bị (ví dụ: `Medium_Phone`) và hoàn tất.

### Khởi động máy ảo từ Terminal:

```powershell
# Mở ngầm máy ảo ra một cửa sổ độc lập
Start-Process "$env:LOCALAPPDATA\Android\Sdk\emulator\emulator.exe" -ArgumentList "-avd Medium_Phone"

# Mở trực tiếp máy ảo bằng emulator (nếu đã có trong PATH)
emulator -avd Medium_Phone
```

---

## 4. Biên Dịch & Chạy Ứng Dụng Android

```bash
cd wim-mobile
npm install

# Tạo .env từ mẫu và thay bằng domain HTTPS của WIM UAT
Copy-Item .env.example .env
# EXPO_PUBLIC_WIM_API_BASE_URL=https://<WIM_DOMAIN>

# Build mã nguồn native và cài đặt lên máy ảo Android lần đầu:
npx expo run:android

# Khởi chạy trong các lần tiếp theo:
npm run android
# hoặc: npx expo start --dev-client
```

Ứng dụng Android v1 dành cho tài khoản `operator`, chỉ hỗ trợ nghiệp vụ kho
nhận hàng, cất hàng, lấy hàng và chuyển vị trí. Ứng dụng dùng camera điện thoại
để quét mã, hoạt động online-only và không lưu API key trong file `.env`.

---

# II. THIẾT LẬP MÔI TRƯỜNG IOS (MACOS)

Phát triển ứng dụng iOS yêu cầu máy tính chạy **macOS** (MacBook, Mac mini, iMac, Mac Studio...).

---

## 1. Yêu Cầu Tiên Quyết Cho iOS

1. **Xcode**:
   - Cài đặt từ Mac App Store hoặc tải file `.xip` từ [developer.apple.com/download/all](https://developer.apple.com/download/all).
2. **Homebrew**:
   - Trình quản lý gói cho macOS (nếu máy chưa có, cài tại [brew.sh](https://brew.sh)).
3. **CocoaPods**:
   - Trình quản lý thư viện native iOS (bắt buộc cho React Native & Expo Development Build):
     ```bash
     brew install cocoapods
     ```
   - Kiểm tra sau khi cài: `pod --version`.
4. **Node.js**: Phiên bản LTS (`node -v` và `npm -v`).

---

## 2. Kích Hoạt Xcode & Tải iOS Simulator Runtime

Mở Terminal trên máy Mac và thực hiện các bước sau:

### Bước 1: Kích hoạt công cụ dòng lệnh của Xcode
```bash
# Trỏ CommandLineTools vào Xcode chính
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

# Cấp phép cài đặt các package hệ thống bổ trợ
sudo xcodebuild -runFirstLaunch

# Chấp thuận bản quyền Xcode
sudo xcodebuild -license accept
```

### Bước 2: Tải iOS Simulator Runtime
1. Mở ứng dụng **Xcode**.
2. Vào **Xcode** > **Settings...** (`Cmd + ,`) > chọn tab **Components** (hoặc **Platforms**).
3. Kiểm tra mục **iOS (phiên bản mới nhất, ví dụ iOS 18/27)**: Nếu chưa có hoặc hiện nút `Get`, nhấn tải về (~8 GB).
4. Sau khi tải xong, bạn có thể kiểm tra danh sách máy ảo có sẵn:
   ```bash
   xcrun simctl list devices available
   ```

---

## 3. Cấu Hình Bắt Buộc Cho iOS (Scene Lifecycle)

Trên các phiên bản iOS mới (từ iOS 27+ / Xcode 27), Apple bắt buộc các ứng dụng phải áp dụng kiến trúc **Scene Lifecycle** (`UIScene`). Nếu thiếu, app sẽ bị văng (crash) ngay khi mở với mã lỗi `___UIApplicationEvaluateRuntimeIssueForNoSceneLifecycleAdoption`.

Dự án đã được cấu hình sẵn trong `app.json`:
```json
{
  "expo": {
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.tcap.wimmobile"
    },
    "plugins": [
      [
        "expo-build-properties",
        {
          "ios": {
            "enableSceneSupport": true
          }
        }
      ]
    ]
  }
}
```

---

## 4. Biên Dịch & Chạy Ứng Dụng Trên iOS Simulator

Di chuyển vào thư mục `wim-mobile`:

```bash
cd wim-mobile

# 1. Cài đặt các package dependencies
npm install

# 2. Sinh mã nguồn native iOS (chứa UISceneDelegate tương thích iOS 27+)
npx expo prebuild --clean

# 3. Biên dịch và khởi chạy app lên máy ảo iPhone
npx expo run:ios
```

### Khởi chạy trong các lần phát triển tiếp theo:
Khi app đã được cài sẵn icon trên máy ảo, các lần làm việc sau chỉ cần chạy:

```bash
npm run ios
# hoặc: npx expo start --dev-client
```

---

## 5. Các Lưu Ý Quan Trọng Khi Phát Triển

### 1. Kết nối API Backend WIM (NestJS / ERPNext)
Ứng dụng chỉ nhận base URL HTTPS của WIM UAT trong `EXPO_PUBLIC_WIM_API_BASE_URL`:
```ts
const BASE_URL = "https://wim-uat.example.com";
```

### 2. Phím Tắt Hữu Ích Trên iOS Simulator
- **`Cmd + R`**: Tải lại ứng dụng (Reload JS Bundle).
- **`Cmd + D`**: Mở Developer Menu của Expo / React Native.
- **`Cmd + Shift + H`**: Quay về màn hình chính (Home).
- **`Cmd + K`**: Bật / tắt bàn phím mềm ảo khi đang focus ô nhập liệu.

### 3. Khắc Phục Lỗi Thường Gặp (Troubleshooting)

- **Lỗi `open -a Simulator: Unable to find application named 'Simulator'`**:
  - Khắc phục: Mở Xcode -> menu **Xcode** -> **Open Developer Tool** -> **Simulator**. Sau lần mở này, macOS sẽ nhận diện app Simulator bình thường.
- **Lỗi crash `SIGTRAP / BPT trap 5` tại `_UIApplicationEvaluateRuntimeIssueForNoSceneLifecycleAdoption`**:
  - Nguyên nhân: Thiếu cấu hình Scene Lifecycle trên iOS 27+.
  - Khắc phục: Đảm bảo đã cài `expo-build-properties`, cấu hình `"enableSceneSupport": true` trong `app.json`, sau đó chạy `npx expo prebuild --clean` và build lại.
- **Lỗi Podfile / CocoaPods**:
  - Khắc phục: Chạy `cd ios && pod install --repo-update && cd ..`.
