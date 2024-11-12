# 变量

声明变量:

```
变量名 = 值
```

使用变量:

```
$(变量名)
```

## 把 g++-14 替换成变量

```makefile
cc = /opt/homebrew/bin/g++-14

hello : main.o hello.o
	$(cc) -o hello main.o hello.o

main.o : main.cpp hello.h
	$(cc) -c main.cpp

hello.o : hello.cpp hello.h
	$(cc) -c hello.cpp

clean :
	rm hello main.o hello.o
```

## 把依赖项替换成变量

```makefile
cc = /opt/homebrew/bin/g++-14
dependencies = main.o hello.o

hello : $(dependencies)
	$(cc) -o hello $(dependencies)

main.o : main.cpp hello.h
	$(cc) -c main.cpp

hello.o : hello.cpp hello.h
	$(cc) -c hello.cpp

clean :
	rm hello $(dependencies)
```
