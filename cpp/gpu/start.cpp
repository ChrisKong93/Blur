#include "calc_cpu.cuh"
#include "calc_gpu.cuh"
#include "Test.cuh"
#include "blur_gpu.cuh"
#include <thread>
#include "start.h"
#include <windows.h>
using namespace std;


int main() {
	//gpuTest();
	//cpuTest();
	//gpuTest();
	//cpuTest();
	//info();
	//int s = blurTest(0);
	//thread t(r);
	thread t1(blurTest, 0);
	//thread t2(blurTest, 1);
	t1.join();
	//t2.join();
	//Sleep(10 * 1000);
	//while (true)
	//{
	//	printf("%d", 1);
	//}
	return 0;
}
