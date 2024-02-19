# y 轴禁止显示小数

y 轴出现了小数，实际值都是整数:

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
            data: [1, 2, 1, 3, 1, 2],
          },
          {
            name: "库存",
            type: "bar",
            data: [2, 2, 1, 1, 1, 3],
          },
        ],
      };

      myChart.setOption(option);
    </script>
  </body>
</html>
```

![](../img/echarts-3.png)

给 yAxis 增加`minInterval: 1`即可去掉小数。

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
        yAxis: {
          // 去掉小数
          minInterval: 1,
        },
        series: [
          {
            name: "销量",
            type: "bar",
            data: [1, 2, 1, 3, 1, 2],
          },
          {
            name: "库存",
            type: "bar",
            data: [2, 2, 1, 1, 1, 3],
          },
        ],
      };

      myChart.setOption(option);
    </script>
  </body>
</html>
```

![](../img/echarts-4.png)
