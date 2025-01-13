# 删除链表节点

不使用 `current->next = current->next->next` 的方法, 而使用另一种方法。

```cpp
#include <iostream>

class Node {
public:
    int value;
    Node *next;

    explicit Node(int value = 0, Node *next = nullptr) : value(value), next(next) {}
};

void print_list(Node *first) {
    for (Node *current = first; current != nullptr; current = current->next) {
        std::cout << current->value << " ";
    }
    std::cout << std::endl;
}

int main() {
    // 初始化数据
    Node *first = new Node(1, nullptr);
    first->next = new Node(2, nullptr);
    first->next->next = new Node(3, nullptr);

    print_list(first);

    // 删除first节点
    Node *rem_n = first;
    // rem_n_prev是指向first指针的指针
    // 所以*rem_n_prev是first指针的地址
    Node **rem_n_prev = &first;
    // 把first指针的地址替换成下一个节点的指针的地址
    // 等同于把原来的first删掉了
    *rem_n_prev = rem_n->next;

    print_list(first);

    return 0;
}
```
