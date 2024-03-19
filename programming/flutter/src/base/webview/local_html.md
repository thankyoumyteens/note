# 显示本地 html

项目根目录新建 assets 文件夹, 文件目录结构:

```
project
└─ assets
  └─ demo1
    └─ about
        └─ about.html
    └─ css
        └─ main.css
    └─ img
        └─ a.png
    └─ index.html
```

## html 文件内容

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Title</title>
    <link rel="stylesheet" href="css/main.css" />
  </head>
  <body>
    <h1>Demo1</h1>
    <a href="about/about.html">about</a>
    <br />
    <img src="img/a.png" alt="a" />
  </body>
</html>

<!-- about.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Title</title>
    <link rel="stylesheet" href="../css/main.css" />
  </head>
  <body>
    <h1>About</h1>
    <a href="../index.html">about</a>
    <br />
    <img src="../img/a.png" alt="a" />
  </body>
</html>
```

## 修改 pubspec.yaml

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  jaguar: ^3.1.3
  jaguar_flutter_asset: ^3.0.0
  webview_flutter: ^4.7.0

flutter:
  assets:
    - assets/demo1/index.html
    - assets/demo1/about/about.html
    - assets/demo1/img/a.png
    - assets/demo1/css/main.css
```

## main.dart

```dart
import 'package:flutter/material.dart';
import 'package:jaguar/jaguar.dart';
import 'package:jaguar_flutter_asset/jaguar_flutter_asset.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() async {
  // 启动本地服务器
  final server = Jaguar(port: 8617);
  server.addRoute(serveFlutterAssets());
  await server.serve(logRequests: true);

  server.log.onRecord.listen((r) => print(r));

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Demo',
      home: WebViewLocal(),
    );
  }
}

class WebViewLocal extends StatefulWidget {
  const WebViewLocal({super.key});

  @override
  State<StatefulWidget> createState() {
    return WebViewLocalState();
  }
}

class WebViewLocalState extends State<WebViewLocal> {
  @override
  Widget build(BuildContext context) {
    WebViewController controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse('http://127.0.0.1:8617/demo1/index.html'));
    return Scaffold(
      appBar: AppBar(
        title: const Text('标题'),
      ),
      body: WebViewWidget(controller: controller),
    );
  }
}
```
