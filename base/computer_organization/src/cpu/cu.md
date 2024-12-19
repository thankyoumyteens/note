# 控制器

控制器的输入信号:

- 时钟: 完成每个操作都需要占用一定的时间, 各个操作之间有先后次序之分, 因此控制单元需要在时钟的控制下按照一定的顺序发出控制信号
- 指令寄存器(IR): 指令寄存器的操作码字段决定了指令的操作类型，因此是控制单元的输入信号
- 标志: 控制单元有时候需要根据 CPU 当前的状态来产生相应的控制信号，因此“标志”也是输入信号
- 来自总线的控制信号，如中断请求等

控制器的输出信号:

- CPU 内的控制信号: CPU 内的数据传输，或控制 ALU 执行不同的运算等
- 送至系统总线的信号: 如控制主存读/写，I/O 操作，中断响应等

## CPU 内部采用单总线方式的数据通路

- bus: CPU 内部的总线, 用来在 CPU 内部传输数据
- Y 和 Z 寄存器: 用于暂时存储参与运算的数据和中间结果
- 红线: CU 的控制信号
- 黑线: 数据

![](../img/cu1.jpg)

寄存器之间的数据传送, 以 PC 中的数据送入 MAR 为例:

1. PC 中的数据送入 MAR
   - PC<sub>out</sub> 和 MAR<sub>in</sub> 有效
   - (PC) -> bus -> MAR

主存与 CPU 的数据传送, 以 CPU 从主存中取指令为例:

1. PC 中的数据送入 MAR
   - PC<sub>out</sub> 和 MAR<sub>in</sub> 有效
   - (PC) -> bus -> MAR
2. CU 通过控制总线向主存发送读信号: 1 -> 控制总线 -> R
3. 把指令从主存送入 MDR:
   - MDR<sub>in</sub> 有效
   - M(MAR) -> 数据总线 -> MDR
4. 把指令从 MDR 送入 IR:
   - MDR<sub>out</sub> 和 IR<sub>in</sub> 有效
   - (MDR) -> bus -> IR

执行算术/逻辑运算, 以加法为例:

1. 将指令的地址码送入 MAR
   - IR<sub>out</sub> 和 MAR<sub>in</sub> 有效
   - Ad(IR) -> bus -> MAR
   - 注意: 取指后 MDR 中保存的也是指令, 所以也可以从 MDR 中把指令送到 MDR: (MDR) -> bus -> MAR
2. 向主存发送读命令, 启动主存执行读操作: 1 -> R
3. 把加法运算的操作数从主存送入 MDR
   - MDR<sub>in</sub> 有效
   - M(MAR) -> 数据总线 -> MDR
4. 把操作数送入 Y 中暂存:
   - Y<sub>in</sub> 和 MDR<sub>out</sub> 有效
   - (MDR) -> bus -> Y
5. ACC 中存放的是被加数, 把 ACC 和 Y 相加, 结果暂存到 Z 中:
   - ALU<sub>in</sub> 和 ACC<sub>out</sub> 有效
   - CU 向 ALU 发送加法命令
   - (ACC) + (Y) -> Z
6. 把 Z 中的结果放回 ACC:
   - ACC<sub>in</sub> 和 Z<sub>out</sub> 有效
   - (Z) -> bus -> ACC

由于单总线方式在同一时刻只能进行一次数据传输操作, 而 ALU 同时需要两个输入, 所以要先把一个操作数临时存放到寄存器 Y 中。如果采用多总线方式, 则可以通过另一条内部总线直接把数据送给 ALU。

### 例题

设有如图所示的单总线结构，分析指令 ADD (R0),R1 的指令流程和控制信号。

![](../img/cpu6.jpg)

取指周期:

| 时序 | 微操作         | 有效控制信号                               |
| ---- | -------------- | ------------------------------------------ |
| 1    | (PC) -> MAR    | PC<sub>out</sub>, MAR<sub>in</sub>         |
| 2    | M(MAR) -> MDR  | MemR, MAR<sub>out</sub>, MDR<sub>in</sub>E |
| 3    | (MDR) -> IR    | MDR<sub>out</sub>, IR<sub>in</sub>         |
| 4    | 指令译码       | -                                          |
| 5    | (PC) + 1 -> PC | -                                          |

间址周期: 完成取数操作，被加数在主存中，加数已经放在寄存器 R<sub>1</sub> 中

| 时序 | 微操作                 | 有效控制信号                               |
| ---- | ---------------------- | ------------------------------------------ |
| 1    | (R<sub>0</sub>) -> MAR | R<sub>0out</sub>, MAR<sub>in</sub>         |
| 2    | M(MAR) -> MDR          | MemR, MAR<sub>out</sub>, MDR<sub>in</sub>E |
| 3    | (MDR) -> Y             | MDR<sub>out</sub>, Y<sub>in</sub>          |

执行周期:

| 时序 | 微操作                     | 有效控制信号                                                  |
| ---- | -------------------------- | ------------------------------------------------------------- |
| 1    | (R<sub>1</sub>) + (Y) -> Z | R<sub>1out</sub>, ALU<sub>in</sub>, CU 向 ALU 发 ADD 控制信号 |
| 2    | (Z) -> MDR                 | Z<sub>out</sub>, MDR<sub>in</sub>                             |
| 3    | (MDR) -> M(MAR)            | MemW, MDR<sub>out</sub>E, MAR<sub>out</sub>                   |

## CPU 内部采用专用数据通路方式

在任意两个需要通信的器件之间都建立专用的数据通路

![](../img/cpu7.jpg)

取指周期:

1. (PC) -> MAR, C<sub>0</sub> 有效
2. (MAR) -> 主存, C<sub>1</sub> 有效
3. 1 -> R
4. M(MAR) -> MDR, C<sub>2</sub> 有效
5. (MDR) -> IR, C<sub>3</sub> 有效
6. (PC) + 1 -> PC
7. Op(IR) -> CU, C<sub>4</sub> 有效
