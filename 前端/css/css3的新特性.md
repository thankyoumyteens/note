# 过渡

> transition： CSS属性, 花费时间, 效果曲线(默认ease), 延迟时间(默认0)

例:
```
/*宽度从原始值到制定值的一个过渡, 运动曲线ease,运动时间0.5秒, 0.2秒后执行过渡*/
transition：width .5s ease .2s
```

# 动画

> animation：动画名称, 一个周期花费时间, 运动曲线（默认ease）, 动画延迟（默认0）, 播放次数（默认1）, 是否反向播放动画（默认normal）, 是否暂停动画（默认running）

例:
```
@keyframes logo1 {
    0%{
        transform:rotate(180deg);
        opacity: 0;
    }
    100%{
        transform:rotate(0deg);
        opacity: 1;
    }
}
animation: logo1 1s ease-in 2s;
```

# 形状转换

例:
```
transform:rotate(30deg);
transform:translateX(30px);
```

# 阴影

> box-shadow: 水平阴影的位置 垂直阴影的位置 模糊距离 阴影的大小 阴影的颜色 阴影开始方向（默认是从里往外, 设置inset就是从外往里）

例:
```
box-shadow: 10px 10px 5px #888888;
```

# 边框圆角

> border-radius: n1,n2,n3,n4; n1-n4四个值的顺序是：左上角, 右上角, 右下角, 左下角。

例:
```
border-radius::50%;
```

# 文字阴影

> text-shadow:水平阴影, 垂直阴影, 模糊的距离, 以及阴影的颜色

例:
```
text-shadow: 0 0 10px #f00;
```

# 颜色

> rgba（rgb为颜色值, a为透明度）

例:
```
color: rgba(255,0,0,0.1);
```
