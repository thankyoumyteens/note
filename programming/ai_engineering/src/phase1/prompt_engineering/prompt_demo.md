# 一个工业级的信息抽取 Prompt

这个 Prompt 结合了你提到的 Few-Shot（少样本） 和 CoT（思维链） 技巧，并做了严格的格式约束。

你可以直接复制并在任何大模型（如 Gemini、GPT-4、Claude 等）中测试它：

```sh
# Role
你是一个专业的金融市场数据抽取引擎。你的任务是从冗长杂乱的市场新闻中提取关键信息。

# Task
请仔细阅读 [Input] 中的新闻文本，提取相关信息，并**严格以合法的 JSON 格式输出**。

# Extraction Fields (JSON Schema)
请确保你的 JSON 包含以下字段：

- `company_name`: 公司名称（包含股票代码，如有）
- `main_event`: 事件主体（客观概括发生的核心事件）
- `reasoning`: 推理过程（**请一步一步思考**：该事件如何影响公司的成本、收入、市场份额或未来预期？）
- `earnings_impact`: 对财报的潜在影响（仅限：正面 / 负面 / 中性，并附带一句话简短结论）

# Rules
1. 严格按照 JSON 格式输出，不要输出任何额外的问候语、解释性文本。
2. 即使新闻内容含糊不清，也请尽力推断；如果完全没有提及某项内容，请填入 "null"。

# Examples (Few-Shot)

## Example 1
**Input:** 苹果公司今天在发布会上宣布推出全新的 M4 AI 芯片，算力较上一代提升了一倍，且服务器功耗降低了 30%。华尔街分析师普遍认为，这将大幅提升其第三季度的硬件利润率。
**Output:**
{
"company_name": "苹果公司 (Apple)",
"main_event": "推出全新 M4 AI 芯片，算力翻倍，功耗降低 30%。",
"reasoning": "功耗降低直接减少运营成本；算力翻倍提升了产品竞争力，有望刺激硬件销量。成本下降加上销量预期上升，将改善整体利润表现。",
"earnings_impact": "正面。预计将显著提升第三季度硬件利润率。"
}

## Example 2
**Input:** 数据分析公司 Palantir (PLTR) 近日意外流失了英国国家医疗服务体系 (NHS) 的一份重要政府合同，该合同约占其欧洲区总营收的 5%。不过有消息指出，其商用业务板块本季度实现了 15% 的超预期增长。
**Output:**
{
"company_name": "Palantir (PLTR)",
"main_event": "流失占欧洲营收 5% 的英国 NHS 政府合同，但商用业务实现 15% 增长。",
"reasoning": "政府大单流失会直接削减短期的确定性收入；但商用业务的强劲增长表明其商业化转型正在加速，能够部分对冲政府订单流失的损失。",
"earnings_impact": "中性偏负面。短期营收承压，但商用业务的增长缓解了对整体财报的冲击。"
}

# Input
[请在此处粘贴你需要分析的冗长杂乱的新闻文本]
```

为什么这个 Prompt 会很强大？（拆解你的“新业务逻辑”）

1. 结构化指令（Role & Task）：相当于传统后端的 class 和 method 定义，明确了模型的作用和核心任务。
2. 强制类型定义（Extraction Fields & Rules）：明确指出需要提取的 4 个字段，相当于定义了数据模型（Data Model）。同时用明确的 Rule 斩断了大模型喜欢“废话连篇”的习惯，确保输出可以直接被代码中的 `JSON.parse()` 解析。
3. 隐式 CoT (思维链)：我特意在字段中加入了一个 reasoning 字段，并在括号里加入了“请一步一步思考”。这不仅仅是为了给你看分析过程，更是为了强迫模型在得出 earnings_impact 结论之前，先在 reasoning 里进行逻辑推演。这能极大降低大模型瞎编（幻觉）的概率。
4. Few-Shot (少样本提示)：提供了两个正反面的 Example。大模型很聪明，它会模仿 Example 中的语言风格、颗粒度和 JSON 结构。

## 如何使用这个 Prompt

拿到这个 Prompt，就像你在传统开发中写好了一个复杂的 function 或定义了一个新的接口，接下来的关键是怎么去执行它。

根据你的使用场景，有两种典型的用法：一种是人工测试（调试阶段），另一种是代码集成（生产阶段）。

### 在网页端直接测试（“调试”阶段）

在把 Prompt 写进代码之前，我们通常会直接在 AI 对话框里进行“黑盒测试”。

步骤：

1. 复制整个 Markdown 格式的 Prompt。
2. 准备数据：去财经网站随便复制一段关于某个公司的杂乱新闻、研报片段或社交媒体长文。
3. 替换占位符：把 Prompt 最后一行 `[请在此处粘贴你需要分析的冗长杂乱的新闻文本]` 替换成你找的新闻原文。
4. 发送给大模型：回车发送，观察模型输出的 JSON 是否符合预期。
   - 提示： 如果发现它偶尔不按要求输出 JSON，或者提取的信息不准，你就继续修改 Prompt（调整指令或增加 Example），这就相当于传统开发中的“改 Bug”。

### 在代码中调用（“生产”阶段）

这是 AI 原生应用最核心的一步。你要在后端代码里通过调用大模型 API（比如 OpenAI API 或 Google Gemini API）来执行这个 Prompt，并将大模型返回的 JSON 字符串反序列化为代码中的对象，供后续业务逻辑使用。

````py
import json
import openai # 假设使用 OpenAI 的 API

# 1. 定义你的“业务逻辑” (Prompt Template)
PROMPT_TEMPLATE = """
# Role
你是一个专业的金融市场数据抽取引擎... (此处省略中间内容，就是把上面的 Prompt 粘过来)

# Input
{news_text}
"""

def extract_financial_info(raw_news: str):
    # 2. 动态注入变量 (相当于传参)
    final_prompt = PROMPT_TEMPLATE.format(news_text=raw_news)

    # 3. 调用大模型 API执行“业务流转”
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.1 # 抽取任务建议把 temperature 调低，让输出更确定、更严谨
    )

    # 4. 获取大模型的文本输出
    result_text = response.choices[0].message.content

    # 5. 清洗并解析 JSON (将非结构化文本转化为结构化数据)
    # 有时模型会带上 ```json ``` 标记，需要做个简单的字符串剥离
    clean_text = result_text.replace("```json", "").replace("```", "").strip()

    try:
        # 传统后端的精髓来了：转成真正的 Object/Dict 供下游使用！
        data_object = json.loads(clean_text)
        return data_object
    except json.JSONDecodeError:
        return {"error": "大模型没有返回合法的 JSON"}

# --- 实际使用 ---
messy_news = "路透社报道，Palantir (PLTR) 刚刚赢得了一份价值 4.8 亿美元的美国国防部大单..."
extracted_data = extract_financial_info(messy_news)

# 现在你可以像操作普通对象一样操作它了
print("提取到的公司:", extracted_data.get("company_name"))
if extracted_data.get("earnings_impact") == "正面":
    print("触发买入信号逻辑...") # 衔接传统的 if/else 业务逻辑
````

核心思维转变：你看，在 extract_financial_info 这个函数里，没有任何正则匹配、没有复杂的字符串截取、没有 NLP 算法库。所有的脏活累活，都被那一段长长的 Prompt 在大模型的黑盒里搞定了。最后输出的，就是清清爽爽的标准对象。这就是 AI 时代的“新业务逻辑”。
