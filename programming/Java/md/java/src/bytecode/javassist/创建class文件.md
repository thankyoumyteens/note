# 创建 class 文件

```java
package org.example;

import javassist.*;

public class JavassistDemo {

    public static void createClassFile() throws Exception {
        ClassPool pool = ClassPool.getDefault();

        // 创建Person类
        CtClass classPerson = pool.makeClass("com.demo.Person");

        // 为Person类添加一个字段 private String name
        CtField fieldName = new CtField(pool.get("java.lang.String"), "name", classPerson);
        fieldName.setModifiers(Modifier.PRIVATE);
        classPerson.addField(fieldName);

        // 生成getter和setter方法
        classPerson.addMethod(CtNewMethod.setter("setName", fieldName));
        classPerson.addMethod(CtNewMethod.getter("getName", fieldName));

        // 为Person类添加无参构造方法
        CtConstructor cons = new CtConstructor(new CtClass[]{}, classPerson);
        cons.setBody("{}");
        classPerson.addConstructor(cons);

        // 为Person类添加有参构造方法
        cons = new CtConstructor(new CtClass[]{pool.get("java.lang.String")}, classPerson);
        // $0 代表 this
        // $1,$2,$3... 代表方法参数
        cons.setBody("{$0.name = $1;}");
        classPerson.addConstructor(cons);

        // 为Person类添加一个自定义方法
        // public String testName(String)
        CtMethod ctMethod = new CtMethod(pool.get("java.lang.String"),
                "testName", new CtClass[]{pool.get("java.lang.String")}, classPerson);
        ctMethod.setModifiers(Modifier.PUBLIC);
        ctMethod.setBody("{ return $0.name + $1; }");
        classPerson.addMethod(ctMethod);

        // 生成.class文件
        // 文件路径: C:\Users\Public\com\demo\Person.class
        classPerson.writeFile("C:\\Users\\Public");
    }

    public static void main(String[] args) {
        try {
            createClassFile();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 生成的 class 文件

```java
package com.demo;

public class Person {
  private String name;

  public void setName(String paramString) {
    this.name = paramString;
  }

  public String getName() {
    return this.name;
  }

  public Person() {}

  public Person(String paramString) {
    this.name = paramString;
  }

  public String testName(String paramString) {
    return this.name + paramString;
  }
}
```
