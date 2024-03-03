# 等待异步操作完成

在发送异步请求前展示 loading 组件，在异步请求完成后隐藏 loading 组件。

## loading

```dart
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class Loading extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: const Color.fromRGBO(22, 25, 35, 1),
      child: const Center(
        child: CircularProgressIndicator(
          color: Colors.white,
        ),
      ),
    );
  }
}
```

## 等待异步操作完成

```dart
class MyState extends State<BookWrapper> {
  MyState();
  // 表示异步操作是否完成
  bool loadComplete = false;
  // 异步获取的数据
  List<Map> currentUrlList = [];

  // 异步获取数据
  Future<List<Map>> getAllUrl() async {
    Database database = await openDatabase("demo.db");
    List<Map> list = await database.rawQuery('select * from current_url');
    return list;
  }

  @override
  void initState() {
    super.initState();

    // 异步获取数据
    getAllUrl().then((urlList) {
      currentUrlList = urlList;
      loadComplete = true;
      setState(() {});
    });
  }

  @override
  Widget build(BuildContext context) {
    WebViewController controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted);

    if (loadComplete) {
      // 异步数据获取完成
      String url = currentUrlList[0]["cur_url"];
      // 恢复上次访问的页面
      controller.loadRequest(Uri.parse(url));
    } else {
      // 异步数据还没获取到
      controller.loadRequest(Uri.parse("index.html"));
    }

    return Scaffold(
      // 异步请求结束前展示loading, 异步请求完成后隐藏loading
      body: loadComplete ? WebViewWidget(controller: controller) : Loading(),
    );
  }
}
```
