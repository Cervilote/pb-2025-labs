/* arrays.c — Массивы.
   Собирать: gcc -fsanitize=address -g arrays.c -o arrays
   Запустить: ./arrays   */

#include <stdio.h>
#include <stdlib.h>

void zero_int_array(int* array, int n) {
    for (int i = 0; i < n; i++) {
        array[i] = 0;
    }
}

void print_int_array(int* array, int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", array[i]);
    }
}

int main() {
    printf("==============================\nМассивы С:\n==============================\n");

    printf("\n1. Статический\n\n");

    int a[] = {1, 2, 3, 4, 5, 6, 7, 8};

    printf("Массив a: размер массива: %lu, размер элемента: %lu\n", sizeof(a) / sizeof(a[0]), sizeof(a[0]));

    printf("a = [ ");
    print_int_array(a, sizeof(a) / sizeof(a[0]));
    printf("]");

    printf("\n");
    printf("\n------------------------------\n");
    printf("\n2. Динамический\n\n");

    int b_size = 10;
    int* b = (int*)malloc(b_size * sizeof(int));
    // zero_int_array(b, b_size);

    printf("Массив b: размер массива: %lu, размер элемента: %lu\n", sizeof(b), sizeof(b[0]));

    printf("b = [ ");
    print_int_array(b, b_size);
    printf("]");

    //free(b);

    // printf("\n\nafter free\nb = [ ");
    // print_int_array(b, b_size);
    // printf("]");

    printf("\n");
    printf("\n------------------------------\n");
}
