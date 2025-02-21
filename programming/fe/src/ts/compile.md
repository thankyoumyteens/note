# 基本使用

### 1. 安装 ts

```sh
npm install typescript -g
```

### 2. 初始化项目目录

```sh
mkdir ts-demo
cd ts-demo
tsc --init
```

### 3. 创建 demo.ts

```ts
let student = {
  name: "John",
  age: 25,
};

console.log(student.name);
```

### 4. 监听目录变化, 并自动把 ts 文件编译成 js 文件

```sh
tsc --watch
```
