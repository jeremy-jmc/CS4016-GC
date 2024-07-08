
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <curand_kernel.h>

struct Matrix {
  int rows;
  int cols;
  float *M;
};

__global__ void populateMatrixKernel(float *M, int rows, int cols, unsigned long seed) {
  int idx = blockIdx.x * blockDim.x + threadIdx.x;
  int totalSize = rows * cols;
  if (idx < totalSize) {
    curandState state;
    curand_init(seed, idx, 0, &state);
    M[idx] = curand_uniform(&state);
  }
}

void populateMatrix(Matrix &M1) {
  int totalSize = M1.rows * M1.cols;
  float *d_M;
  cudaMalloc(&d_M, totalSize * sizeof(float));
  int threadsPerBlock = 256;
  int blocksPerGrid = (totalSize + threadsPerBlock - 1) / threadsPerBlock;

  populateMatrixKernel<<<blocksPerGrid, threadsPerBlock>>>(d_M, M1.rows, M1.cols, time(0));

  cudaMemcpy(M1.M, d_M, totalSize * sizeof(float), cudaMemcpyDeviceToHost);
  cudaFree(d_M);
}

__global__ void multiplyMatricesKernel(float *M1, int rows1, int cols1, float *M2, int rows2, int cols2, float *M3) {
  int row = blockIdx.y * blockDim.y + threadIdx.y;
  int col = blockIdx.x * blockDim.x + threadIdx.x;

  if (row < rows1 && col < cols2) {
    float sum = 0;
    for (int k = 0; k < cols1; ++k) {
      sum += M1[row * cols1 + k] * M2[k * cols2 + col];
    }
    M3[row * cols2 + col] = sum;
  }
}

void multiplyMatrices(Matrix &M1, Matrix &M2, Matrix &M3) {
  M3.rows = M1.rows;
  M3.cols = M2.cols;
  int sizeM1 = M1.rows * M1.cols * sizeof(float);
  int sizeM2 = M2.rows * M2.cols * sizeof(float);
  int sizeM3 = M3.rows * M3.cols * sizeof(float);

  float *d_M1, *d_M2, *d_M3;
  cudaMalloc(&d_M1, sizeM1);
  cudaMalloc(&d_M2, sizeM2);
  cudaMalloc(&d_M3, sizeM3);

  cudaMemcpy(d_M1, M1.M, sizeM1, cudaMemcpyHostToDevice);
  cudaMemcpy(d_M2, M2.M, sizeM2, cudaMemcpyHostToDevice);

  dim3 threadsPerBlock(16, 16);
  dim3 blocksPerGrid((M3.cols + threadsPerBlock.x - 1) / threadsPerBlock.x,
                     (M3.rows + threadsPerBlock.y - 1) / threadsPerBlock.y);

  multiplyMatricesKernel<<<blocksPerGrid, threadsPerBlock>>>(d_M1, M1.rows, M1.cols, d_M2, M2.rows, M2.cols, d_M3);

  cudaMemcpy(M3.M, d_M3, sizeM3, cudaMemcpyDeviceToHost);

  cudaFree(d_M1);
  cudaFree(d_M2);
  cudaFree(d_M3);
}

void printMatrix(Matrix M1) {
  for (int i = 0; i < M1.rows; ++i) {
    for (int j = 0; j < M1.cols; ++j) {
      std::cout << M1.M[i * M1.cols + j] << " ";
    }
    std::cout << std::endl;
  }
}

int main() {
  srand(static_cast<unsigned>(time(0)));

  int widthA, heightA, widthB, heightB;

  std::cout << "Enter the dimensions of matrix A (width height): ";
  std::cin >> widthA >> heightA;

  std::cout << "Enter the dimensions of matrix B (width height): ";
  std::cin >> widthB >> heightB;

  if (widthA != heightB) {
    std::cerr << "Error: Incompatible dimensions for matrix multiplication."
              << std::endl;
    return -1;
  }

  Matrix M1 = {heightA, widthA, new float[heightA * widthA]};
  Matrix M2 = {heightB, widthB, new float[heightB * widthB]};
  Matrix M3 = {heightA, widthB, new float[heightA * widthB]};

  populateMatrix(M1);
  populateMatrix(M2);

  std::cout << "Matrix A:" << std::endl;
  //printMatrix(M1);

  std::cout << "Matrix B:" << std::endl;
  //printMatrix(M2);

  multiplyMatrices(M1, M2, M3);
  std::cout << "Resulting Matrix C computed" << std::endl;
  //printMatrix(M3);

  delete[] M1.M;
  delete[] M2.M;
  delete[] M3.M;

  return 0;
}

// nvcc -o w14_matmul w14_matmul.cu && ./w14_matmul