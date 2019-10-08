cmake_minimum_required(VERSION 3.14)
project(gpu)

set(CMAKE_CXX_STANDARD 14)
find_package(CUDA REQUIRED)
#file(GLOB CU GPUinfo.cu)
#cuda_add_executable( main GPUinfo.cu)
#file(GLOB CU blur_gpu.cu)
#cuda_add_executable( main blur_gpu.cu)
file(GLOB CU calc_cpu.cu)
cuda_add_executable( main calc_cpu.cu)

include_directories(${CUDA_INCLUDE_DIRS})