cmake_minimum_required(VERSION 2.8)
project(main)

set(QMAKE_CXXFLAGS "-std=c++11")

find_package( OpenCV REQUIRED)

#set(CMAKE_BUILD_TYPE Debug)
#AUX_SOURCE_DIRECTORY(./src DIR_SRCS)
add_executable( main blur.cpp)
target_link_libraries( main ${OpenCV_LIBS} )