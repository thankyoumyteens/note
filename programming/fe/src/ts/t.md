# 泛型

## 函数的泛型

```ts
function print<T>(a: T): void {
  console.log(a);
}

print<number>(1); // 1
```

## 箭头函数的泛型

```ts
const print1 = <T>(a: T) => {
  console.log(a);
};

print1<number>(1); // 1
```

## 接口的泛型

```ts
interface Demo<T> {
  data: T;
}

const demo: Demo<string> = {
  data: "hello world",
};
```

## 类的泛型

```ts
class Demo<T> {
  private data: T;
  constructor(data: T) {
    this.data = data;
  }
  getData(): T {
    return this.data;
  }
}

const demo = new Demo<string>("Hello");
```
