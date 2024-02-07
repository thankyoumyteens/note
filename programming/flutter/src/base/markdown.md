# 显示 markdown

项目根目录新建 assets 文件夹, md 文件目录结构:

```
project
├─ assets
  └─ img
    └─ img1.png
  └─ md
    └─ demo1.md
    └─ demo2.md
```

demo1.md 内容:

```md
# demo1

<!-- 路径前需要加resource: -->

![img1](resource:assets/img/img1.png)

[跳转到 demo2](assets/md/demo2.md)
```

demo2.md 内容:

```md
# demo2

![img1](resource:assets/img/img1.png)
```

编辑 pubspec.yaml 文件:

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_markdown: ^0.6.0

flutter:
  assets:
    - assets/md/demo1.md
    - assets/md/demo2.md
    - assets/img/img1.png
```

编辑 main.dart 文件:

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
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
  // 当前md文件路径
  var filePath = "assets/md/demo1.md";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 标题
      appBar: AppBar(
        title: Text(filePath),
      ),
      body: Center(
        child: FutureBuilder(
          // md文件路径
          future: rootBundle.loadString(filePath),
          builder: (BuildContext context, AsyncSnapshot snapshot) {
            if (snapshot.hasData) {
              return Markdown(
                data: snapshot.data,
                // 处理md文件中的链接点击事件
                onTapLink: (text, url, title) {
                  // 跳转到其它文件的路径
                  filePath = url.toString();
                  setState(() {});
                },
              );
            } else {
              return const Center(
                child: Text("加载中..."),
              );
            }
          },
        ),
      ),
    );
  }
}
```
