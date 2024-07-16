# 圆环图

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
        series: [
          {
            type: "pie",
            // 圆环图
            // [内环半径, 外环半径]
            radius: ["30%", "50%"],
            // [圆心x, 圆心y]
            center: ["50%", "50%"],
            avoidLabelOverlap: true,
            data: [
              {
                name: "销量",
                value: 9,
              },
              {
                name: "库存",
                value: 1,
              },
            ],
          },
        ],
      };

      myChart.setOption(option);
    </script>
  </body>
</html>
```
