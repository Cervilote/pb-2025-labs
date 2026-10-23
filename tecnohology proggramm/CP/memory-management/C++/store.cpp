// store.cpp — то же хранилище на C++.
// Собирать: g++ -std=c++17 -fsanitize=address -g store.cpp -o store_cpp

#include <cstdio>
#include <memory>
#include <vector>

struct Point { double x, y; };

// ---- вариант 1: new/delete, те же дефекты, что в C -------------------------
struct StoreRaw {
    Point *items;
    int count, capacity;
    StoreRaw(int cap) : items(new Point[cap]), count(0), capacity(cap) {}
    ~StoreRaw() { delete[] items; }
};

// ---- вариант 2: unique_ptr, владение выражено в типе -----------------------
struct StoreUnique {
    std::unique_ptr<Point[]> items;
    int count, capacity;
    StoreUnique(int cap) : items(new Point[cap]), count(0), capacity(cap) {}
    // деструктор не нужен: освобождение при выходе из области видимости
};

// ---- вариант 3: shared_ptr и циклическая ссылка ----------------------------
struct Node {
    int value;
    std::shared_ptr<Node> next;
    ~Node() { printf("уничтожен узел %d\n", value); }
};

void demo_cycle() {
    auto a = std::make_shared<Node>();
    auto b = std::make_shared<Node>();
    a->value = 1;
    b->value = 2;
    a->next = b;
    b->next = a;          // цикл: счётчики никогда не обнулятся
    printf("выходим из demo_cycle\n");
    // сообщений об уничтожении не будет — память не освобождена
}

int main() {
    { StoreUnique s(2); printf("unique_ptr: освобождение автоматическое\n"); }
    demo_cycle();
    printf("demo_cycle завершилась\n");
    return 0;
}
