# 集成 echarts

1. 安装依赖

```sh
npm install echarts --save
```

2. 在 main.js 中全局引入

```js
import echarts from "echarts";
Vue.prototype.$echarts = echarts;
```

3. 创建 echarts 容器

```html
<div id="main" style="width: 600px; height: 400px"></div>
```

4. 使用

```js
drawChart() {
    const e = document.getElementById("main");
    let myChart = this.$echarts.init(e);
    const option = {
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
    myChart.setOption(option);
},
```
