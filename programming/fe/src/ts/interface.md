# 接口

```ts
interface Computer {
  cpu: string;
  memory: string;
  storage: string;

  getSpecs(): string;
}

class Laptop implements Computer {
  cpu: string;
  memory: string;
  storage: string;

  constructor(cpu: string, memory: string, storage: string) {
    this.cpu = cpu;
    this.memory = memory;
    this.storage = storage;
  }

  getSpecs(): string {
    return `CPU: ${this.cpu}, Memory: ${this.memory}, Storage: ${this.storage}`;
  }
}
```

## 用对象直接实现接口

```ts
interface Computer {
  cpu: string;
  memory: string;
  storage: string;

  getSpecs(): string;
}

const computer: Computer = {
  cpu: "i7",
  memory: "16GB",
  storage: "512GB",

  getSpecs() {
    return `${this.cpu} ${this.memory} ${this.storage}`;
  },
};
```

## 自动合并

ts 会自动把重名的接口合并到一起

```ts
interface Computer {
  cpu: string;
  memory: string;
  storage: string;
}

interface Computer {
  getSpecs(): string;
}

const computer: Computer = {
  cpu: "i7",
  memory: "16GB",
  storage: "512GB",

  getSpecs() {
    return `${this.cpu} ${this.memory} ${this.storage}`;
  },
};
```
