// ConsoleApplication1.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

int main() {
	cout << "Hello World!\n" << endl;
	// 读入一张图片
	Mat img = imread("../../../image/test.jfif");
	//Mat img = imread("C:\\Users\\Lenovo\\Desktop\\image\\test.jpg");
	clock_t startTime, endTime;
	
	int h = img.rows;
	int w = img.cols;
	int c = img.channels();
	int k = 21;
	//Mat img_new = Mat(h, w, CV_8UC3);
	Mat img_new = img;
	/*
	cout << "Im.dims  = " << img.dims << endl;
	cout << "Im.rows  = " << img.rows << endl;
	cout << "Im.cols  = " << img.cols << endl;
	cout << "Im.channels = " << img.channels() << endl;
	cout << (int)(img.at<Vec3b>(0,0)[0]) << endl;
	*/
	startTime = clock();//计时开始
	for (int i = 0; i < h; i++) {
		for (int j = 0; j < w; j++) {
			int o = (k - 1) / 2;
			int m = i - o;
			int n = j - o;
			Vec3i s;
			if ((o <= i && i < h - o) && (o <= j && j < w - o)) {
				//cout << j << "," << i << endl;
				for (int x = 0; x < k; x++) {
					for (int y = 0; y < k; y++) {
						s += img.at<Vec3b>(m + x, n + y);
					}
				}
				img_new.at<Vec3b>(i, j) = s / (k*k);
			}
		}
	}
	endTime = clock();//计时结束
	cout << "CPU The run time is: " << (double)(endTime - startTime)/1000 /* CLOCKS_PER_SEC*/ << "s" << endl;
	// 创建一个名为 "图片"窗口    
	namedWindow("图片");
	// 在窗口中显示图片   
	imshow("图片", img_new);
	// 等待窗口不关闭
	waitKey(0);
	return 0;
}
