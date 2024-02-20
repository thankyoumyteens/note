# clearValidate 某一个表单项

```js
// 方式一
this.$refs["myForm"].clearValidate("inputProp");
// 方式二
this.$refs["myForm"].fields.map((i) => {
  if (i.prop === "inputProp") {
    i.clearValidate();
  }
});
```
