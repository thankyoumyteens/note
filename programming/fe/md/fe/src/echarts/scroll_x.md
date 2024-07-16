# x 轴滚动条

通过配置 dataZoom 实现滚动。

dataZoom 的属性说明:

- zoomLock: 让滚动只会平移数据，而不会缩放数据，
- start 和 end 的取值范围是 0 ~ 100，表示 0% ~ 100% 利用百分比的形式来决定可视化窗口的大小是数据总量的大小的百分之多少。比方说设定
  ```js
  start: 0,
  end: 40,
  ```
  这样就会展示前百分之 40 的数据
- startValue 和 endValue 的取值范围就是数据的条数，表示开始的数据位置和结束的数据位置。比方说设定
  ```js
  startValue: 0,
  endValue: 2,
  ```
  这样就会展示前三条数据

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
        dataZoom: [
          {
            type: "slider", // 滚动条
            show: true, // 显示滚动条
            // 初始展示x坐标为0-7的数据
            startValue: 0,
            endValue: 7,
            height: 7, // 滚动条高度
            bottom: 10, // 距离echarts下边框的距离
            showDataShadow: false, // 是否显示滚动条阴影
            fillerColor: "#00000033", // 滚动条的颜色
            // borderColor: "transparent", // 滚动条滑轨的边框颜色
            zoomLock: true, // 禁止缩放
            brushSelect: false, // 隐藏缩放手柄
            handleSize: 0, // 隐藏滚动条两边的手柄
            showDetail: false, // 拖拽时隐藏滚动条两侧的文字
          },
        ],
        xAxis: {
          data: [
            "x1",
            "x2",
            "x3",
            "x4",
            "x5",
            "x6",
            "x7",
            "x8",
            "x9",
            "x10",
            "x11",
            "x12",
            "x13",
            "x14",
            "x15",
            "x16",
            "x17",
            "x18",
            "x19",
            "x20",
            "x21",
            "x22",
            "x23",
            "x24",
            "x25",
            "x26",
            "x27",
            "x28",
            "x29",
            "x30",
            "x31",
            "x32",
            "x33",
            "x34",
            "x35",
            "x36",
            "x37",
            "x38",
            "x39",
            "x40",
            "x41",
            "x42",
            "x43",
            "x44",
            "x45",
            "x46",
            "x47",
            "x48",
            "x49",
            "x50",
            "x51",
            "x52",
            "x53",
            "x54",
            "x55",
            "x56",
            "x57",
            "x58",
            "x59",
            "x60",
            "x61",
            "x62",
            "x63",
            "x64",
            "x65",
            "x66",
            "x67",
            "x68",
            "x69",
            "x70",
            "x71",
            "x72",
            "x73",
            "x74",
            "x75",
            "x76",
            "x77",
            "x78",
            "x79",
            "x80",
            "x81",
            "x82",
            "x83",
            "x84",
            "x85",
            "x86",
            "x87",
            "x88",
            "x89",
            "x90",
            "x91",
            "x92",
            "x93",
            "x94",
            "x95",
            "x96",
            "x97",
            "x98",
            "x99",
            "x100",
          ],
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
