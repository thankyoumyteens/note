# 曲线下方区域颜色渐变

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ECharts Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
  </head>
  <body>
    <div id="main" style="width: 600px; height: 400px"></div>
    <script type="text/javascript">
      var myChart = echarts.init(document.getElementById("main"));

      var option = {
        xAxis: {
          data: ["A", "B", "C", "D", "E"],
        },
        yAxis: {},
        series: [
          {
            data: [10, 22, 28, 23, 19],
            type: "line",
            smooth: true,
            itemStyle: {
              normal: {
                // 背景渐变
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  {
                    offset: 0,
                    color: "#d7f4f8", // 0% 处的颜色
                  },
                  {
                    offset: 0.5,
                    color: "#eefcfd", // 50% 处的颜色
                  },
                  {
                    offset: 1,
                    color: "#fff", // 100% 处的颜色
                  },
                ]),
                // 线条样式
                lineStyle: {
                  width: 3,
                  type: "solid",
                  color: "#4fd6d2",
                },
              },
              // 鼠标hover时的线条样式
              emphasis: {
                color: "#4fd6d2",
                lineStyle: {
                  width: 2,
                  type: "dotted",
                  color: "#4fd6d2",
                },
              },
            },
            // 必须加上这个属性, 否则颜色渐变不生效
            areaStyle: { normal: {} },
          },
        ],
      };

      myChart.setOption(option);
    </script>
  </body>
</html>
```

![](../img/echarts-10.png)

## vue 中使用

main.js

```js
// 引入echarts
import * as echarts from "echarts";
Vue.prototype.$echarts = echarts;
```

使用

```js
color: new this.$echarts.graphic.LinearGradient();
// ...
```
