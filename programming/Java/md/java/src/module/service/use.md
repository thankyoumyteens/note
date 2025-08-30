# 使用者模块

```java
package com.example.use;

import java.util.ServiceLoader;

import com.example.transfer.api.Transfer;

public class Main {
    public static void main(String[] args) {
        // 获取Transfer接口的所有可用的实现类
        ServiceLoader<Transfer> implList = ServiceLoader.load(Transfer.class);
        // 调用获取到的所有实现类
        for (Transfer impl : implList) {
            System.out.println(impl.downloadData("setup.exe"));
        }
    }
}
```

## 模块描述符

```java
module user.use {
    // 导入接口
    requires data.transfer.api;
    // 告诉java模块系统, 本模块需要使用Transfer接口的实现类
    uses com.example.transfer.api.Transfer;
}
```

从理论上讲，即使在运行时没有绑定任何服务，应用程序也可以启动。此时调用 `ServiceLoader::load` 不会产生任何实例。
