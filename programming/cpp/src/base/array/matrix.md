# 二维数组

声明二维数组:

```cpp
// 10行20列
int arr[10][20];
```

## 行指针(数组指针)

```cpp
int arr[10][20];

// 必须指明列的长度
// p指向arr第0行
int (*p)[20] = arr;

for (int col = 0; col < 20; ++col) {
    std::cout << (*p)[col] << std::endl;
}
```

## 把二维数组作为参数传递

```cpp
// 必须指明列的长度
void print(int (*arr)[20], int length);
```
