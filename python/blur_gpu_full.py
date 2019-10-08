# -*- coding: utf-8 -*-
import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pycuda.autoinit as init
import pycuda.driver as drv
from PIL import Image
from pycuda.compiler import SourceModule

# from six.moves import range

init
drv.init()
# print(" %d device(s) found." % drv.Device.count())

Count = 0
for ordinal in range(drv.Device.count()):
    dev = drv.Device(ordinal)
    # print(' Device #%d: %s' % (ordinal, dev.name()))
    # print(' Compute Capability: %d.%d' % dev.compute_capability())
    # print(' Total Memory: %s KB' % (dev.total_memory() // (1024)))
    atts = [(str(att), value) for att, value in list(dev.get_attributes().items())]
    atts.sort()
    for att, value in atts:
        # print(' %s : %s' % (att, value))
        if att == 'ASYNC_ENGINE_COUNT':
            Count = value

# 相当于直接生成一个C语言的kernel，注意输入的数据类型是unsigned char
mod = SourceModule('''
__global__ void operatepic(int *g, unsigned char *img1, unsigned char *img2) {
    //const int i =
            (blockIdx.x + blockIdx.y * gridDim.x) * blockDim.x * blockDim.y + threadIdx.y * blockDim.x + threadIdx.x;
    const int threadId_3D = threadIdx.x + threadIdx.y*blockDim.x + threadIdx.z*blockDim.x*blockDim.y;
    const int blockId_3D = blockIdx.x + blockIdx.y*gridDim.x + blockIdx.z*gridDim.x*gridDim.y;
    const int i = threadId_3D + (blockDim.x*blockDim.y*blockDim.z)*blockId_3D;
    //printf("%d\\n", i);
    int h = g[0]; //图片高度
    int w = g[1]; //图片宽度
    int k = g[2]; //模糊内核
    int e = (k - 1) / 2;
    long j = g[3] * g[4];
    int z = 0;
    if (h * w % j == 0) {
        z = h * w / j;
    } else if (h * w % j != 0) {
        z = (h * w / j) + 1;
    }
    
    for (int q = 0; q < z; q++) {
        int s1 = 0, s2 = 0, s3 = 0;
        int a = (i + q * j) / w; //行数
        int b = (i + q * j) % w; //列数
        if (i + q * j < h * w) {
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
                img2[3 * (i + q * j) + 0] = (s1 / (k * k));
                img2[3 * (i + q * j) + 1] = (s2 / (k * k));
                img2[3 * (i + q * j) + 2] = (s3 / (k * k));
            } else {
                img2[3 * (i + q * j) + 0] = img1[3 * (i + q * j) + 0];
                img2[3 * (i + q * j) + 1] = img1[3 * (i + q * j) + 1];
                img2[3 * (i + q * j) + 2] = img1[3 * (i + q * j) + 2];
            }
        }
    }
}
__global__ void test(){
    const int threadId_3D = threadIdx.x + threadIdx.y*blockDim.x + threadIdx.z*blockDim.x*blockDim.y;
    const int blockId_3D = blockIdx.x + blockIdx.y*gridDim.x + blockIdx.z*gridDim.x*gridDim.y;
    const int i = threadId_3D + (blockDim.x*blockDim.y*blockDim.z)*blockId_3D;
    printf("%d,",i);
}
''')


def run(path):
    # im = Image.open(path)
    # im.show()
    img1 = np.array(Image.open(path).convert('RGB'))  # 打开图像并转化为数字矩阵
    # print(type(img1))
    img2 = np.ones_like(img1) * 255
    # 通过cuda来调用gpu模块
    operatepic = mod.get_function('operatepic')
    test = mod.get_function('test')
    print(img1.shape)
    h, w, c = img1.shape
    k = 21  # 卷积核kernel
    b = Count * 10  # 块儿数
    t = 128  # 每个块儿线程数
    info = [h, w, k, b, t]
    info = np.int32(info)
    print(info)
    start = time.time()
    # 根据自己的GPU性能选择合适的block、grid，如果超出会报错
    for i in range(10):
        operatepic(drv.In(info), drv.In(img1), drv.Out(img2), block=(t, 1, 1), grid=(b, 1))
    stop = time.time()
    print((stop - start) / 10)
    # test(block=(t, 1, 1), grid=(1, 1))
    # plt.figure("pic")
    # plt.imshow(img2)
    # plt.axis('off')
    # plt.show()


if __name__ == '__main__':
    # run(path='./image/test.jfif')
    dir = os.getcwd()
    # print(dir)
    path = dir + './../image/test.jfif'
    # path = dir + '/image/test.jpg'
    print(path)
    # s = 0.0
    run(path=path)
