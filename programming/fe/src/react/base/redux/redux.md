# Redux

1. 安装依赖

```sh
npm install @reduxjs/toolkit react-redux
```

store 目录结构设计:

1. 通常集中状态管理的部分都会单独创建一个单独的 store 目录
2. 应用通常会有很多个子 store 模块，所以创建一个 modules 目录，在内部编写业务分类的子 store
3. store 中的入口文件 index.js 的作用是组合 modules 中所有的子模块，并导出 store
