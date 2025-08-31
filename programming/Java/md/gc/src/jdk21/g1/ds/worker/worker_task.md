# WorkerTask

```cpp
// --- src/hotspot/share/gc/shared/workerThread.hpp --- //

class WorkerTask : public CHeapObj<mtInternal> {
private:
    const char *_name;
    const uint _gc_id;

public:
    explicit WorkerTask(const char *name) :
            _name(name),
            _gc_id(GCId::current_or_undefined()) {}

    const char *name() const { return _name; }

    const uint gc_id() const { return _gc_id; }

    // 具体的任务逻辑
    virtual void work(uint worker_id) = 0;
};
```
