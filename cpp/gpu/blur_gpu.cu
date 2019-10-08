#include "blur_gpu.cuh"

__global__ void operatepic(int g, int *img1, int *img2, int *img3, int index) {
	int t = 32 * 30;
	int threadId_3D = threadIdx.x + threadIdx.y*blockDim.x + threadIdx.z*blockDim.x*blockDim.y;
	int blockId_3D = blockIdx.x + blockIdx.y*gridDim.x + blockIdx.z*gridDim.x*gridDim.y;
	int i = threadId_3D + (blockDim.x*blockDim.y*blockDim.z)*blockId_3D;

	if (g / t < 1) {
		img3[i] = (img1[i] + img2[i]) / 2;
	}
	else {
		for (int j = 0; j <= (g / t); j++) {
			if (index == 0) {
				img3[i + j * t] = (img1[i + j * t] + img2[i + j * t]) / 2;
			}
			else
			{
				img3[i + j * t] = (img1[i + j * t] + img2[i + j * t]) / 2 + 1;
			}
		}
	}
}


int main(int index = 0) {
	clock_t startTime, endTime;
	startTime = clock();
	int Row = 1920;
	int Col = 1080;
	int *A = (int *)malloc(sizeof(int) * Row * Col);
	int *B = (int *)malloc(sizeof(int) * Row * Col);
	int *C = (int *)malloc(sizeof(int) * Row * Col);
	//malloc device memory
	int *d_dataA, *d_dataB, *d_dataC;
	//cudaSetDevice(3);
	cudaError_t cudaStatus;
	cudaStatus = cudaSetDevice(index);
	if (cudaStatus != cudaSuccess) {
		fprintf(stderr, "cudaSetDevice failed!  Do you have a CUDA-capable GPU installed?\n");
	}
	else {
		printf("success\n");
	}
	cudaMalloc((void**)&d_dataA, sizeof(int) * Row * Col);
	cudaMalloc((void**)&d_dataB, sizeof(int) * Row * Col);
	cudaMalloc((void**)&d_dataC, sizeof(int) * Row * Col);
	//set value
	for (int i = 0; i < Row * Col; i++) {
		A[i] = 255;
		B[i] = 0;
	}
	int s = Row * Col;
	//cout << s << endl;
	cudaMemcpy(d_dataA, A, sizeof(int) * Row * Col, cudaMemcpyHostToDevice);
	cudaMemcpy(d_dataB, B, sizeof(int) * Row * Col, cudaMemcpyHostToDevice);
	dim3 threadPerBlock(32, 1, 1);
	dim3 blockNumber(30, 1, 1);
	//printf("Block(%d,%d)   Grid(%d,%d).\n", threadPerBlock.x, threadPerBlock.y, blockNumber.x, blockNumber.y);

	operatepic <<< blockNumber, threadPerBlock >>> (s, d_dataA, d_dataB, d_dataC, index);
    //拷贝计算数据-一级数据指针
	cudaMemcpy(C, d_dataC, sizeof(int) * Row * Col, cudaMemcpyDeviceToHost);
//	for (int j = 0; j < s; j++) {
//		printf("%d", C[j]);
//	}
    //释放内存
	free(A);
	free(B);
	free(C);
	cudaFree(d_dataA);
	cudaFree(d_dataB);
	cudaFree(d_dataC);

	endTime = clock();//计时结束

	cout << "GPU The run time is: " << (double)(endTime - startTime) /* CLOCKS_PER_SEC*/ << "ms" << endl;
	return 0;
}