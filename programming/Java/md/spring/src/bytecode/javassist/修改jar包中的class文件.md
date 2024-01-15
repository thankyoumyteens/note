# 修改 jar 包中的 class 文件

```java
package org.example;

import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;

public class JavassistDemo {

    public static void editClass() throws Exception {
        ClassPool pool = ClassPool.getDefault();

        pool.insertClassPath("C:\\Users\\Public\\spring-context-5.2.5.RELEASE.jar");
        CtClass classPathXmlApplicationContext = pool.get("org.springframework.context.support.ClassPathXmlApplicationContext");

        // 修改getConfigResources方法
        CtMethod getConfigResources = classPathXmlApplicationContext.getDeclaredMethod("getConfigResources");
        getConfigResources.insertBefore("System.out.println(\"pre\");");

        // 生成class文件
        classPathXmlApplicationContext.writeFile("C:\\Users\\Public");
    }

    public static void main(String[] args) {
        try {
            editClass();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

之后可以用压缩软件将原 jar 包中的 class 文件替换为新生成的 class 文件。
