# 提示词缓存

Prompt Caching 是一种发生在 LLM（大模型）服务器内存深处的“前缀状态复用（KV Cache Reuse）”技术。

想象一下 Java MCP Agent：每次你发请求，你不仅发了用户的提问（几十个字），你还必须把厚厚的“系统人设”、几十个“MCP 工具的 JSON Schema”、甚至一大段“RAG 检索出来的企业规章制度”一起打包发过去。

这就会导致一个极其绝望的局面：每次请求的有效信息只有 50 个 Token，但前面的“背景铺垫”足足有 5000 个 Token！ 大模型每次都要傻乎乎地重新阅读并计算这 5000 个背景 Token，极度浪费算力。

Prompt Caching 的核心法则：精确前缀匹配 (Exact Prefix Match)。

只要你两次请求的**开头部分（Prefix）**一字不差，大模型就会直接从它的内存里把上一次计算好的中间状态（KV Cache）端出来，跳过阅读阶段，直接开始回答。

目前，OpenAI 和 Anthropic (Claude) 对待 Prompt Caching 的策略有所不同。

1. OpenAI 的“隐式羊毛” (Implicit Caching): OpenAI（如 GPT-4o）不需要你改任何代码。只要你的 Prompt 大于 1024 个 Token，它就会自动在后台帮你缓存前缀。

   ```py
   # ❌ 极其愚蠢的写法 (缓存永远无法命中)
   messages = [
       # 动态时间放在了开头，前缀永远在变！
       {"role": "user", "content": f"今天是 {datetime.now()}。请查询订单。"},
       {"role": "system", "content": "你是一个极其复杂的 ERP 助手... (5000 tokens)"}
   ]

   # ✅ 架构师的正确写法 (享受 50% 成本减免)
   messages = [
       # 静态的巨石放在最前
       {"role": "system", "content": "你是一个极其复杂的 ERP 助手... (5000 tokens)"},
       # 动态小尾巴放在最后
       {"role": "user", "content": f"今天是 {datetime.now()}。请查询订单。"}
   ]
   ```

2. Anthropic (Claude) 的“显式断点” (Explicit Caching): Claude 更加硬核，它允许你在代码里手动打上 `cache_control` 的断点。告诉模型：“读到这里，把前面的内容给我死死记住！”
3. Google (Gemini)极其灵活的“双规制”
   1. 隐式缓存 (Implicit caching)：在 Gemini 2.5 及以后的模型中默认开启，原理类似 OpenAI，自动命中。
   2. 显式缓存 (Explicit caching)：更偏向于一种“云存储服务”。你可以通过 API 提前把几百万字的文档“上传”并冻结成一个 Cache 对象，甚至可以设置它的存活时间（TTL）。后续调用时，直接传入这个对象的 ID 即可。
4. 开源生态 (vLLM, SGLang 等)：如果你打算在公司内部买机器私有化部署开源模型（如 Qwen 或 Llama），现代的推理引擎（Inference Engine）如 vLLM 和 SGLang 早就把 Automatic Prefix Caching (自动前缀缓存) 做成了底层标配。只要开启这个配置，引擎就会在显存里默默帮你省钱。
