# 安装echarts

```
npm install echarts --save
```

# 在 main.js 中全局引入 echarts

```js
import echarts from "echarts";
Vue.prototype.$echarts = echarts;
```

# 创建echarts容器

```html
<div id="main" style="width: 600px; height: 400px"></div>
```

# 绘图

```js
drawChart() {
    // 基于准备好的dom，初始化echarts实例  这个和上面的main对应
    let myChart = this.$echarts.init(document.getElementById("main"));
    // 指定图表的配置项和数据
    let option = {
    title: {
        text: "ECharts 入门示例",
    },
    tooltip: {},
    legend: {
        data: ["销量"],
    },
    xAxis: {
        data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
    },
    yAxis: {},
    series: [
        {
        name: "销量",
        type: "bar",
        data: [5, 20, 36, 10, 10, 20],
        },
    ],
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
},
```
