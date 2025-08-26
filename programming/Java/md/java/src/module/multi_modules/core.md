# 提供方法的模块

CalcCore.java 的内容

```java
package com.example.calc.core;

public class CalcCore {
    public int add(int a, int b) {
        return a + b;
    }
}
```

## 模块描述符

```java
module calc.core {
    exports com.example.calc.core;
}
```

calc.core 模块需要导出包含 CalcCore 类的包。

通过使用关键字 exports，可以将模块中的包公开以供其他模块使用。通过声明导出包 com.example.calc.core 后，其所有的 public 类型都可以被其他模块使用。反之，模块中未导出的包都是模块私有的。

一个模块可以导出多个包。
