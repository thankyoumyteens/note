# 类型断言

在 TypeScript 中，类型断言是一种告诉编译器“相信我，我知道自己在做什么”的方式，它允许你手动指定一个值的类型。

## 尖括号语法

在早期的 TypeScript 代码中，使用尖括号语法来进行类型断言。其语法格式为 `<类型>值`。

```typescript
let someValue: any = "这是一个字符串";
let strLength: number = (<string>someValue).length;
console.log(strLength);
```

## `as` 语法

`as` 语法是现代 TypeScript 中推荐的类型断言方式，它在 JSX 环境中也能正常使用，其语法格式为 `值 as 类型`。

```typescript
let someValue: any = "这是一个字符串";
let strLength: number = (someValue as string).length;
console.log(strLength);
```

## 非空断言

非空断言使用 `!` 后缀，用于告诉编译器某个变量一定不是 `null` 或 `undefined`。

```typescript
function printLength(str?: string) {
  // 使用非空断言
  let length: number = str!.length;
  console.log(length);
}
printLength("hello");
```
