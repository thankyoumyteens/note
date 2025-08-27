# 使用服务的模块

User.java

```java
package com.example.ui;

public class User {
    public String username;
    public String password;
    public String phone;
    public String email;

    @Override
    public String toString() {
        return "User{" +
                "username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", phone='" + phone + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
```

Main.java

```java
package com.example.ui;

import com.example.mask.Mask;

public class Main {
    public static void main(String[] args) {
        User user = new User();
        user.username = "admin";
        user.password = "123456";
        user.phone = "13800000000";
        user.email = "admin@example.com";
        System.out.println(user);
        // 字段脱敏
        user = (User) Mask.maskFields(user, User.class);
        System.out.println(user);
    }
}
```

## 模块描述符

```java
module user.gui {
    requires data.masking;
}
```
