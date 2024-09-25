# 柱状图圆角

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
        title: {
          text: "ECharts 入门示例",
        },
        tooltip: {},
        legend: {
          data: ["销量", "库存"],
        },
        xAxis: {
          data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
        },
        yAxis: {},
        series: [
          {
            name: "销量",
            type: "bar",
            itemStyle: {
              // 柱形图圆角: 左上角, 右上角, 左下角, 右下角
              barBorderRadius: [20, 20, 0, 0],
            },
            data: [5, 20, 36, 10, 10, 20],
          },
          {
            name: "库存",
            type: "bar",
            data: [5, 25, 40, 20, 15, 20],
          },
        ],
      };

      myChart.setOption(option);
    </script>
  </body>
</html>
```

## 效果

![](../img/echarts-9.png)
