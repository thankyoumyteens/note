# 路由

路由用来实现页面之间的跳转。

lib 目录下新建 data.dart 文件:

```dart
import 'package:flutter/material.dart';

class MyDataPage extends StatelessWidget {
  const MyDataPage({super.key});

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: Text("List Page"),
      ),
      body: Center(
          child: Text("data page")
      ),
    );
  }

}
```

在 main.dart 中导入 data.dart: 

```dart
import 'package:flutter/material.dart';
// 导入data.dart
import 'data.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      // 主页面
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
                    // 跳转
                    Navigator.push(context, MaterialPageRoute(
                        builder: (context) {
                          // 跳转到MyDataPage
                          return  MyDataPage();
                        }
                      )
                    );
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

## 根据路由名称跳转

修改 main.dart:

```dart
import 'package:flutter/material.dart';
// 导入data.dart
import 'data.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // 这里不能使用const
    return MaterialApp(
      // 定义路由名称
      routes: {
        "data": (context) => MyDataPage()
      },
      // 主页面
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
                    // 根据路由名称跳转
                    Navigator.pushNamed(context, "data");
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
