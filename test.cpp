#include <iostream>

struct A {
    int a;
} aaa[3];

void test(A *a, A *b) {
    *a = aaa[2];
    *b = aaa[2];
}

int main() {
    aaa[0].a = 111;
    aaa[1].a = 999;
    aaa[2].a = 555;

    std::cout << aaa[0].a << " " << aaa[1].a << "\n";
    test(&aaa[0], &aaa[1]);
    std::cout << aaa[0].a << " " << aaa[1].a << "\n";
    return 0;
}