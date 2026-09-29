cmake_minimum_required(VERSION 3.22.1)
project(papaya_ncnn LANGUAGES CXX)

set(ncnn_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third_party/ncnn/${ANDROID_ABI}/lib/cmake/ncnn")
find_package(ncnn REQUIRED)

add_library(papaya_ncnn SHARED src/main/cpp/papaya_ncnn.cpp)
target_link_libraries(papaya_ncnn PRIVATE ncnn)
target_link_options(papaya_ncnn PRIVATE
  "-Wl,-z,max-page-size=16384"
  "-Wl,-z,common-page-size=16384"
)
