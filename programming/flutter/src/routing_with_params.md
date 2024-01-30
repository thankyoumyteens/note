# 路由传参

创建参数类 my-args.dart:

```dart
class MyArgs {
  String title;
  String message;

  MyArgs(this.title, this.message);
}
```

创建接收参数的页面 data.dart:

```dart
import 'package:flutter/material.dart';
import 'my-args.dart';

class MyDataPage extends StatelessWidget {
  const MyDataPage({super.key});

  @override
  Widget build(BuildContext context) {
    // 接收参数并转成MyArgs类型
    final MyArgs args = ModalRoute.of(context)!.settings.arguments as MyArgs;

    return Scaffold(
      appBar: AppBar(
        // 使用参数
        title: Text(args.title)
      ),
      body: Center(
          // 使用参数
          child: Text(args.message)
      ),
    );
  }

}
```

创建发送参数的页面 main.dart:

```dart
import 'package:flutter/material.dart';
import 'data.dart';
import 'my-args.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      routes: {
        "data": (context) => MyDataPage()
      },
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<StatefulWidget> createState() {
    return MyState();
  }
}

class MyState extends State<MyHomePage> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text("标题"),
        ),
        body: Center(
            child: Column(
              children: [
                TextButton(
                  // 点击事件
                  onPressed: () {
                    // 根据路由名称跳转并传参
                    Navigator.pushNamed(context, "data", arguments: MyArgs("标题1", "来自main"));
                  },
                  child: const Text("跳转"),
                )
              ],
            )
        )
    );
  }

}
```
