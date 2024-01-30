# 基本用法

```dart
import 'package:flutter/material.dart';

/// 程序入库
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

## 变更状态

```dart
import 'package:flutter/material.dart';

/// 程序入库
void main() {
  runApp(const MyApp());
}

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

/// StatefulWidget: 有状态组件, 渲染慢
class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  /// 继承StatefulWidget需要重写createState方法
  @override
  State<StatefulWidget> createState() {
    return MyState();
  }
}

/// State: 状态组件
class MyState extends State<MyHomePage> {

  var helloWorld = "Hello World";

  /// 继承State需要重写build方法
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
        body: Center(
            child: Column(
              children: [
                Text(helloWorld),
                // 按钮
                TextButton(
                  // 点击事件
                  onPressed: () {
                    // 需要在setState中修改字段
                    setState(() {
                      helloWorld = "Hello World !!!";
                    });
                  },
                  child: const Text("按钮"),
                )
              ],
            )
        )
    );
  }

}
```
