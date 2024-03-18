# 监听 url 变化

NavigationDelegate 用于监听页面跳转相关的事件, 其中包括 url 变化的事件。

```dart
WebViewController controller = WebViewController()
  ..setJavaScriptMode(JavaScriptMode.unrestricted)
  ..loadRequest(Uri.parse(uri))
  ..setNavigationDelegate(NavigationDelegate(
    onUrlChange: (param) {
      String newUrl = param.url ?? '';
      print(newUrl);
    },
  ));
```
