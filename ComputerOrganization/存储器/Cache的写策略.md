# 写直达法

当CPU对Cache写命中时，必须把数据同时写入Cache和主存。当某一块需要替换时，也不必把这一块写回到主存中，新调入的块可以可以立即把在Cache的这一块覆盖。

这种方法实现简单，而且能随时保持主存数据的正确性，但可能增加多次不必要的主存写入，降低存取速度。

## 优化

可以在Cache和主存之间加入SRAM实现的FIFO队列作为写缓冲, Cache直接向缓冲区中写入修改的数据, 再由缓冲区自己逐渐写入到主存中, 使得CPU可以不用等待主存写入完成。

使用写缓冲，CPU写的速度很快，若写操作不频繁，则效果很好。若写操作很频繁，可能会因为写缓冲饱和而发生阻塞。

# 写回法

当CPU对Cache写命中时，被写数据只写入Cache，不写入主存。仅当需要替换时，才把已经修改过的Cache块写回到主存。

采用这种方法时需要一个标志位，来标记一个块中的任一单元是否被修改。若被修改，则标志位置1。在需要替换掉这一块时，如果标志位为1，则必须先把这一块写回到主存中，然后才能调入新的块；否则则不必写回主存。

这种方法操作速度快，但因主存中的字块未及时修改而有可能出错。

# 写分配法

当CPU对Cache写不命中时，把主存中的块调入Cache，在Cache中修改。

通常搭配写回法使用

# 非写分配法

当CPU对Cache写不命中时只写入主存，不调入Cache。

搭配全写法使用
