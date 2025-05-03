# 自动推导返回值

decltype 语法: `decltype(表达式) 变量名`

### 1. 如果 expression 是没有用括号括起来的标识符，则变量的类型与该标识符的类型相同，包括 const 等限定符

```cpp
int a = 1;
decltype(a) b = 2;
```

### 2. 如果 expression 是函数调用，则变量的类型与函数的返回值类型相同(函数不能返回 void，但可以返回 void\*)

```cpp
int func() {
    return 0;
}

int main(int argc, char *argv[]) {
    // int
    decltype(func()) a = 1;
    // 函数func的指针
    decltype(func) *b;

    return 0;
}
```

### 3. 如果 expression 是左值(能取地址)、或者用括号括起来的标识符，那么变量的类型是 expression 的引用

```cpp
int a = 1;
// int &
decltype(++a) b = a;
// int &
decltype((a)) c = a;
```

### 4. 如果上面的条件都不满足，则变量的类型与 expression 的类型相同

```cpp
// int
decltype(1+1) a;
```

## 推导函数返回值

```cpp
// -> decltype(a + b)可以省略
template<typename T1, typename T2>
auto func(T1 a, T2 b) -> decltype(a + b) {
    return a + b;
}

int main(int argc, char *argv[]) {
    auto r = func(0.1, 2);
    std::cout << r << std::endl;

    return 0;
}
```
