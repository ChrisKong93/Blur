# -*- coding: utf-8 -*-
import os
import time

import numpy as np
import matplotlib.pyplot as plt
import pycuda.autoinit as init
import pycuda.driver as drv
from PIL import Image
from pycuda.compiler import SourceModule

init

# 相当于直接生成一个C语言的kernel，注意输入的数据类型是unsigned char
mod = SourceModule('''
__global__ void operatelarge(int *g, unsigned char *img1, unsigned char *img2) {
    const int i =
            (blockIdx.x + blockIdx.y * gridDim.x) * blockDim.x * blockDim.y + threadIdx.y * blockDim.x + threadIdx.x;
    int h = g[0]; //图片高度
    int w = g[1]; //图片宽度
    int k = g[2]; //模糊内核
    int e = (k - 1) / 2;
    long j = w * i;
    if (i < h) {
        // 在一行里循环
        for (int z = 0; z < w; z++) {
            int a = (z + j) / w; //行数
            int b = (z + j) % w; //列数
            int s1 = 0, s2 = 0, s3 = 0;
            if ((e <= a && a < h - e) && (e <= b && b < w - e)) {
                int c = a - e;
                int d = b - e;
                for (int x = 0; x < k; x++) {
                    for (int y = 0; y < k; y++) {
                        s1 += (int) img1[3 * ((c + x) * w + (d + y)) + 0];
                        s2 += (int) img1[3 * ((c + x) * w + (d + y)) + 1];
                        s3 += (int) img1[3 * ((c + x) * w + (d + y)) + 2];
                    }
                }
                img2[3 * (z + j) + 0] = (unsigned char) (s1 / (k * k));
                img2[3 * (z + j) + 1] = (unsigned char) (s2 / (k * k));
                img2[3 * (z + j) + 2] = (unsigned char) (s3 / (k * k));
            } else {
                img2[3 * (z + j) + 0] = img1[3 * (z + j) + 0];
                img2[3 * (z + j) + 1] = img1[3 * (z + j) + 1];
                img2[3 * (z + j) + 2] = img1[3 * (z + j) + 2];
            }
        }
    }
}
''')


def run(path):
    # im = Image.open(path)
    # im.show()
    img1 = np.array(Image.open(path).convert('RGB'))  # 打开图像并转化为数字矩阵
    # print(img1)
    img2 = np.ones_like(img1) * 255
    # 通过cuda来调用gpu模块
    operatelarge = mod.get_function('operatelarge')
    print(img1.shape)
    h, w, c = img1.shape
    k = 21  # 卷积核kernel
    info = [h, w, k]
    info = np.int32(info)
    print(info)
    start = time.time()
    # 根据自己的GPU性能选择合适的block、grid，如果超出会报错
    operatelarge(drv.In(info), drv.In(img1), drv.Out(img2), block=(50, 1, 1), grid=(128, 1))
    stop = time.time()
    print(stop - start)
    # return stop - start
    # plt.figure("pic")
    # plt.imshow(img2)
    # plt.axis('off')
    # plt.show()
    return stop - start


if __name__ == '__main__':
    # run(path='C:/Users/Lenovo/Desktop/image/test.jpg')
    dir = os.getcwd()
    print(dir)
    path = dir + './../image/test.jfif'
    print(path)
    s = 0.0
    for i in range(10):
        s += run(path=path)
    print(s / 10)
