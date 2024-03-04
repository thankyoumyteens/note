# Flex

Row 和 Column 都继承自 Flex。Flex 必须指定 direction 字段, Row 为 Axis.horizontal, Column 为 Axis.vertical。

```dart
@override
Widget build(BuildContext context) {
  return const Scaffold(
    body: Flex(
      // 相当于Row
      direction: Axis.horizontal,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text("test 1"),
        Text("test 2"),
      ],
    ),
  );
}
```

## Expanded

Expanded 只能作为 Flex 的子组件, 它可以按 flex 字段设置的比例占据 Flex 的空间。

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    body: SizedBox(
      height: 100,
      child: Flex(
        direction: Axis.horizontal,
        children: [
          Expanded(
            flex: 1,
            child: Container(color: Colors.blue),
          ),
          Expanded(
            flex: 2,
            child: Container(color: Colors.orange),
          ),
          Expanded(
            flex: 1,
            child: Container(color: Colors.blue),
          ),
        ],
      ),
    ),
  );
}
```

效果:

![](../img/flex_expand1.png)
