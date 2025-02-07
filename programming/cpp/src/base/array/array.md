# 数组

```cpp
// 声明数组, 未初始化
int arr1[3];

// 声明数组, 初始化为0
int arr2[3] = {};

// 声明数组, 初始化为1, 2, 3
// 编译器可自动推断出数组的大小
int arr3[] = {1, 2, 3};
```

## 下标

`数组名[下标]` 和 `*(数组名 + 下标)` 是完全等价的:

```cpp
std::cout << arr[1];
std::cout << *(arr + 1);
```

## 计算数组的长度

```cpp
int arr[] = {1, 2, 3};

unsigned size = sizeof(arr) / sizeof(arr[0]);
```

## 清空数组

用 `memset` 函数可以把数组中全部的元素清零。(只适用于 C++基本数据类型)

函数原型:

```cpp
void *memset(void *s, int c, size_t n);
```

## 复制数组

用 `memcpy` 函数可以把数组中全部的元素复制到另一个相同大小的数组。(只适用于 C++基本数据类型)

函数原型:

```cpp
void *memcpy(void *dest, const void *src, size_t n);
```
