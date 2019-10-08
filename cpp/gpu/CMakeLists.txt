cmake_minimum_required(VERSION 3.14)
project(gpu)

set(CMAKE_CXX_STANDARD 14)
find_package(CUDA REQUIRED)
#file(GLOB CU GPUinfo.cu)
#cuda_add_executable( main GPUinfo.cu)
file(GLOB CU GPUinfo.cu)
cuda_add_executable( main GPUinfo.cu)

include_directories(${CUDA_INCLUDE_DIRS})