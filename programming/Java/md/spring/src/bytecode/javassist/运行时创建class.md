# 运行时创建 class

```java
package org.example;

import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;
import javassist.Modifier;

import java.lang.reflect.Method;

public class JavassistDemo {

    public static void genClass() throws Exception {
        ClassPool pool = ClassPool.getDefault();
        // 创建一个类
        CtClass classDemo = pool.makeClass("org.example.Demo");

        // 新增一个方法
        CtMethod preProcessing = new CtMethod(CtClass.intType,
                "test", new CtClass[]{}, classDemo);
        preProcessing.setModifiers(Modifier.PUBLIC);
        preProcessing.setBody("{ System.out.println(\"ok\"); return 1; }");
        classDemo.addMethod(preProcessing);

        // 实例化Demo
        Object demo = classDemo.toClass().newInstance();
        // 调用test方法
        Method testMethod = demo.getClass().getMethod("test");
        Object returnedValue = testMethod.invoke(demo);
        System.out.println(returnedValue);
    }

    public static void main(String[] args) {
        try {
            genClass();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```
