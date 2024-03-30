# VMThread::loop

VMThread 启动后, 会一直执行 VMThread::loop(), 等待处理 VM_Operation, loop()函数会不断读取 `_next_vm_operation` 进行执行。
