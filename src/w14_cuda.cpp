#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void init_array(int *array, int n)
{
    for (int i = 0; i < n; i++)
        array[i] = rand() % 100; // Números aleatorios entre 0 y 99
}

int main(int argc, char *argv[])
{
    int n = 1e9;
    int *arr_1 = nullptr, *arr_2 = nullptr, *sum_array = nullptr;
    arr_1 = (int *)malloc(n * sizeof(int));
    arr_2 = (int *)malloc(n * sizeof(int));
    sum_array = (int *)malloc(n * sizeof(int));

    if (arr_1 == NULL || arr_2 == NULL || sum_array == NULL)
    {
        printf("Error al asignar memoria.\n");
        return 1;
    }


    init_array(arr_1, n);
    init_array(arr_2, n);

    int start_time = clock();
    for (int i = 0; i < n; i++)
    {
        sum_array[i] = arr_1[i] + arr_2[i];
    }

    // printf("Array 1: ");
    // for (int i = 0; i < n; i++)
    // {
    //     printf("%d ", arr_1[i]);
    // }
    // printf("\n");

    // printf("Array 2: ");
    // for (int i = 0; i < n; i++)
    // {
    //     printf("%d ", arr_2[i]);
    // }
    // printf("\n");

    // printf("sum_array de los arrays: ");
    // for (int i = 0; i < n; i++)
    // {
    //     printf("%d ", sum_array[i]);
    // }
    // printf("\n");
    int end_time = clock();

    free(arr_1);
    free(arr_2);
    free(sum_array);
    printf("Time taken: %f\n", (end_time - start_time) / (double) CLOCKS_PER_SEC);
    return 0;
}


// gcc -o w14_cuda w14_cuda.cpp && ./w14_cuda