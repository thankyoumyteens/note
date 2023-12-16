# VMThread::execute

在分配对象时, 如果需要 GC 的话, G1 会创建一个 VM_G1CollectForAllocation 对象交给 VMThread 执行。 JVM 会将 \_next_vm_operation 设置为当前的 VM_G1CollectForAllocation, 之后 JavaThread 会一直阻塞, 直到当前 VM_G1CollectForAllocation 执行结束。

VMThread 启动后, 会一直执行 VMThread::loop(), 等待处理 VM_Operation, loop()函数会不断读取 \_next_vm_operation 进行执行。
