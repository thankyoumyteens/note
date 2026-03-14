# 搭配一个简单的前端页面

现代前端的标准做法是：利用 fetch API 结合 ReadableStream 来手动解析 SSE 数据流。

你可以新建一个文件 index.html，把下面的代码复制进去：

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>华尔街交易员终端</title>
    <style>
      body {
        font-family: "Courier New", Courier, monospace;
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 20px;
      }
      #chat-box {
        height: 400px;
        overflow-y: auto;
        border: 1px solid #444;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #252526;
      }
      .message {
        margin-bottom: 15px;
        line-height: 1.5;
      }
      .user {
        color: #569cd6;
      } /* 蓝色代表用户 */
      .assistant {
        color: #ce9178;
      } /* 橙色代表 AI */
      input[type="text"] {
        width: 70%;
        padding: 10px;
        background: #3c3c3c;
        border: 1px solid #555;
        color: white;
      }
      button {
        padding: 10px 20px;
        background: #007acc;
        color: white;
        border: none;
        cursor: pointer;
      }
      button:disabled {
        background: #555;
        cursor: not-allowed;
      }
    </style>
  </head>
  <body>
    <h2>📈 华尔街交易员终端 (FastAPI SSE 连线)</h2>

    <div id="chat-box"></div>

    <div style="display: flex; gap: 10px;">
      <input
        type="text"
        id="user-input"
        placeholder="问问他目前的指数估值，或者 ROE 怎么看..."
        onkeypress="handleEnter(event)"
      />
      <button id="send-btn" onclick="sendMessage()">发送 (Send)</button>
    </div>

    <script>
      // 模拟一个唯一的用户会话 ID
      const SESSION_ID = "user_" + Math.floor(Math.random() * 10000);
      const chatBox = document.getElementById("chat-box");
      const inputField = document.getElementById("user-input");
      const sendBtn = document.getElementById("send-btn");

      // 回车键发送
      function handleEnter(e) {
        if (e.key === "Enter") sendMessage();
      }

      async function sendMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        // 1. UI 状态更新：把用户的话显示到屏幕上，清空输入框，禁用按钮
        appendMessage("user", "你", text);
        inputField.value = "";
        sendBtn.disabled = true;

        // 提前在界面上创建一个用来容纳 AI 回答的空容器
        const aiMessageDiv = appendMessage("assistant", "华尔街老油条", "");

        try {
          // 2. 发起 Fetch POST 请求
          const response = await fetch("http://127.0.0.1:8000/chat/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: SESSION_ID, message: text }),
          });

          if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

          // 3. 核心获取流式读取器 (Reader)
          const reader = response.body.getReader();
          // 浏览器收到的是二进制的 Uint8Array，需要用 TextDecoder 解码成字符串
          const decoder = new TextDecoder("utf-8");

          let done = false;

          // 4. 循环读取数据流
          while (!done) {
            const { value, done: readerDone } = await reader.read();
            done = readerDone;

            if (value) {
              // 解码这一块的二进制数据
              const chunkStr = decoder.decode(value, { stream: true });

              // 【关键解析逻辑】：
              // chunkStr 可能包含多个 "data: {...}\n\n"（如果网络拥挤，数据会粘包）
              // 我们需要按换行符拆分，然后逐个处理
              const lines = chunkStr.split("\n");

              for (const line of lines) {
                if (line.startsWith("data: ")) {
                  const dataStr = line.replace("data: ", "").trim();

                  // 处理结束标志
                  if (dataStr === "[DONE]") {
                    break;
                  }

                  // 解析 JSON 并把字追加到界面上
                  try {
                    const parsed = JSON.parse(dataStr);
                    if (parsed.content) {
                      aiMessageDiv.innerHTML += parsed.content;
                      // 自动滚动到底部
                      chatBox.scrollTop = chatBox.scrollHeight;
                    } else if (parsed.error) {
                      aiMessageDiv.innerHTML += `<br><span style="color:red;">[${parsed.error}]</span>`;
                    }
                  } catch (e) {
                    // 忽略不完整的 JSON 碎片导致的解析错误
                    console.warn("JSON Parse Error on chunk:", dataStr);
                  }
                }
              }
            }
          }
        } catch (error) {
          console.error("请求失败:", error);
          appendMessage(
            "assistant",
            "系统",
            `<span style="color:red;">网络连接异常，请检查后端是否跨域或启动。</span>`,
          );
        } finally {
          // 请求结束，恢复按钮状态
          sendBtn.disabled = false;
          inputField.focus();
        }
      }

      // 辅助函数：向聊天框添加一条消息节点
      function appendMessage(role, name, content) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${role}`;
        msgDiv.innerHTML = `<strong>${name}: </strong><span class="content">${content}</span>`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        // 返回文本内容的 span 节点，方便后续流式追加
        return msgDiv.querySelector(".content");
      }
    </script>
  </body>
</html>
```

## 处理跨域 (CORS)

修改 main.py：

```py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 开发环境下允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 核心原理

1. `response.body.getReader()`：这赋予了我们精细控制网络底层数据流的能力。我们不再需要死等服务器把所有东西都打包好发过来。
2. `TextDecoder`：网络传输的都是 Uint8Array 字节流，`TextDecoder({ stream: true })` 是个神器，它知道如何处理被网络截断的半个汉字（因为 UTF-8 中一个汉字占 3 个字节，如果这一帧刚好只收到了 1 个字节，它会先缓存着，等下一帧拼齐了再输出，防止乱码）。
3. 粘包处理 (`split('\n')`)：由于 TCP 协议的特性，如果后端输出太快，前端读的时候，一个 chunk 里可能包含了多条 `data: {"content": "..."}\n\n`。我们必须按行拆分，否则 JSON.parse 会直接报错崩溃。

Fetch API 就是现代浏览器自带的、原生的 HTTP 客户端。以前前端老旧的 XMLHttpRequest（XHR）就像是 Java 里古老且难用的 HttpURLConnection；而现在的 Fetch API，就完美等价于 Java 11 之后官方自带的、支持异步的 java.net.http.HttpClient。

之所以我们在刚才的大模型流式输出场景中必须用它，是因为它具备以下几个核心特性：

1. 天生基于 Promise (完全拥抱异步)。以前的老 Ajax 写法（XHR）充满了回调函数（Callback），代码嵌套极深，人称“回调地狱”。而 Fetch API 天生返回 Promise 对象，这意味着你可以极其优雅地配合 async/await 语法，用写同步代码的思维去写异步逻辑，完全不会阻塞页面的渲染。
2. 核心大招：支持底层的流式读取 (Streams API)。这是 Fetch 对比其他封装库（比如前端极其常用的 Axios）在处理大模型场景时的绝对优势。
   - 普通请求（接水桶）： 传统的 HTTP 客户端（包括 Axios 的默认行为）是把整个响应体当成一个完整的字符串或 JSON。如果后端返回 10MB 的数据，它会死等这 10MB 全部下载完，才把结果交给你。
   - Fetch 流式请求（接水管）： 通过我们刚才用到的 `response.body.getReader()`，Fetch 允许你在数据还在网络传输途中、只收到一部分字节的时候，就立刻开始处理！这正是大模型打字机效果的底层灵魂——哪怕 AI 只吐出了半句话，我们也能立刻拿到并渲染在屏幕上。
3. 语法极简，没有历史包袱。它把 HTTP 请求的配置（Method、Headers、Body）封装得非常符合直觉。
