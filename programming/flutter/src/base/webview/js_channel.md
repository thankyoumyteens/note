# flutter 和 js 通信

## js -> flutter

在 html 中添加:

```html
<script>
  // UrlLogger: addJavaScriptChannel中的第一个参数
  // postMessage: 给flutter发送消息
  UrlLogger.postMessage("404.html");
</script>
```

在 flutter 中添加:

```dart
WebViewController controller = WebViewController()
  ..setJavaScriptMode(JavaScriptMode.unrestricted)
  ..loadRequest(Uri.parse(uri))
  ..addJavaScriptChannel("UrlLogger", onMessageReceived: (message) {
    // 接收js中postMessage的消息
    // 打印: 404.html
    print(message.message);
  });
```
