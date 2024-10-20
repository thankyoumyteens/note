# 编译

1. 安装

```sh
npm install typescript -g
```

2. 初始化目录

```sh
mkdir ts-demo
cd ts-demo
tsc --init
```

3. 创建 demo.ts

```ts
let student = {
  name: "John",
  age: 25,
};

console.log(student.name);
```

4. 监听目录变化, 并自动编译

```sh
tsc --watch
```
