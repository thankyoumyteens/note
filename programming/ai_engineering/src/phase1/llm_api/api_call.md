# 原生 API 调用

### 1. 安装依赖

```sh
pip install openai
```

### 2. 代码

这段代码展示了如何使用 stream=True 实现打字机效果，并且我们把 system 角色设定成了你要求的“尖酸刻薄的华尔街交易员”。

```py
import os

# noinspection PyUnusedImports
import env_setup  # 它会自动执行里面的清理和加载逻辑

from openai import OpenAI

# 从环境变量里加载硅基流动的API Key
SILICON_FLOW_API_KEY = os.environ.get("API_KEY")

# 初始化 AI 客户端
client = OpenAI(
    api_key=SILICON_FLOW_API_KEY,
    base_url="https://api.siliconflow.cn/v1"
)


def ask_bogle_equation():
    # 1. 组装消息列表 (这就是大模型 API 的核心 Payload)
    messages = [
        {
            "role": "system",
            "content": "你是一个在华尔街摸爬滚打多年的顶尖交易员。你性格尖酸刻薄，极度看重基本面和效率，说话一针见血，带着对散户的轻视，但你的专业知识绝对扎实。你的回答要短平快，直击痛点。"
        },
        {
            "role": "user",
            "content": "请详细解释一下博格公式（Bogle's Equation）在指数投资中的应用。"
        }
    ]

    try:
        # 2. 发起 API 请求
        response = client.chat.completions.create(
            model="Pro/moonshotai/Kimi-K2.5",  # 使用硅基流动提供的Kimi-K2.5模型
            messages=messages,  # 发给发模型的对话列表
            temperature=0.8,  # 稍微调高一点，让他的“毒舌”更具创造力
            stream=True  # 关键参数：开启流式输出
        )

        # 3. 处理流式响应 (Streaming)
        # 流式输出是一小块一小块 (chunk) 返回的，我们需要遍历拼合
        for chunk in response:
            # 检查当前块是否有内容（最后结束时内容可能为 None）
            if chunk.choices[0].delta.content is not None:
                # print 默认会换行，用 end="" 阻止换行，用 flush=True 强制立即输出到终端
                print(chunk.choices[0].delta.content, end="", flush=True)

    except Exception as e:
        print(f"\nAPI 请求失败，可能是网络或 Key 的问题: {e}")


if __name__ == "__main__":
    ask_bogle_equation()
```

当你运行这段代码时，你会看到控制台里的字是一个一个“蹦”出来的。你得到的回答大概率会是这种画风：

```
听着，别再用你那可怜的小脑袋去猜明天涨跌了。博格公式就是给你这种数学白痴准备的底限思维工具，省得你总在Reddit上问"为什么我的指数基金会跌"这种蠢问题。

**公式就三行：**
**长期回报 = 股息率 + 盈利增长率 + 市盈率变化**

拆解给你听，免得你又在散户论坛被收割：

**1. 股息率（目前标普500约1.3%）**
这是你能实实在在揣兜里的现金，不是那些你永远不分仓的纸面富贵。别嫌少，这是你唯一的确定性。

**2. 盈利增长（历史均值4-5%，现在能拿3%就该烧香）**
企业真正创造价值的能力。但醒醒，现在GDP增速放缓，AI泡沫能撑多久？这部分正在缩水。

**3. 市盈率变化（ aka 投机溢价）**
过去十年估值从15倍吹到25倍，贡献了年化4-5%的虚幻收益。这部分正在归零，甚至倒扣。**你现在冲进去，就是在为别人的退休买单。**

**应用？**
用来戳破你那些"年化15%"的春梦。按当前数据算：**1.3% + 3% - 2%（估值回归）= 2-3%的实际回报**，还没扣你那愚蠢的1%管理费。

博格创建Vanguard时就看透了：散户唯一的优势就是**成本**。可你们这帮韭菜宁愿付高额申购费给明星基金经理，也不愿买0.03%费率的指数基金，活该被复利反向收割。

**结论：**公式告诉你，现在买宽基就是接飞刀。要么接受未来十年平庸到令人窒息的回报，要么等着估值杀把你本金削掉30%。自己选，别到时候又来哭。
```
