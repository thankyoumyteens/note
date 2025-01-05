# 基本使用

makefile 语法

```
target : prerequisites
	recipe
	...
	...
```

- target: 一个或多个可执行文件或者 `.o` 文件, 还可以是一个标签(label)
- prerequisites: 生成该 target 需要依赖的文件
- recipe: 该 target 要执行的任意的 shell 命令, 注意 recipe 前的换行符不能用空格替代

## 示例

1. 创建 hello.h

```cpp
#ifndef HELLO_H
#define HELLO_H
void hello();
#endif
```

2. 创建 hello.cpp

```cpp
#include <iostream>

void hello() {
    std::cout << "Hello, World!" << std::endl;
}
```

3. 创建 main.cpp

```cpp
#include "hello.h"

int main() {
    hello();
    return 0;
}
```

4. 创建 Makefile (注意文件中不能用空格替代换行符)

```makefile
hello : main.o hello.o
	/opt/homebrew/bin/g++-14 -o hello main.o hello.o

main.o : main.cpp hello.h
	/opt/homebrew/bin/g++-14 -c main.cpp

hello.o : hello.cpp hello.h
	/opt/homebrew/bin/g++-14 -c hello.cpp

clean :
	rm hello main.o hello.o
```

5. 构建

```sh
gmake
```

6. 运行:

```sh
./hello
```

7. 清理:

```sh
gmake clean
```

make 的执行流程:

1. make 会在当前目录下寻找名字叫 `Makefile` 或 `makefile` 的文件
2. 如果找到, 它会找文件中的第一个 target
   ```
   hello : main.o hello.o
   ```
3. 如果 `hello` 文件不存在, 或者 `hello` 所依赖的 `main.o` 或 `hello.o` 文件的文件修改时间要比 `hello` 这个文件新, 那么, 就会执行 `hello` 下面所定义的命令来重新生成 `hello` 文件
   ```
   /opt/homebrew/bin/g++-14 -o hello main.o hello.o
   ```
4. 如果 `hello` 所依赖的 `main.o` 文件不存在, 那么 make 会继续在当前文件中找到 target 为 `main.o` 的配置
   ```
   main.o : main.cpp hello.h
       /opt/homebrew/bin/g++-14 -c main.cpp
   ```
5. 如果找到则再根据 `main.o` 的规则生成 `main.o` 文件
6. 生成 `main.o` 文件后, 如果 `hello` 所依赖的 `hello.o` 文件也不存在, 那么 make 会继续在当前文件中找到 target 为 `hello.o` 的配置
   ```
   hello.o : hello.cpp hello.h
       /opt/homebrew/bin/g++-14 -c hello.cpp
   ```
7. 如果找到则再根据 `hello.o` 的规则生成 `hello.o` 文件
8. 最后再用 `main.o` 和 `hello.o` 文件生成 make 的最终目标 `hello` 文件

最后的 clean 不是一个文件, 而是一个动作, 其冒号后什么也没有, 那么 make 就不会自动去找它的依赖, 也就不会自动执行其后所定义的命令。要执行其后的命令, 就要在 make 命令后加上这个动作的名字: `make clean`, 以此来清除所有的目标文件, 以便重新编译。
