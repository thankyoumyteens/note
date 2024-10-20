# 对象

```ts
let student: {
  name: string;
  age?: number; // ? 表示可选的属性
};

student = {
  name: "Tom",
  // 可选的属性可以不赋值
};
```

## 索引签名

```ts
let student: {
  name?: string;
  age?: number;
  // 允许添加任意属性
  [propName: string]: any;
};

student = {};

student.address = "New York";
```
