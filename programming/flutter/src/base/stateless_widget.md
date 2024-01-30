# 无状态组件

```dart
import 'package:flutter/material.dart';

/// 程序入口
void main() {
  runApp(const MyApp());
}

/// StatelessWidget: 无状态组件, 渲染快
class MyApp extends StatelessWidget {
  /// 构造方法
  const MyApp({super.key});

  /// 继承StatelessWidget需要重写build方法
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      // 主页面
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    // Scaffold: 内置控件
    return Scaffold(
        // appBar: 标题栏
        appBar: AppBar(
          title: const Text("标题"),
        ),
        // body: 控件内容
        // Center: 水平垂直居中
        body: const Center(
            child: Text('Hello World')
        )
    );
  }
}
```
