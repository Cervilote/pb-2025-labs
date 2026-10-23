/* hello.c — Простейший проект.
   Собирать: gcc -g hello-pointers.c -o hello
   Запустить: ./hello   */

#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    char* parr = (char*)arr;

    printf("[ ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]);
    }
    printf("]\n");

    printf("[ ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", *(parr + i));
    }
    printf("]\n");

    short a = 7;
    int b = 9;
    float x = 3.1415926;

    printf("a = %d, b = %d, x = %f\n", a, b, x);
    printf("&a = %d, &b = %d, &x = %d\n", &a, &b, &x);

    short* pa = &a;
    int* pb = &b;
    float* px = &x;

    printf("pa = %d, pb = %d, px = %d\n", pa, pb, px);
    printf("a = %d, b = %d, x = %f\n", *pa, *pb, *px);

    short** ppa = &pa;
    int** ppb = &pb;
    float** ppx = &px;

    printf("ppa = %d, ppb = %d, ppx = %d\n", ppa, ppb, ppx);
    printf("*ppa = %d, *ppb = %d, *ppx = %d\n", *ppa, *ppb, *ppx);
    printf("**ppa = %d, **ppb = %d, **ppx = %f\n", **ppa, *ppb, *ppx);

    printf("a = %llu, b = %llu, x = %llu\n", sizeof(a), sizeof(b), sizeof(x));
    printf("a = %llu, b = %llu, x = %llu\n", sizeof(pa), sizeof(pb), sizeof(px));
}
