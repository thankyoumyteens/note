# 自定义类型

```ts
type MyString = string;

let a: MyString = "Hello";
```

## 联合类型

```ts
// MyType 既可以是 string 类型，也可以是 number 类型
type MyType = string | number;

let a: MyType = "Hello";
let b: MyType = 10;
```

## 交叉类型

```ts
type Part1 = {
  name: string;
};

type Part2 = {
  age: number;
};

// All 中包含了 Part1 和 Part2 的所有属性
type All = Part1 & Part2;

const obj: All = {
  name: "John",
  age: 30,
};
```
