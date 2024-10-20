# 类

```ts
class Student {
  // 不写默认是public
  private name: string;
  private age: number;

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  // 不写默认是public
  public getDetails() {
    return `Name: ${this.name}, Age: ${this.age}`;
  }
}

const student = new Student("John", 25);

console.log(student.getDetails());
```

简写:

```ts
class Student {
  constructor(private name: string, private age: number) {}

  public getDetails() {
    return `Name: ${this.name}, Age: ${this.age}`;
  }
}

const student = new Student("John", 25);

console.log(student.getDetails());
```

## 继承

```ts
class Computer {
  constructor() {}
}

class Laptop extends Computer {
  constructor() {
    super();
  }
}
```

## 只读字段

```ts
class Student {
  constructor(public readonly name: string) {}
}

const student = new Student("John");

// Error: Cannot assign to 'name' because it is a read-only property.
student.name = "Doe";
```

## 抽象类

```ts
abstract class Computer {
  abstract getCPU(): string;
}

class Laptop extends Computer {
  getCPU(): string {
    return "Intel Core i7";
  }
}

let laptop = new Laptop();
console.log(laptop.getCPU()); // Output: Intel Core i7
```
