# 运行时修改 class

```java
package org.example;

public class Demo {
    public String getMsg() {
        return "ok";
    }
}
```

```java
package org.example;

import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;
import javassist.Modifier;

import java.lang.reflect.Method;

public class JavassistDemo {

    /**
     * 需要保证org.example.Demo类被其它地方加载前调用此方法
     */
    public static void editClass() throws Exception {
        ClassPool pool = ClassPool.getDefault();
        CtClass classDemo = pool.get("org.example.Demo");

        // 新增方法
        CtMethod preProcessing = new CtMethod(CtClass.voidType,
                "preProcessing", new CtClass[]{}, classDemo);
        preProcessing.setModifiers(Modifier.PUBLIC);
        preProcessing.setBody("{ System.out.println(\"pre\"); }");
        classDemo.addMethod(preProcessing);

        CtMethod postProcessing = new CtMethod(CtClass.voidType,
                "postProcessing", new CtClass[]{}, classDemo);
        postProcessing.setModifiers(Modifier.PUBLIC);
        postProcessing.setBody("{ System.out.println(\"post\"); }");
        classDemo.addMethod(postProcessing);

        // 修改getMsg方法
        CtMethod getMsg = classDemo.getDeclaredMethod("getMsg");
        // 在方法的起始位置插入代码
        getMsg.insertBefore("preProcessing();");
        // 在方法的所有 return 语句前插入代码
        getMsg.insertAfter("postProcessing();");

        // 实例化Demo
        Object demo = classDemo.toClass().newInstance();
        // 调用getMsg方法
        Method getMsgMethod = demo.getClass().getMethod("getMsg");
        Object returnedValue = getMsgMethod.invoke(demo);
        System.out.println(returnedValue);
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
