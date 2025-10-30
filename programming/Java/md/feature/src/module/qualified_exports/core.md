# 提供功能的模块

注意 Mask 类中使用到了反射

```java
package com.example.mask;

import java.lang.reflect.Field;

public class Mask {
    /**
     * 字段脱敏
     */
    public static Object maskFields(Object obj, Class<?> clz) {
        Field[] fields = clz.getFields();
        for (Field field : fields) {
            try {
                Object o = field.get(obj);
                if (o instanceof String) {
                    String str = (String) o;
                    if (str.length() > 4) {
                        field.set(obj, str.substring(0, 2) + "****" + str.substring(4));
                    } else {
                        field.set(obj, str.substring(0, 2) + "****");
                    }
                }
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            }
        }
        return obj;
    }
}
```

## 模块描述符

```java
module data.masking {
    exports com.example.mask;
}
```
