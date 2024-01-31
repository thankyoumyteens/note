# 渐变

## 线性渐变

begin 和 end 表示渐变的方向。color 表示渐变的颜色。stops 表示渐变的进度, 取值为 0~1。

```dart
class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          decoration: const BoxDecoration(
            // 线性渐变
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Colors.blueAccent,
                Colors.blue,
                Colors.orange,
                Colors.redAccent,
                Colors.red,
              ],
              stops: [
                0,
                0.3,
                0.6,
                0.9,
                1,
              ],
            ),
          ),
          width: 200,
          height: 200,
        ),
      ),
    );
  }
}
```

![](../img/LinearGradient.png)
