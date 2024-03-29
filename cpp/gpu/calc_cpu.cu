#include "calc_cpu.cuh"
#define ROWS 1024
#define COLS 1024
using namespace std;

void matrix_mul_cpu(float* M, float* N, float* P, int width)
{
	for (int i = 0; i < width; i++)
		for (int j = 0; j < width; j++)
		{
			float sum = 0.0;
			for (int k = 0; k < width; k++)
			{
				float a = M[i*width + k];
				float b = N[k*width + j];
				sum += a * b;
			}
			P[i*width + j] = sum;
		}
}


int main()
{
	clock_t startTime, endTime;
	startTime = clock();//计时开始

	
	float *A, *B, *C;
	int total_size = ROWS * COLS * sizeof(float);
	A = (float*)malloc(total_size);
	B = (float*)malloc(total_size);
	C = (float*)malloc(total_size);

	//CPU一维数组初始化
	for (int i = 0; i < ROWS*COLS; i++)
	{
		A[i] = 80.0;
		B[i] = 20.0;
	}

	matrix_mul_cpu(A, B, C, COLS);

	endTime = clock();//计时结束
	cout << "CPU The run time is: " << (double)(endTime - startTime) /* CLOCKS_PER_SEC*/ << "ms" << endl;
	return 0;
}