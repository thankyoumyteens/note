# 动态绑定 img 的 src 属性

错误代码：

```html
<img :src="'@/assets/image/1.png'" alt="" />
```

正确代码：

```html
<img :src="require('@/assets/image/1.png')" alt="" />
```
