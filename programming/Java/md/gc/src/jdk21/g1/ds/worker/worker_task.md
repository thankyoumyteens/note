# WorkerTask

WorkerTask 类是 OpenJDK 中垃圾收集器工作线程的任务抽象基类, 所有需要由工作线程执行的垃圾收集任务都需要继承此类并实现 work 方法

```cpp
// --- src/hotspot/share/gc/shared/workerThread.hpp --- //

/**
 * 继承自CHeapObj<mtInternal>，表明此类实例分配在C堆上，内存类型为mtInternal
 */
class WorkerTask : public CHeapObj<mtInternal> {
private:
    const char *_name; // 任务名称，用于日志和调试
    const uint _gc_id; // 垃圾收集周期ID，标识任务所属的GC周期

public:
    /**
     * 构造函数，初始化任务名称和GC ID
     * @param name 任务名称字符串
     */
    explicit WorkerTask(const char *name) :
            _name(name),
            _gc_id(GCId::current_or_undefined()) {}

    /**
     * 获取任务名称
     * @return 任务名称字符串指针
     */
    const char *name() const { return _name; }

    /**
     * 获取任务所属的GC周期ID
     * @return GC ID值
     */
    const uint gc_id() const { return _gc_id; }

    /**
     * 纯虚函数，定义具体的任务逻辑，由子类实现
     * @param worker_id 执行该任务的工作线程ID
     */
    virtual void work(uint worker_id) = 0;
};
```
