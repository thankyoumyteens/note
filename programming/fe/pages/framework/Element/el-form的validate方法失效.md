# el-form的validate方法失效

```js
// 错误代码
const checkMaxScore = (rule, value, callback) => {
  if (value === null || value === undefined) {
    callback(new Error("最高得分不允许为空!"));
  }
  if (value < this.edit.data.minScore) {
    callback(new Error("最高得分不得低于最低得分!"));
  }
};
```

原因：el-form组件使用自定义校验规则时，必须保证自定义校验规则的每个分支都调用了callback方法，否则会导致el-form组件的validate方法无法进入回调函数。

```js
// 正确代码
const checkMaxScore = (rule, value, callback) => {
  if (value === null || value === undefined) {
    callback(new Error("最高得分不允许为空!"));
  }
  if (value < this.edit.data.minScore) {
    callback(new Error("最高得分不得低于最低得分!"));
  }
  // 注意： 自定义校验规则必须保证每个分支都调用了callback方法
  callback();
};
```
