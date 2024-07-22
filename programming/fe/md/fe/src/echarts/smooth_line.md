# 平滑曲线图

将折线图 series 的 smooth 属性设置为 true 即可。

```js
option = {
  xAxis: {
    data: ["A", "B", "C", "D", "E"],
  },
  yAxis: {},
  series: [
    {
      data: [10, 22, 28, 23, 19],
      type: "line",
      smooth: true, // 平滑曲线图
    },
  ],
};
```
