# 禁止手机浏览器缩放

Vue3 项目在 iPhone 上输入时页面自动放大，是由于 Safari 浏览器的默认行为：当输入框（input/textarea）获得焦点时，若页面字体小于 16px，Safari 会自动放大页面以提高可读性。

## 优化视口（viewport）配置

```html
<!-- index.html 中 -->
<meta
  name="viewport"
  content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
/>
```

- `width=device-width` 确保页面宽度与设备宽度一致
- `initial-scale=1.0` 初始缩放比例为 1
- `maximum-scale=1.0` 和 `user-scalable=no` 禁止用户手动缩放（可选，根据需求决定是否开启）
