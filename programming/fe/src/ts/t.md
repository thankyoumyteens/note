# 泛型

泛型函数:

```ts
function print<T>(a: T): void {
  console.log(a);
}

print<number>(1); // 1
```

泛型接口:

```ts
interface Demo<T> {
  data: T;
}

const demo: Demo<string> = {
  data: "hello world",
};
```

泛型类:

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
