# 实现类模块

```java
package com.example.device;

import com.example.transfer.api.Transfer;

public class Computer implements Transfer {

    /**
     * 下载数据
     */
    @Override
    public boolean downloadData(String name) {
        System.out.println("from computer");
        System.out.println(name + "downloading...");
        return true;
    }
}
```

## 模块描述符

```java
module data.transfer.computer {
    // 导入接口
    requires data.transfer.api;
    // 提供了Transfer接口的一个实现类: Computer
    provides com.example.transfer.api.Transfer with com.example.device.Computer;
}
```
