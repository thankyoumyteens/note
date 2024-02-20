# clearValidate 失效

将 clearValidate 放入 nextTick 中:

```js
this.$nextTick(() => {
  this.$refs["myForm"].clearValidate();
});
```
