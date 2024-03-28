# 缓存一致性

CPU 的运算速度远快于主存, 为了解决这个问题, 一般会在 CPU 与主存之间添加一级或者多级高速缓存(Cache)。按照数据读取顺序和与 CPU 结合的紧密程度, CPU 缓存可以分为一级缓存(L1)、二级缓存(L2)和三级缓存(L3)。每一级缓存中所储存的全部数据都是下一级缓存的一部分。越靠近 CPU 的缓存越快也越小, L1 和 L2 只能被一个单独的 CPU 核心使用, L3 被所有 CPU 核心共享。当 CPU 执行运算的时候, 它先去 L1 查找所需的数据, 再去 L2, 然后是 L3, 如果这些缓存中都没有所需的数据, 就要去主存中查找。

Cache 是以缓存行(Cache Line)为单位存储的, 缓存行是 CPU 和主存之间数据传输的最小单位, 每个缓存行的大小通常是 64 字节。

![](../img/cpu_cache.png)

如果数据写入 Cache 之后, 主存与 Cache 相对应的数据将会不同, 这种情况下需要把 Cache 中的数据同步回主存中。

## 写回

CPU 通过写回(Write Back)策略将 Cache 中的数据同步回内存。

1. 当发生写操作时, 如果数据已经在 Cache 里了, 则直接修改 Cache 里的数据, 同时标记 Cache 里的这个 Cache Line 为脏(Dirty), 表示 Cache 里面的这个 Cache Line 的数据和内存是不一致的, 这种情况是不用把数据写到内存里的
2. 当发生写操作时, 如果数据不在 Cache 中, CPU 会选中一个 Cache Line 用于缓存该数据, 并且检查这个 Cache Line 有没有被标记为脏, 如果是脏的话, 就会把这个 Cache Line 里的数据写回到内存, 然后再把当前要写入的数据, 写入到这个 Cache Line 里, 同时也把它标记为脏。如果 Cache Line 没有被标记为脏, 就直接将数据写入到这个 Cache Line 里, 然后再把这个 Cache Line 标记为脏的就好了。

在把数据写入到 Cache 的时候, 只有在缓存不命中, 同时数据对应的 Cache Line 为脏的情况下, 才会将数据写到内存中, 而在缓存命中的情况下, 只需把该数据对应的 Cache Line 标记为脏即可, 而不用写到内存里。如果大量的操作都能够命中缓存, 那么大部分时间 CPU 都不需要直接读写内存。

这种方式在单核 CPU 中不会由问题, 但是在多核 CPU 中就会有缓存一致性问题。

## 缓存一致性问题

例如两个 CPU 同时拥有共享变量 a, 且 a=0, 这时如果 CPU 0 修改了 a 的值为 1, CPU 使用写回策略, 先把值为 1 的修改写入到自己的 L1/L2 Cache 中, 然后把 Cache 中对应的 Cache Line 标记为脏, 这个时候数据其实没有被同步到内存中, CPU 0 的这个 Cache Line 要被替换的时候, 数据才会写入到内存里。如果此时另一个 CPU 1 尝试从内存读取变量 a 的值, 由于 L1/L2 Cache 是每个 CPU 核心私有的, 它读到的将会是错误的值 0。

要解决这⼀问题, 就要满足两个条件: 

1. 写传播(Wreite Propagation): 在一个 CPU 核⼼⾥的 Cache 数据更新时, 必须要同步到其他核⼼的 Cache 中
2. 事务的串行化(Transaction Serialization): 在一个 CPU 核心里面的读取和写入, 在其他 CPU 中看起来, 顺序是一样的

## 总线嗅探

总线嗅探实现了写传播。

CPU 和内存或其他 CPU 的通信是通过嗅探(Snoop)内存或其他 CPU 发出的请求消息完成的, 有时 CPU 也需要针对总线中的某些请求消息进行响应。这被称为总线嗅探(Bus Snooping)。

当 CPU 0 修改了 Cache 中变量 a 的值时, 会通过总线把这个事件⼴播通知给其他所有的核⼼, 每个 CPU 核⼼都会监听总线上的⼴播事件, 并检查⾃⼰的 Cache ⾥⾯是否有变量 a, 如果 CPU 1 的 Cache 中有变量 a, 那么也需要更新⾃⼰的 Cache 中的变量 a 的值。

CPU 需要每时每刻监听总线上的⼀切活动, 但是不管别的核⼼的 Cache 是否缓存相同的数据, 都需要发出⼀个⼴播事件, 这⽆疑会加重总线的负担。

总线嗅探机制中的消息: 

- Read: 通知其他 CPU 和内存, 当前 CPU 准备读取某个数据。该消息内包含待读取数据的内存地址
- Read Response: 该消息内包含了被请求读取的数据。该消息可能是内存返回的, 也可能是其他高速缓存嗅探到 Read 消息后返回的
- Invalidate: 通知其他 CPU 将指定内存地址的数据所在的 Cache Line 设置为已失效
- Invalidate Acknowledge: 接收到 Invalidate 消息的 CPU 必须回复此消息, 表示已经将对应的 Cache Line 设置为已失效
- Read Invalidate: 此消息为 Read 和 Invalidate 消息组成的复合消息, 主要是用于通知其他 CPU 当前 CPU 准备更新一个数据了, 并请求其他 CPU 将对应的 Cache Line 设置为已失效。接收到该消息的 CPU 必须回复 Read Response 和 Invalidate Acknowledge 消息
- Writeback: 消息包含了需要写入内存的数据和其对应的内存地址

## MESI 协议

MESI 协议基于总线嗅探机制实现了事务串形化, 降低了总线带宽压⼒。

MESI 协议有四种状态: 

1. M(Modified): 已修改, 表示这个 Cache Line 中的数据已经被修改了, 还没有写回到内存里去
2. E(Exclusive): 独占, 数据只存储在⼀个 CPU 核⼼的 Cache ⾥, ⽽其他 CPU 核⼼的 Cache 没有该数据, 可以直接修改数据, ⽽不需要通知其他 CPU 核⼼。在独占状态下的数据, 如果有其他核⼼从内存读取了相同的数据到各⾃的 Cache, 那么这个时候, 独占状态就会变成共享状态
3. S(Shared): 共享, 相同的数据在多个 CPU 核⼼的 Cache ⾥都有, 当要更新 Cache ⾥⾯的数据的时候, 不能直接修改, ⽽是要先向所有的其他 CPU 核⼼⼴播⼀个请求, 要求先把其他核⼼中对应的 Cache Line 标记为已失效, 然后再更新当前 Cache ⾥⾯的数据
4. I(Invalid): 已失效, 表示这个 Cache Line 已经失效, 不可以读取

四种状态的转换: 

1. 当 CPU 0 从内存中读取变量 a 的值时, 数据被缓存在 CPU 0 ⾃⼰的 Cache ⾥⾯, 此时其他 CPU 核⼼的 Cache 没有缓存该数据, 于是标记 Cache Line 状态为【独占】, 此时其 Cache 中的数据与内存是⼀致的
2. 然后 CPU 1 也从内存读取了变量 a 的值, 此时会发送消息给其他 CPU 核⼼, 由于 CPU 0 已经缓存了该数据, 所以会把数据返回给 CPU 1。在这个时候, CPU 0 和 CPU 1 缓存了相同的数据, Cache Line 的状态就会变成【共享】, 并且其 Cache 中的数据与内存也是⼀致的
3. 当 CPU 0 要修改 Cache 中变量 a 的值, 发现数据对应的 Cache Line 的状态是共享状态, 则要向其他所有 CPU 核⼼⼴播⼀个请求, 要求先把其他核⼼的 Cache 中对应的 Cache Line 标记为【⽆效】状态, 然后 CPU 0 要等到其他核心的回复后, 才能更新 Cache ⾥⾯的数据, 同时标记 Cache Line 为【已修改】状态, 此时 Cache 中的数据与内存不⼀致
4. 如果 CPU 0 继续修改 Cache 中变量 a 的值, 由于此时的 Cache Line 是【已修改】状态, 因此不需要给其他 CPU 核⼼发送消息, 直接更新数据即可
5. 如果变量 a 对应的 Cache Line 要被替换, 发现 Cache Line 状态是【已修改】状态, 就会在替换前先把数据同步到内存

MESI 协议解决了缓存一致性问题, 但是其自身也存在一个性能问题: CPU 执行写内存操作时, 必须等待其他所有 CPU 将其高速缓存中的相应副本数据删除并接收到这些 CPU 所回复的 Invalidate Acknowledge/Read Response 消息之后才能将数据写入 Cache。为了规避和减少这种等待造成的写操作的延迟, 硬件设计者引入了写缓冲器和无效化队列。

## 写缓冲器

写缓冲器(Store Buffer, 也称 Write Buffer)是 CPU 核心内部的一个容量比高速缓存还小的私有高速存储部件(写缓冲器的容量大小通常等于 L1 Cache 的缓存行宽度, 比如 32 字节、64 字节)。每个 CPU 核心都有自己的 Store Buffer, 其内部可能包含若干条目(Entry)。一个 CPU 核心无法读取另外一个 CPU 核心上的 Store Buffer 中的内容。

引入 Store Buffer 之后, CPU 在执行写操作时的处理: 

1. 如果相应的 Cache Line 状态为 E 或者 M, 那么 CPU 可能会直接将数据写入相应的缓存行而无需发送任何消息(x86 架构的 CPU 会不管相应的 Cache Line 状态如何, 直接先将每一个写操作的结果存入 Store Buffer)
2. 如果相应的 Cache Line 状态为 S, 那么 CPU 会先将写操作的相关数据(包括数据和待操作的内存地址)存入 Store Buffer 的 Entry 之中, 并发送 Invalidate 消息, 然后 CPU 不会继续等待, 而是去处理其它任务。等收到 Invalidate Acknowledge 消息之后, 再将 Store Buffer 中的数据写入相应的 Cache Line
3. 如果相应的 Cache Line 状态为 I, 那么 CPU 会先将写操作相关数据存入 Store Buffer 的 Entry 之中, 并发送 Read Invalidate 消息, 然后 CPU 不会继续等待, 而是去处理其它任务。等收到 Read Response 消息之后, 再将 Store Buffer 中的数据写入相应的 Cache Line

## 无效化队列

引入无效化队列(Invalidate Queue)之后, CPU 在接收到 Inavalidate 消息之后并不删除消息中指定地址相应的副本数据, 而是将消息存入无效化队列之后就回复 Invalidate Acknowedge 消息, 过段时间, 再从无效化队列中取出 Invalidate 消息消费, 将自己对应的 Cache Line 状态设为 I。无效化队列减少了写操作执行 CPU 所需要的等待时间。有些 CPU(比如 x86)可能没有使用无效化队列。
