import os
import time

import numpy as np
from PIL import Image
from numba import jit


# 做某一个像素点的均值模糊
@jit
def average(i, j, k):
    m = int(i - (k - 1) / 2)
    n = int(j - (k - 1) / 2)
    s = np.zeros(3)
    for x in range(k):
        for y in range(k):
            s += img[m + x][n + y]
    return s // (k * k)


def blur():
    k = 21
    n = int((k - 1) / 2)
    print(h, w, k)
    # 遍历出没有个像素点的坐标
    for i in range(h):
        for j in range(w):
            if n <= i < h - n and n <= j < w - n:
                img_new[i][j] = average(i, j, k)


dir = os.getcwd()
# print(dir)
path = dir + './../image/test.jfif'
print(path)
img = np.array(Image.open(path))  # 打开图像并转化为数字矩阵
img_new = img
# im = Image.open(path)
# im.show()
h, w, c = img.shape

if __name__ == '__main__':
    s = 0.0
    for i in range(10):
        start = time.time()
        blur()
        stop = time.time()
        s += stop - start
        print(stop - start)
    print(s / 10)
    # plt.figure("pic")
    # plt.imshow(img_new)
    # plt.axis('off')
    # plt.show()
