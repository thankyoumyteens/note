# 接口模块

```java
package com.example.transfer.api;

public interface Transfer {
    /**
     * 下载数据
     */
    boolean downloadData(String name);
}
```

## 模块描述符

```java
module data.transfer.api {
    exports com.example.transfer.api;
}
```
