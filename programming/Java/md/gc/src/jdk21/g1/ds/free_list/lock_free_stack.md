# 无锁栈

LockFreeStack 是一个无锁的 LIFO（后进先出）栈实现，其核心设计目标是通过"侵入式链表"和"原子操作(CAS)"实现多线程环境下的高效并发操作。

侵入式链表：元素自身携带链表指针，而非由栈分配节点。优势：无内存分配开销，元素可同时属于多个栈（通过不同的链表指针成员）。要求：元素类需提供 next_ptr 函数，用来返回链表的下一个节点。

```cpp
// T：栈元素类型
// next_ptr：函数指针，返回元素内链表指针的地址
template<typename T, T *volatile *(*next_ptr)(T &)>
class LockFreeStack {
    // 栈顶指针
    T *volatile _top;

    // push和prepend函数都会调用此函数, 原子地将链表压入栈顶
    // 执行流程:
    // 1. 将新链表的尾部 last 的 next 指向当前栈顶 cur
    // 2. 使用 CAS 将 _top 从 cur 更新为 first（新链表头部）
    // 3. 若 CAS 失败（其他线程修改了 _top），重试直到成功
    void prepend_impl(T *first, T *last) {
        T *cur = top();
        T *old;
        do {
            old = cur;
            set_next(*last, cur);
            cur = Atomic::cmpxchg(&_top, cur, first);
        } while (old != cur);
    }

    // 禁止拷贝该类的对象
    NONCOPYABLE(LockFreeStack);

public:
    LockFreeStack() : _top(nullptr) {}

    ~LockFreeStack() { assert(empty(), "stack not empty"); }

    // 出栈
    // 执行流程:
    // 1. 读取当前栈顶 result
    // 2. 计算新栈顶 new_top（即 result->next）
    // 3. 使用 CAS 将 _top 从 result 更新为 new_top
    // 4. 若成功，返回弹出的元素；否则重试
    T *pop() {
        T *result = top();
        T *old;
        do {
            old = result;
            T *new_top = nullptr;
            if (result != nullptr) {
                new_top = next(*result);
            }
            result = Atomic::cmpxchg(&_top, result, new_top);
        } while (result != old);
        if (result != nullptr) {
            set_next(*result, nullptr);
        }
        return result;
    }

    // 清空栈
    // 原子地将 _top 置为 nullptr，返回原栈顶链表
    T *pop_all() {
        return Atomic::xchg(&_top, (T *) nullptr);
    }

    // 将单个元素压入栈顶
    void push(T &value) {
        assert(next(value) == nullptr, "precondition");
        prepend_impl(&value, &value);
    }

    // 将链表（first 到 last）批量压入栈顶
    void prepend(T &first, T &last) {
        assert(next(last) == nullptr, "precondition");
#ifdef ASSERT
        for (T *p = &first; p != &last; p = next(*p)) {
            assert(p != nullptr, "invalid prepend list");
        }
#endif
        prepend_impl(&first, &last);
    }

    void prepend(T &first) {
        T *last = &first;
        while (true) {
            T *step_to = next(*last);
            if (step_to == nullptr) break;
            last = step_to;
        }
        prepend_impl(&first, last);
    }

    bool empty() const { return top() == nullptr; }

    T *top() const { return Atomic::load(&_top); }

    // 遍历链表计数，但 不保证线程安全
    size_t length() const {
        size_t result = 0;
        for (const T *current = top(); current != nullptr; current = next(*current)) {
            ++result;
        }
        return result;
    }

    // 通过 next_ptr 函数操作元素的链表指针，使用原子操作保证线程安全
    static T *next(const T &value) {
        return Atomic::load(next_ptr(const_cast<T &>(value)));
    }

    // 通过 next_ptr 函数操作元素的链表指针，使用原子操作保证线程安全
    static void set_next(T &value, T *new_next) {
        Atomic::store(next_ptr(value), new_next);
    }
};
```
