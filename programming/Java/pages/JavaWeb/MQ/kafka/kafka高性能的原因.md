# 顺序写磁盘

顺序写磁盘相比磁盘的随机写快很多

# 利用Page Cache空中接力的方式来实现高效读写

操作系统本身有一层缓存，叫做page cache，是在内存里的缓存，我们也可以称之为os cache，意思就是操作系统自己管理的缓存。原理就是Page Cache可以把磁盘中的数据缓存到内存中，把对磁盘的访问改为对内存的访问。

# 零拷贝方式

假如不用零拷贝方式，kafka从磁盘读数据发送给下游的消费者大概的过程为：kafka首先看看要读的数据在不在os cache里，如果不在的话就从磁盘文件里读取数据后放入os cache，接着再到应用程序进程的缓存里，再到操作系统层面的Socket缓存里，最后从Socket缓存里提取数据后发送到网卡，最后发送出去给消费者。

零拷贝：直接让操作系统的cache中的数据发送到网卡后传输给下游的消费者，直接跳过了两次拷贝数据的步骤，Socket缓存中仅仅会拷贝一个描述符过去，不会拷贝数据到Socket缓存。
