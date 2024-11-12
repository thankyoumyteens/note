# 隐式规则

make 可以自动推导文件以及文件依赖关系后面的命令，只要 make 看到一个 `.o` 文件，它就会自动的把 `.c` 或 `.cpp` 文件加在依赖关系中，比如 make 遇到了 `main.o` ，那么 `main.cpp` 就会它的依赖文件。并且编译命令 `cc -c main.cpp` 也会被推导出来，于是 makefile 可以简化成:

```makefile
dependencies = main.o hello.o

hello : $(dependencies)
	cc -o hello $(dependencies)

main.o : hello.h

hello.o : hello.h

clean :
	rm hello $(dependencies)
```

## mac 下的问题

mac 在编译 C++ 程序的时候, 需要在编译命令中添加 `-lstdc++` 参数，引入 C++ 的标准库:

```sh
cc -lstdc++ -o main.cpp
```

所以上面的写法在 mac 中会报错: Undefined symbols for architecture arm64。

所以 mac 中只能省略默认的 `.cpp` 依赖, 还是需要加上编译命令:

```makefile
cc = /opt/homebrew/bin/g++-14
dependencies = main.o hello.o

hello : $(dependencies)
	$(cc) -o hello $(dependencies)

main.o : hello.h
	$(cc) -c main.cpp

hello.o : hello.h
	$(cc) -c hello.cpp

clean :
	rm hello $(dependencies)
```
