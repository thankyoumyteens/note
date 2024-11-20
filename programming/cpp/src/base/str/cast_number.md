# 数值类型转换

## 数值转字符串

```cpp
int num = 10;
std::string str = std::to_string(num);
```

- `string to_string(int __val);`
- `string to_string(unsigned __val);`
- `string to_string(long __val);`
- `string to_string(unsigned long __val);`
- `string to_string(long long __val);`
- `string to_string(unsigned long long __val);`
- `string to_string(float __val);`
- `string to_string(double __val);`
- `string to_string(long double __val);`

## 字符串转数值

```cpp
std::string str = "3.14";
double num = std::stod(str);
```

- `int stoi(const string& __str, size_t* __idx = nullptr, int __base = 10);`
- `long stol(const string& __str, size_t* __idx = nullptr, int __base = 10);`
- `unsigned long stoul(const string& __str, size_t* __idx = nullptr, int __base = 10);`
- `long long stoll(const string& __str, size_t* __idx = nullptr, int __base = 10);`
- `unsigned long long stoull(const string& __str, size_t* __idx = nullptr, int __base = 10);`
- `float stof(const string& __str, size_t* __idx = nullptr);`
- `double stod(const string& __str, size_t* __idx = nullptr);`
- `long double stold(const string& __str, size_t* __idx = nullptr);`
