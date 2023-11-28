# Cache的效率

设tc为访问一次Cache所需时间, tm为访问一次主存所需时间

设命中率为H, 即CPU欲访问的信息已在Cache中的比率, 则缺失（未命中）率M = 1 - H

# 系统的平均访问时间 t

## 方式1

先访问Cache, 若Cache未命中再访问主存

t=H×tc + (1-H)×(tc+tm)

## 方式2

同时访问 Cache和主存, 若Cache命中则立即停止访问主存

t=H×tc + (1-H)×tm
