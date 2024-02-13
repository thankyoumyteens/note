# SizedBox

主要用来控制子组件的大小, 能强制子组件具有特定宽度或高度, 使子组件设置的宽高失效。

```dart
SizedBox(
  width: 100,
  height: 100,
  child: Container(
    // 子组件的宽高无效
    width: 500,
    height: 500,
    color: Colors.orange,
  ),
),
```
