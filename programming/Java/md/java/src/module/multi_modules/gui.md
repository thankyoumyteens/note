# 使用服务的模块

CalcMain.java 的内容

```java
package com.example.calc.gui;

import com.example.calc.core.CalcCore;

public class CalcMain {
    public static void main(String[] args) {
        CalcCore calc = new CalcCore();
        System.out.println("1+1=" + calc.add(1, 1));
    }
}
```

## 模块描述符

```java
module calc.gui {
    requires calc.core;
}
```

calc.gui 模块需要声明对 calc.core 模块的依赖。

当编译 CalcMain.java 时, javac 就会根据模块描述符里的依赖, 在模块路径中查找 calc.core 模块并进行编译。
