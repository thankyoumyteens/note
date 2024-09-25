# 圆环图中间显示文字

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
        graphic: [
          {
            type: "group",
            // 注意它的父元素是整个画布, 而不是圆环
            // 所以它相对于整个画布居中, 而不是相对于圆环
            left: "center",
            top: "center",
            width: 100,
            height: 100,
            children: [
              {
                type: "circle",
                left: "center",
                top: "center",
                shape: {
                  r: 47,
                },
                style: {
                  fill: "#F0F0F0",
                  stroke: "#F0F0F0",
                },
              },
              {
                type: "text",
                left: "center",
                top: 30,
                style: {
                  text: "百分比",
                  textAlign: "center",
                  fill: "#999999",
                  fontSize: 16,
                },
              },
              {
                type: "text",
                left: "center",
                top: 55,
                style: {
                  text: "90%",
                  textAlign: "center",
                  fill: "#000",
                  fontSize: 16,
                },
              },
            ],
          },
        ],
        series: [
          {
            type: "pie",
            radius: ["30%", "50%"],
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

![](../img/echarts-7.png)
