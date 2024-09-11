# 控制某个方法并发访问线程的数量

使用信号量 Semaphore

1. 创建信号量, 指定资源个数 `Semaphore semaphore = new Semaphore(3)`
2. 线程运行后获取资源, 没有资源则会阻塞 `semaphore.acquire()`
3. 运行完成后释放资源 `semaphore.release()`
