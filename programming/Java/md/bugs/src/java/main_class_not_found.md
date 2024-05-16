# 找不到或无法加载主类

## wrong name

执行

```sh
java HelloJNI
```

报错

```sh
错误: 找不到或无法加载主类 HelloJNI
原因: java.lang.NoClassDefFoundError: HelloJNI (wrong name: org/example/jnidemo/HelloJNI)
```

java 代码中包含 package: `package org.example.jnidemo;`, 需要退出到包的上级目录下执行:

```sh
cd ../../../
java org.example.jnidemo.HelloJNI
```
