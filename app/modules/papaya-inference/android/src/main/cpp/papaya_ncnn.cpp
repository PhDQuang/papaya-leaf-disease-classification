#include <jni.h>
#include <android/asset_manager_jni.h>
#include <algorithm>
#include <cmath>
#include <mutex>
#include <vector>
#include "net.h"

namespace {
std::mutex net_mutex;
ncnn::Net net;
bool loaded = false;

jfloatArray make_array(JNIEnv* env, const std::vector<float>& values) {
    jfloatArray result = env->NewFloatArray(static_cast<jsize>(values.size()));
    if (result && !values.empty()) {
        env->SetFloatArrayRegion(result, 0, static_cast<jsize>(values.size()), values.data());
    }
    return result;
}

void fail(JNIEnv* env, const char* message) {
    jclass exception = env->FindClass("java/lang/IllegalStateException");
    if (exception) env->ThrowNew(exception, message);
}
}

extern "C" JNIEXPORT void JNICALL
Java_expo_modules_papayainference_PapayaInferenceModule_nativeLoadYolo(
    JNIEnv* env, jobject, jobject java_assets) {
    std::lock_guard<std::mutex> lock(net_mutex);
    if (loaded) return;
    AAssetManager* assets = AAssetManager_fromJava(env, java_assets);
    if (!assets) { fail(env, "Cannot access Android model assets"); return; }
    net.opt.use_vulkan_compute = false;
    net.opt.num_threads = 4;
    if (net.load_param(assets, "yolo11m_papaya.param") != 0 ||
        net.load_model(assets, "yolo11m_papaya.bin") != 0) {
        net.clear();
        fail(env, "Could not load YOLO NCNN model");
        return;
    }
    loaded = true;
}

extern "C" JNIEXPORT jfloatArray JNICALL
Java_expo_modules_papayainference_PapayaInferenceModule_nativeRunYolo(
    JNIEnv* env, jobject, jobject bitmap, jfloat minimum_confidence) {
    std::lock_guard<std::mutex> lock(net_mutex);
    if (!loaded) { fail(env, "YOLO model is not loaded"); return nullptr; }
    ncnn::Mat input = ncnn::Mat::from_android_bitmap(env, bitmap, ncnn::Mat::PIXEL_RGB);
    if (input.empty() || input.w != 832 || input.h != 832) {
        fail(env, "YOLO input must be an 832x832 ARGB bitmap");
        return nullptr;
    }
    const float norm[3] = {1.f / 255.f, 1.f / 255.f, 1.f / 255.f};
    input.substract_mean_normalize(nullptr, norm);
    ncnn::Extractor extractor = net.create_extractor();
    if (extractor.input("in0", input) != 0) {
        fail(env, "YOLO input layer in0 failed");
        return nullptr;
    }
    ncnn::Mat output;
    if (extractor.extract("out0", output) != 0 || output.empty()) {
        fail(env, "YOLO output layer out0 failed");
        return nullptr;
    }
    // Ultralytics NCNN raw output is [8, 14196]: xywh + four class scores.
    const int values_per_anchor = 8;
    int anchors = 0;
    bool channels_first = false;
    if (output.dims == 2 && output.h == values_per_anchor) {
        anchors = output.w;
        channels_first = true;
    } else if (output.dims == 2 && output.w == values_per_anchor) {
        anchors = output.h;
    } else if (output.dims == 3 && output.c == values_per_anchor && output.h == 1) {
        anchors = output.w;
        channels_first = true;
    } else if (output.dims == 3 && output.c == 1 && output.h == values_per_anchor) {
        anchors = output.w;
        channels_first = true;
    } else {
        fail(env, "Unexpected YOLO output shape; expected 8 x 14196");
        return nullptr;
    }
    auto at = [&](int field, int anchor) -> float {
        if (output.dims == 3 && output.c == values_per_anchor) return output.channel(field).row(0)[anchor];
        if (output.dims == 3) return output.channel(0).row(field)[anchor];
        return channels_first ? output.row(field)[anchor] : output.row(anchor)[field];
    };
    std::vector<float> detections;
    detections.reserve(512);
    for (int i = 0; i < anchors; ++i) {
        int best_class = 0;
        float score = at(4, i);
        for (int c = 1; c < 4; ++c) {
            float candidate = at(4 + c, i);
            if (candidate > score) { score = candidate; best_class = c; }
        }
        if (!std::isfinite(score) || score < minimum_confidence) continue;
        float x = at(0, i), y = at(1, i), w = at(2, i), h = at(3, i);
        if (!std::isfinite(x) || !std::isfinite(y) || !std::isfinite(w) || !std::isfinite(h) || w <= 0 || h <= 0) continue;
        detections.insert(detections.end(), {x, y, w, h, static_cast<float>(best_class), score});
    }
    return make_array(env, detections);
}
