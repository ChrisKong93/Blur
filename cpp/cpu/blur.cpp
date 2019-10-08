// ConsoleApplication1.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

int main() {
	cout << "Hello World!\n" << endl;
	// 读入一张图片（poyanghu缩小图）    
	Mat img = imread("C:\\Users\\Lenovo\\Desktop\\image\\timg.jfif");
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
				//cout << s << endl;
			}
			//cout << s.at<Vec3b>(0, 0) << endl;
			//return 0;
			//img_new.at<Vec3b>(i, j)[0] = img.at<Vec3b>(i, j)[0] / 2;
			//img_new.at<Vec3b>(i, j)[1] = img.at<Vec3b>(i, j)[1] / 2;
			//img_new.at<Vec3b>(i, j)[2] = img.at<Vec3b>(i, j)[2] / 2;
		}
	}
	endTime = clock();//计时结束
	cout << "CPU The run time is: " << (double)(endTime - startTime)/1000 /* CLOCKS_PER_SEC*/ << "s" << endl;
	// 创建一个名为 "图片"窗口    
	namedWindow("图片");
	// 在窗口中显示图片   
	imshow("图片", img_new);
	// 等待6000 ms后窗口自动关闭    
	waitKey(0);
	return 0;
}


// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门提示: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
