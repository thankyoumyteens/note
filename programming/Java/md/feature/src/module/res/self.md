# 加载本模块的资源

目录结构

```
demo
├── com
│   └── example
│       ├── Main.java
│       └── inPackage.txt
├── module-info.java
└── topLevel.txt
```

Main.java

```java
package com.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class Main {

    public static void main(String[] args) {
        Class<Main> c = Main.class;
        Module module = c.getModule();
        // 加载顶级资源
        try (InputStream topLevel = module.getResourceAsStream("topLevel.txt")) {
            BufferedReader reader = new BufferedReader(new InputStreamReader(topLevel));
            String line = reader.readLine();
            System.out.println(line);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        // 加载位于文件夹内的资源
        try (InputStream inPackage = module.getResourceAsStream("com/example/inPackage.txt")) {
            BufferedReader reader = new BufferedReader(new InputStreamReader(inPackage));
            String line = reader.readLine();
            System.out.println(line);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
```

## 编译

```sh
javac -d out/demo \
    --module-path out \
    src/demo/com/example/Main.java \
    src/demo/module-info.java

# javac不支持复制资源文件到输出目录
# 需要手动复制资源文件到输出目录
cp src/demo/topLevel.txt out/demo/
cp src/demo/com/example/inPackage.txt out/demo/com/example/
```

## 运行

```sh
java --module-path out --module demo/com.example.Main
```
