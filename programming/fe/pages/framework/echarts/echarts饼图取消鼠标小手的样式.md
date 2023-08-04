```js
series: [
    {
    ....
    type: 'pie',
    label: {
        normal: {
        show: true,
        position: 'center',
        ....
        fontSize: '12'
        }
    },
    labelLayout: {
        dy: this.title.indexOf('\n') > -1 ? 2 : 0
    },
    cursor: 'default' // 鼠标样式
    }
]
```

修改后发现只是鼠标移入圆环是默认样式了，但是中间的文字还是手指样式，所以决定复写css的样式，设置鼠标经过整个盒子的样式

```css
.pie-chart {
  div > div > canvas {
    cursor: default;
  }
}
```
