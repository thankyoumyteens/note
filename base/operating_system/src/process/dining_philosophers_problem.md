# 哲学家进餐问题

一张圆桌上坐着 5 名哲学家, 每两个哲学家之间的桌上摆一根筷子, 桌子的中间是一碗米饭。哲学家们只能进行思考或进餐, 哲学家在思考时, 并不影响他人。只有当哲学家饥饿时, 才试图拿起左、右两根筷子。如果筷子已在他人手上, 则需等待。饥饿的哲学家只有同时拿起两根筷子才可以开始进餐, 当进餐完毕后, 放下筷子继续思考。

如果每个哲学家吃饭前依次拿起左、右两支筷子, 当 5 个哲学家并发地拿起了自己左手边的筷子, 就会导致每位哲学家循环等待右边
的人放下筷子, 发生死锁。

## 解决方案一

当两边的筷子都可用时才拿: 对拿筷子这一步骤进行加锁, 保证哲学家能够同时拿起一双筷子, 而不会拿了一边后另一边被人抢走, 保证不会因为每个哲学家都只拿了一只筷子而导致死锁。

```cpp
// 5个筷子
semaphore chopstick[5] = { 1, 1, 1, 1, 1 };
// 保证互斥地取筷子
semaphore mutex = 1;

// 第index个哲学家准备进餐
void philosopherWantToEat(int index) {
    // 左边的筷子在chopstick中的索引
    int leftChopstick = index;
    // 右边的筷子在chopstick中的索引
    int rightChopstick = (index + 1) % 5;

    // 锁住, 确保同时拿起两只筷子
    P(mutex);
    P(chopstick[leftChopstick]);
    P(chopstick[rightChopstick]);
    V(mutex);

    eat();

    // 放下筷子
    V(chopstick[leftChopstick]);
    V(chopstick[rightChopstick]);
}
```

## 解决方案二

限制就餐的哲学家数量: 只要同时进餐的哲学家不超过四人时, 即使在最坏情况下, 也至少有一个哲学家能够拿到多出来的那一只筷子。

```cpp
// 5个筷子
semaphore chopstick[5] = { 1, 1, 1, 1, 1 };
// 限制就餐的哲学家数量
semaphore maxCount = 4;

// 第index个哲学家准备进餐
void philosopherWantToEat(int index) {
    // 左边的筷子在chopstick中的索引
    int leftChopstick = index;
    // 右边的筷子在chopstick中的索引
    int rightChopstick = (index + 1) % 5;

    // 确保同时就餐的哲学家数量小于4
    P(maxCount);
    P(chopstick[leftChopstick]);
    P(chopstick[rightChopstick]);

    eat();

    // 放下筷子
    V(chopstick[leftChopstick]);
    V(chopstick[rightChopstick]);
    V(maxCount);
}
```

## 解决方案三

规定奇数位的哲学家先拿左边的筷子, 再拿右边的筷子。而偶数位的哲学家先拿右边的再拿左边的。这样就能够保证至少有一个哲学家能够获得两只筷子。

```cpp
// 5个筷子
semaphore chopstick[5] = { 1, 1, 1, 1, 1 };

// 第index个哲学家准备进餐
void philosopherWantToEat(int index) {
    // 左边的筷子在chopstick中的索引
    int leftChopstick = index;
    // 右边的筷子在chopstick中的索引
    int rightChopstick = (index + 1) % 5;

    if (index & 1) {
        // 奇数, 先拿左边的筷子
        P(chopstick[leftChopstick]);
        P(chopstick[rightChopstick]);
    } else {
        // 偶数, 先拿右边的筷子
        P(chopstick[rightChopstick]);
        P(chopstick[leftChopstick]);
    }

    eat();

    // 放下筷子
    V(chopstick[leftChopstick]);
    V(chopstick[rightChopstick]);
}
```
