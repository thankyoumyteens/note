# 刷新

刷新的原因: 电容内的电荷只能维持2ms, 2ms内必须刷新一次给电容充电

刷新的实质：先将原信息读出，再由刷新放大器形成原信息重新写入的过程

## 刷新与存取不能并行

因为内存就一套地址译码和片选装置，刷新与存取有相似的过程，它要选中一行——这期间片选线、地址线、地址译码器全被占用着。同理，刷新操作之间也不能并行——意味着一次只能刷一行。

## 假定

- 刷新周期为2ms
- 以行为单位, 每次刷新一行存储单元
- 存取周期为0.5μs，即刷新1行的时间为0.5μs
- 对128×128的矩阵的存储芯片进行刷新

# 集中刷新

集中刷新是在规定的一个刷新周期内，对全部存储单元集中一段时间逐行进行刷新，此刻必须停止读/写操作。

用0.5μs*128=64μs的时间对128行进行逐行刷新，由于这64μs的时间不能进行读/写操作，故称为“死时间”或访存“死区”。

由于存取周期为0.5μs，刷新周期为2ms，即4000个存取周期。

# 分散刷新

分散刷新是指对每行存储单元的刷新分散到每个存取周期内完成。其中，把机器的存取周期tc分成两段，前半段tM用来读/写信息，后半段tR用来刷新。

即在每个存取操作后绑定一个刷新操作。延长了存取周期，这样存取周期就成了0.5μs + 0.5μs =1μs。但是由于与存取操作绑定，就不需要专门给出一段时间来刷新了。

这样，每有128个读取操作，就会把0-127行全部刷新一遍。故每隔128μs 就可将存储芯片全部刷新一遍，即刷新周期是1μs×128=128μs远短于2ms，而且不存在停止读/写的死时间，但是存取周期长了，整个系统速度降低了。

# 异步刷新

具体操作为：在2ms内对128行各刷新一遍

即每隔15.6μs刷新一行(2000μs/128≈15.6μs)，而每行刷新的时间仍为0.5μs。这样，刷新一行只能停止一个存取周期，但对每行来说，刷新间隔时间仍为2ms，而死时间为0.5μs。（相对每一段来说，是集中式刷新，相对整体来说，是分散式刷新）

如果将DRAM的刷新安排在CPU对指令的译码阶段，由于这个阶段CPU不访问存储器，所以这种方案既克服了分散刷新需独占0.5μs用于刷新，使存取周期加长且降低系统速度的缺点，又不会出现集中刷新的访存“死区”问题，从根本上上提高了整机的工作效率。
