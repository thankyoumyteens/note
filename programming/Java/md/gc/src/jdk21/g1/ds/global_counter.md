# GlobalCounter

GlobalCounter(全局计数器)用来实现 RCU 机制

RCU(读-拷贝-更新, Read-Copy Update)是一种用于在多线程环境下高效地实现共享数据读写操作的同步机制。它主要用于解决在并发访问场景下，如何在保证数据一致性的同时，尽可能地提高读操作的性能。

在 RCU 机制下，读操作几乎没有锁的开销。当一个线程进行读操作时，它可以直接访问共享数据，不需要获取任何锁。因为 RCU 机制保证了在读取数据的过程中，数据不会被其他线程修改（或者说修改操作对读操作是透明的）。

写操作相对复杂一些。当一个线程需要修改共享数据时，它首先会拷贝一份要修改的数据副本。然后，在这个副本上进行修改操作。以链表为例，如果要插入一个新节点，先把整个链表（或者相关部分）拷贝一份，然后在副本链表中插入新节点。在修改完成后，需要使用一个同步机制来更新原始数据，使得后续的读操作能够看到新的数据。这个更新过程通常会等待所有正在进行的旧数据的读操作完成，然后再将修改后的副本替换原始数据。这样可以确保在更新过程中，没有读操作会访问到一个不一致的中间状态。

## 优缺点

由于读操作不需要获取锁，因此可以实现很高的并发读性能。但每次写操作都要拷贝数据并等待合适的时机更新，这可能会消耗大量的时间和内存资源。

## GlobalCounter 实现

全局计数器: 在基于计数器的 RCU 实现中，首先会有一个全局计数器（Global Counter）。这个计数器用于记录整个系统的更新次数或者版本号。它通常是一个原子类型（如原子整数），以确保在多线程环境下能够正确地进行计数操作，不会出现数据竞争导致计数错误。

线程局部计数器: 每个线程也会有一个与之关联的局部计数器（Thread-Local Counter）。这个计数器用于跟踪每个线程所看到的数据版本或者更新状态。当线程首次访问共享数据时，其局部计数器会被初始化，通常初始化为和全局计数器相同的值。这样，线程局部计数器和全局计数器就建立了关联，用于后续判断线程读取的数据版本是否是最新的。

旧读操作: 是指在写操作开始修改数据之前就已经开始的读操作。这些读操作正在读取的数据版本是旧的数据版本。

新读操作: 是指在写操作已经更新数据或者在写操作更新数据过程中开始的读操作。这些读操作读取的数据是更新后的数据版本或者是不受当前写操作干扰的数据版本。

### 读操作实现

当一个线程进行读操作时，它首先会读取自己的局部计数器和全局计数器的值。这个读取过程是原子操作，以确保获取到的计数器值是准确的。

线程在读取共享数据的过程中，不需要获取锁或者其他复杂的同步机制。因为只要全局计数器的值没有发生变化（即没有写操作进行数据更新），线程读取的数据就是一致的。如果在读取过程中全局计数器的值发生了变化，由于之前已经读取了计数器的值，线程可以通过比较局部计数器和全局计数器来判断自己读取的数据是否仍然有效。一般来说，如果局部计数器的值等于全局计数器的值，那么线程读取的数据就是最新的，是有效的。如果局部计数器的值小于全局计数器的值，说明在读取过程中有写操作进行了数据更新，此时可能需要根据具体的应用场景来决定如何处理(一种简单的处理方式是重新读取数据，以获取最新的数据版本)。

### 写操作实现

1. 数据备份: 当一个线程需要进行写操作时，它首先要进行数据备份。因为在 RCU 机制下，不能直接修改正在被读取的数据，所以需要拷贝一份要修改的数据副本
2. 数据修改: 在备份的数据副本上进行修改操作。这一步相对比较自由，因为不会影响正在进行的读操作
3. 更新全局计数器: 在完成数据修改后，写操作线程需要更新全局计数器。这是一个原子操作，通常会使用原子加法来增加全局计数器的值，以标记数据已经进行了一次更新
4. 等待旧读操作完成: 写操作线程需要等待所有旧读操作完成。这是通过检查各个线程的局部计数器来实现的。对于每个线程，如果其局部计数器的值小于更新后的全局计数器的值，说明这个线程是一个旧读操作线程，正在读取旧版本的数据。写操作线程需要等待这些线程完成读操作，确保它们不会再访问即将被替换的旧数据。对于新的读操作线程，其计数器值相对全局计数器版本较大。这意味着新的读操作线程是在新的数据版本或者新的读写阶段开始的，由于是在新的数据版本基础上进行读取，不会受到当前写操作更新旧数据的影响，所以不需要等待。写操作只需要关注那些已经在旧数据版本上进行读取的线程，并等待它们完成读取后再进行数据更新，以确保数据的一致性
5. 数据更新: 当所有旧读操作线程完成读取后，写操作线程可以将修改后的数据副本替换原来的共享数据，完成数据的更新操作。这样，后续的读操作线程就能够读取到新的数据版本了

## GlobalCounter 类

```cpp
// --- src/hotspot/share/utilities/globalCounter.hpp --- //

class GlobalCounter : public AllStatic {
private:
    // 由于不清楚最终在BSS段中会和什么相邻
    // 所以要通过填充周边内存确保计数器位于单独的缓存行上
    struct PaddedCounter {
        DEFINE_PAD_MINUS_SIZE(0, DEFAULT_CACHE_LINE_SIZE, 0);
        volatile uintx _counter;
        DEFINE_PAD_MINUS_SIZE(1, DEFAULT_CACHE_LINE_SIZE, sizeof(volatile uintx));
    };

    // 全局计数器
    static PaddedCounter _global_counter;

    // 最低位表示激活状态
    // 计数器的值大于等于1为激活
    static const uintx COUNTER_ACTIVE = 1;
    // 计数器的值每次加2
    static const uintx COUNTER_INCREMENT = 2;

    // 用来实现: 等待所有线程的旧读操作完成
    class CounterThreadCheck;

public:

    // The type of the critical section context passed from
    // critical_section_begin() to critical_section_end().
    enum class CSContext : uintx {
    };

    // 必须在读取数据之前调用
    // critical_section_begin 的返回值用来传给 critical_section_end 函数
    static CSContext critical_section_begin(Thread *thread);

    // 必须在数据读取完成后调用
    // context 参数必须是 critical_section_begin 方法的返回值
    static void critical_section_end(Thread *thread, CSContext context);

    // 在调用之前, 需要使旧数据对新的读线程不可访问
    // 函数返回后, 旧数据就可以安全地清理了
    static void write_synchronize();

    // 用来简化 critical_section_begin 和 critical_section_end 的调用
    // 构造函数调用 critical_section_begin
    // 析构函数调用 critical_section_end
    class CriticalSection;
};
```

## 读操作

```cpp
// --- src/hotspot/share/utilities/globalCounter.inline.hpp --- //

inline GlobalCounter::CSContext
GlobalCounter::critical_section_begin(Thread *thread) {
    assert(thread == Thread::current(), "must be current thread");
    // 每个线程内部有一个 _rcu_counter 计数器
    uintx old_cnt = Atomic::load(thread->get_rcu_counter());
    // 如果当前 _rcu_counter 是激活状态(即大于等于1), 则 _rcu_counter 保持不变
    // 否则, 把 _rcu_counter 设为激活状态
    uintx new_cnt = old_cnt;
    // 判断是否激活(最低位是否等于1)
    if ((new_cnt & COUNTER_ACTIVE) == 0) {
        // 设为设为激活状态
        // 全局计数器的值和 COUNTER_ACTIVE 按位或, 保证值至少是1
        new_cnt = Atomic::load(&_global_counter._counter) | COUNTER_ACTIVE;
    }
    // 把新值存回线程
    Atomic::release_store_fence(thread->get_rcu_counter(), new_cnt);
    // 返回旧值, 调用 critical_section_end 函数后会恢复旧值
    return static_cast<CSContext>(old_cnt);
}

inline void
GlobalCounter::critical_section_end(Thread *thread, CSContext context) {
    assert(thread == Thread::current(), "must be current thread");
    assert((*thread->get_rcu_counter() & COUNTER_ACTIVE) == COUNTER_ACTIVE, "must be in critical section");
    // 恢复旧值, 把线程内部的 _rcu_counter 计数器恢复到调用 critical_section_begin 之前的值
    Atomic::release_store(thread->get_rcu_counter(),
                          static_cast<uintx>(context));
}

// 用法:
// {
//     GlobalCounter::CriticalSection cs(Thread::current());
//     do something
// }
//
class GlobalCounter::CriticalSection {
private:
    Thread *_thread;
    CSContext _context;
public:
    // 创建对象时, 构造函数调用 critical_section_begin
    inline CriticalSection(Thread *thread) :
            _thread(thread),
            _context(GlobalCounter::critical_section_begin(_thread)) {}

    // 离开作用域时, 析构函数调用 critical_section_end
    inline  ~CriticalSection() {
        GlobalCounter::critical_section_end(_thread, _context);
    }
};
```

## 写操作

1. 调用 write_synchronize 之前, 需要先用修改后的数据副本替换原来的共享数据(修改指针), 并保留旧数据
2. write_synchronize 会将全局计数器+2, 此后的读线程内部计数器全是大于等于全局计数器的, 读取的也是新数据
3. write_synchronize 等待所有旧读线程读取完毕
4. write_synchronize 返回之后, 已经没有旧读线程了, 就可以释放旧数据的内存了

```cpp
// --- src/hotspot/share/utilities/globalCounter.cpp --- //

void GlobalCounter::write_synchronize() {
    assert((*Thread::current()->get_rcu_counter() & COUNTER_ACTIVE) == 0x0, "must be outside a critcal section");
    // Atomic::add需要提供StoreLoad内存屏障的功能, 保证_counter的修改对所有线程立即可见
    uintx gbl_cnt = Atomic::add(&_global_counter._counter, COUNTER_INCREMENT);

    // 等待所有线程的旧读操作完成
    CounterThreadCheck ctc(gbl_cnt);
    for (JavaThreadIteratorWithHandle jtiwh; JavaThread *thread = jtiwh.next();) {
        ctc.do_thread(thread);
    }
    for (NonJavaThread::Iterator njti; !njti.end(); njti.step()) {
        ctc.do_thread(njti.current());
    }
}

class GlobalCounter::CounterThreadCheck : public ThreadClosure {
private:
    uintx _gbl_cnt;
public:
    CounterThreadCheck(uintx gbl_cnt) : _gbl_cnt(gbl_cnt) {}

    void do_thread(Thread *thread) {
        SpinYield yield;
        // 等待thread线程的旧读操作完成
        while (true) {
            uintx cnt = Atomic::load_acquire(thread->get_rcu_counter());
            // (cnt - _gbl_cnt) > (max_uintx / 2) 用于判断是不是新读操作, 如果是新读操作则跳出循环
            if (((cnt & COUNTER_ACTIVE) != 0) && (cnt - _gbl_cnt) > (max_uintx / 2)) {
                // 自旋等待
                yield.wait();
            } else {
                break;
            }
        }
    }
};
```

## SpinYield

```cpp
// --- src/hotspot/share/utilities/spinYield.hpp --- //

class SpinYield : public StackObj {
    Tickspan _sleep_time;
    uint _spins;
    uint _yields;
    uint _spin_limit;
    uint _yield_limit;
    uint _sleep_ns;

    void yield_or_sleep();

public:
    // 执行下一轮延迟操作
    void wait() {
        // 简单策略：_spins小于按照配置的次数(_spin_limit)时立即返回（自旋），达到配置的次数后切换为让出处理器（yield）或休眠（sleep）
        // 未来可能会提供其他策略，例如（1）如果系统未饱和则始终进行自旋，或者（2）如果让出处理器操作无效则进行休眠
        if (_spins < _spin_limit) {
            ++_spins;
            // int SpinPause() {
            //     return 0;
            // }
            SpinPause();
        } else {
            yield_or_sleep();
        }
    }
};

// --- src/hotspot/share/utilities/spinYield.cpp --- //

void SpinYield::yield_or_sleep() {
    if (_yields < _yield_limit) {
        ++_yields;
        // 让出处理器
        os::naked_yield();
    } else {
        // 进行休眠
        Ticks sleep_start = Ticks::now();
        os::naked_short_nanosleep(_sleep_ns);
        _sleep_time += Ticks::now() - sleep_start;
    }
}
```
