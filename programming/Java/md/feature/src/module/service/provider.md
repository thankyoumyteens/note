# 提供服务的方式

可以通过两种方式创建服务实例:

1. 服务实现类必须具有 public 的无参数构造方法
2. 使用静态的提供者方法

## 提供者方法

提供者方法是一个名为 provider 的 public static 无参数方法，其返回类型是服务类型。在提供者方法中如何实例化服务完全取决于 provider 的实现，可以缓存并返回单例对象，也可以为每个调用者创建一个新的对象。

```java
package com.example.device;

import com.example.transfer.api.Transfer;

public class Computer implements Transfer {

    // 构造方法不对外提供
    private Computer(){}

    /**
     * 下载数据
     */
    @Override
    public boolean downloadData(String name) {
        System.out.println("from computer");
        System.out.println(name + "downloading...");
        return true;
    }

    // 提供者方法
    public static Computer provider() {
        return new Computer();
    }
}
```

如果 provider 方法与服务实现类不在同一个类中, 那么 module-info.java 中的 provides ... with ... 后的类要改成指向包含该 provider 法的类。
