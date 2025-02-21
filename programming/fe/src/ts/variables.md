# 定义变量时指定类型

格式

```ts
let 变量名: 类型 = 初始值;
```

## 基本类型的变量

```ts
let a: string = "Hello World";
let b: number = 10;
let c: boolean = true;
```

## 对象类型的变量

```ts
let student: {
  name: string;
  age: number;
};

student = {
  name: "Tom",
  age: 10,
};
```

## 函数类型的变量

```ts
let add: (x: number, y: number) => number;

add = function (x, y) {
  return x + y;
};

let result = add(2, 3);
```

## 数组类型的变量

```ts
// 两种写法

let a: string[] = ["a", "b", "c"];
let b: Array<string> = ["a", "b", "c"];
```

## 元组类型的变量

```ts
let a: [string, number] = ["hello", 10];
```
