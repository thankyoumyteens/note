# 自动生成接口文档

FastAPI 会根据你的代码和 Pydantic 模型，自动生成符合 OpenAPI 标准的 API 文档。

保持你的服务器运行，在浏览器中访问：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

你会看到一个漂亮的 Swagger UI 界面。

1. 点开 POST /items/ 接口。
2. 点击右上角的 "Try it out"。
3. 在请求体框内输入 JSON 测试数据：
   ```json
   {
     "name": "机械键盘",
     "description": "青轴，带 RGB 背光",
     "price": 299.5,
     "tax": 10.5
   }
   ```
4. 点击 "Execute"。你不仅能看到请求成功，还能直接在界面上测试各种数据类型错误的拦截情况。
