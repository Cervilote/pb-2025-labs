/* store.c — хранилище точек на ручном управлении памятью.
   Собирать: gcc -fsanitize=address -g store.c -o store && ./store   */

#include <stdio.h>
#include <stdlib.h>

typedef struct { double x, y; } Point;

typedef struct {
    Point *items;
    int count;
    int capacity;
} Store;

Store *store_create(int capacity) {
    Store *s = malloc(sizeof(Store));
    s->items = malloc(sizeof(Point) * capacity);
    s->count = 0;
    s->capacity = capacity;
    return s;
}

int store_add(Store *s, double x, double y) {
    if (s->count >= s->capacity) {
        return -1;              /* ДЕФЕКТ 1: ранний возврат, вызывающий не знает,
                                   что делать с уже занятой памятью             */
    }
    s->items[s->count].x = x;
    s->items[s->count].y = y;
    return s->count++;
}

void store_free(Store *s) {
    free(s->items);
    free(s);
}

int main(void) {
    Store *s = store_create(2);
    // store_add(s, 1.0, 2.0);
    // store_add(s, 3.0, 4.0);

    // if (store_add(s, 5.0, 6.0) < 0) {
    //     printf("хранилище заполнено\n");
    //     return 1;               /* ДЕФЕКТ 1: выход без store_free — утечка */
    // }

    // Point *p = &s->items[0];
    // store_free(s);
    // printf("x = %f\n", p->x);   /* ДЕФЕКТ 2: обращение по освобождённому указателю.
    //                                Без санитайзера часто печатает верное значение */

    // store_free(s);        /* ДЕФЕКТ 3: раскомментировать — двойное освобождение */
    return 0;
}
