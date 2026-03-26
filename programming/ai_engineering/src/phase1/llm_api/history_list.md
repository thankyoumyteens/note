# 支持多轮对话

大模型 API 最反直觉的一点就是：它是个“鱼的记忆”，完全没有状态（Stateless）。 你前面跟它聊了三百回合，只要下一次 HTTP 请求没带上之前的聊天记录，它就会把你当成陌生人。

为了让它有记忆，我们必须在代码里维护一个“对话列表”，每次用户提问时，把新的问题塞进列表，每次 AI 回答完，把 AI 的完整回答也塞进列表，然后再把整个列表打包发给服务器。

```py
import os

import env_setup
from openai import OpenAI

SILICON_FLOW_API_KEY = os.environ.get("API_KEY")

# 初始化客户端
client = OpenAI(
    api_key=SILICON_FLOW_API_KEY,
    base_url="https://api.siliconflow.cn/v1"
)


def start_chat():
    # 1. 初始化对话历史 (History List)
    # 这就像 Java 里的 List<Map<String, String>>
    messages = [
        {
            "role": "system",
            "content": "你是一个在华尔街摸爬滚打多年的顶尖交易员。你极度看重基本面数据（如 ROE、P/E 估值、盈利收益率），说话一针见血、极其毒舌，带着对散户的轻视。你的回答要短平快。"
        }
    ]

    print("交易大厅连线成功。输入 'quit' 或 'exit' 退出。\n")
    print("-" * 50)

    # 2. 开启多轮对话的主循环
    while True:
        # 获取用户输入
        user_input = input("\n你: ")
        if user_input.lower() in ['quit', 'exit']:
            print("挂断电话。")
            break

        # 去除首尾的空格
        if not user_input.strip():
            continue

        # 3. 将【用户的提问】追加到历史记录中
        # Python 的 list.append() 类似于 Java 的 ArrayList.add()
        messages.append({"role": "user", "content": user_input})

        print("华尔街老油条: ", end="")

        try:
            # 4. 发送包含完整历史记录的请求
            response = client.chat.completions.create(
                model="Pro/moonshotai/Kimi-K2.5",
                messages=messages,
                temperature=0.8,
                stream=True
            )

            # 准备一个变量，用来拼接流式输出的完整回答
            full_assistant_reply = ""

            # 5. 处理流式输出并拼接
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    # 将每一块碎片收集起来
                    full_assistant_reply += content

            print()  # 换行

            # 6. 【最关键的一步】：将【AI的完整回答】追加到历史记录中
            # 只有这样，下一轮循环发请求时，AI 才知道自己刚才说过什么
            messages.append({"role": "assistant", "content": full_assistant_reply})

        except Exception as e:
            print(f"\n[网络波动，交易员爆粗口了: {e}]")
            # 如果请求失败，把刚才加进去的用户问题弹出来，避免破坏上下文结构
            messages.pop()


if __name__ == "__main__":
    start_chat()
```

运行上面的代码，你可以尝试这样对话：

1. 你： “除了博格公式，我看指数基金还要盯紧什么？”
2. AI： （会毒舌地给你讲 ROE 或者估值）
3. 你： “那你能具体解释一下你刚才提到的那个指标吗？”
   (这个时候，它能完美回答，因为它看到了 messages 列表里自己刚才说的话)

## 架构视角的底层逻辑

在这个脚本里，我们的 messages 是一个存在内存里的 Python 局部变量。对于单机跑跑脚本来说没问题。但是，如果你在思考真实的后端架构，这里其实埋着一个大坑。

如果你把这个服务部署到线上，用户的每一个 HTTP 请求可能被负载均衡分配到不同的节点。当前线程一旦结束，内存里的 messages 也就灰飞烟灭了。这就意味着，在分布式的生产环境中，我们绝不能把对话历史存在应用的内存里。

真实的生产级解法是：引入外部缓存机制。

每一次用户发起请求时，携带一个唯一的 Session ID。后端服务拿到 ID 后，去高速缓存（比如 Redis）里把对应的 messages 历史（JSON 格式）拉出来，反序列化成列表，把新问题 append 进去，调用大模型 API。拿到完整回答后，再次 append，然后把最新的大列表序列化写回 Redis，并设置一个过期时间（TTL）。这种模式下，不管请求打到哪台服务器，状态都是一致的。
