#include<stdio.h>
#include<iostream>
#include<ctime>
#include<cstdlib>

__global__ void add(int *a, int *b, int *c)
{
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    c[index] = a[index] + b[index];
}

int main(){
    int size = 1e9; 
    
    int *a, *b, *c;
    int *d_a, *d_b, *d_c;
    int *h_a, *h_b, *h_c;
    int *h_sum;
    int *d_sum;
    int totalSize = size * sizeof(int);
    int threadsPerBlock = 256;
    int blocksPerGrid = (size + threadsPerBlock - 1) / threadsPerBlock;

    a = (int *)malloc(totalSize);
    b = (int *)malloc(totalSize);
    c = (int *)malloc(totalSize);
    h_sum = (int *)malloc(totalSize);

    cudaMalloc(&d_a, totalSize);
    cudaMalloc(&d_b, totalSize);
    cudaMalloc(&d_c, totalSize);
    cudaMalloc(&d_sum, totalSize);

    h_a = a;
    h_b = b;
    h_c = c;

    srand(time(0));
    for(int i = 0; i < size; i++){
        h_a[i] = rand() % 100;
        h_b[i] = rand() % 100;
    }

    cudaMemcpy(d_a, h_a, totalSize, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, totalSize, cudaMemcpyHostToDevice);

    int start_time = clock();
    add<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c);
    int end_time = clock();

    cudaMemcpy(h_c, d_c, totalSize, cudaMemcpyDeviceToHost);

    for(int i = 0; i < size; i++){
        h_sum[i] = h_a[i] + h_b[i];
    }

    cudaMemcpy(d_sum, h_sum, totalSize, cudaMemcpyHostToDevice);

    for(int i = 0; i < size; i++){
        if(h_c[i] != h_sum[i]){
            printf("Error at index %d\n", i);
            break;
        }
    }

    free(a);
    free(b);
    free(c);
    free(h_sum);
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    cudaFree(d_sum);

    printf("Time taken: %f\n", (end_time - start_time) / (double) CLOCKS_PER_SEC);
    return 0;
}

// nvcc -o w14_cuda w14_cuda.cu && ./w14_cuda