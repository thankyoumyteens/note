# 语气控制

实现语气控制的核心在于**在代码中动态拼接文本标签**，并**动态配置 `InferCodeParams` 参数对象**。

在实际的代码工程中，我们通常不会把控制标签硬编码在字符串里，而是让系统（或大语言模型）根据上下文动态生成。

以下是一个完整的代码示例，展示了如何在 Python 脚本中同时结合**“标签插入”、“温度调节”和“特定情绪音色加载”**这三种手段。

### 实战代码：动态情绪合成脚本

你可以新建一个 `emotion_control_demo.py` 来运行测试这段代码。

```python
import ChatTTS
import torch
import soundfile as sf
import os

print("正在加载 ChatTTS 模型...")
chat = ChatTTS.Chat()
chat.load(compile=False)

# ==========================================
# 1. 模拟加载你的“情绪专属音色库”
# 在实际应用中，你需要先通过抽卡把对应的 .pt 文件保存下来
# 这里为了演示，我们临时随机生成一个特征代替
# ==========================================
# 实际生产中这里应该是: my_spk = torch.load("我的专属音色.pt")
my_spk = chat.sample_random_speaker()
print("✅ 已锁定专属音色，接下来所有生成都基于这个人。")
def generate_speech(text, emotion_type, output_filename):
    print(f"\n--- 正在让这个声音表演 [{emotion_type}] 情绪 ---")

    if emotion_type == "calm":
        # 平静模式：
        # 1. 不加任何多余的标点和 Token，或者用句号代替逗号让语速变缓
        # 2. Temperature 压低，让他控制住情绪，像播音员一样
        final_text = text
        params = ChatTTS.Chat.InferCodeParams(
            spk_emb=my_spk,       # 【关键】使用同一个音色
            temperature=0.2,      # 情绪起伏极小，声音极度稳定
            top_P=0.7             # 限制发音的多样性
        )

    elif emotion_type == "excited":
        # 激动模式：
        # 1. 强行插入笑声 [laugh] 和感叹号 (注意全半角)
        # 2. Temperature 拉高，让他放飞自我，音调会自然变高变扬
        final_text = text.replace("。", "! ") + " [laugh]"
        params = ChatTTS.Chat.InferCodeParams(
            spk_emb=my_spk,       # 【关键】依然是这同一个人！
            temperature=0.65,     # 允许情绪产生较大的波动和起伏
            top_P=0.9             # 允许发音有更多变化
        )

    else:
        raise ValueError("不支持的情绪类型")

    print(f"台词: {final_text}")
    print(f"情绪释放度 (Temperature): {params.temperature}")

    wavs = chat.infer([final_text], params_infer_code=params)

    audio_data = wavs[0].squeeze()
    sf.write(output_filename, audio_data, 24000)
    print(f"✅ 生成完毕: {output_filename}")

# ==========================================
# 2. 测试运行
# ==========================================
# 让这个人平静地说
generate_speech(
    text="关于明年的架构演进，我们可能需要重新评估微服务的边界。",
    emotion_type="calm",
    output_filename="same_person_calm.wav"
)

# 让同一个人激动地/大笑着说
generate_speech(
    text="这个 Bug 终于修复了，太不容易了", # 故意不加句号，在代码里替换
    emotion_type="excited",
    output_filename="same_person_excited.wav"
)
```

## ChatTTS 的情绪瓶颈

这种通过 Temperature 和 Token 来改变同一个音色情绪的做法，效果是有上限的。

“底色”很难洗掉：如果你一开始抽到的那个 my_spk（音色种子）的主人，在训练集里的原声就是一个声音极度低沉、毫无生气的男低音，那么即使你把 temperature 拉到 0.8，疯狂加 `[laugh]`，他听起来也只是一个 **“在冷笑的冷漠男低音”**，很难变成那种极其阳光活泼的声音。

在实际的商业落地中（比如很多情感陪伴 Agent），因为模型很难把同一个声音无缝拉扯出跨度极大的情绪，很多开发者会采用 **“特征插值（Embedding Interpolation）”**的黑科技：

1. 准备一个 主音色.pt。
2. 准备一个 通用愤怒音色.pt。
3. 在代码里把这两个张量按比例融合：`final_spk = (主音色 * 0.8) + (通用愤怒音色 * 0.2)`。

这样既保持了主音色 80% 的辨识度（听起来还是那个人），又强行混入了 20% 的愤怒感。

### 实战代码：张量混合与特征插值

你可以新建一个 embedding_mix.py 来运行：

```py
import ChatTTS
import torch
import soundfile as sf
import lzma
import numpy as np
import pybase16384 as b14  # ChatTTS 自带的编码库

print("正在加载 ChatTTS 模型...")
chat = ChatTTS.Chat()
chat.load(compile=False)

# ==========================================
# 1. 解码与编码的黑科技函数 (应对最新版 ChatTTS 机制)
# ==========================================
def decode_spk(spk_str):
    """将压缩字符串解压回 PyTorch 数学张量"""
    compressed = b14.decode_from_string(spk_str)
    # 必须使用与 ChatTTS 官方完全一致的解压滤镜
    filters = [{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}]
    decompressed = lzma.decompress(compressed, format=lzma.FORMAT_RAW, filters=filters)
    return torch.tensor(np.frombuffer(decompressed, dtype=np.float16))

def encode_spk(tensor):
    """将运算后的张量重新压缩回 ChatTTS 认识的字符串"""
    np_array = tensor.cpu().numpy().astype(np.float16)
    filters = [{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}]
    compressed = lzma.compress(np_array.tobytes(), format=lzma.FORMAT_RAW, filters=filters)
    return b14.encode_to_string(compressed)

# ==========================================
# 2. 准备基础特征 (抽取到的是字符串)
# ==========================================
print("正在抽取测试音色...")
torch.manual_seed(1024)
spk_main_str = chat.sample_random_speaker() # 专属主音色

torch.manual_seed(2048)
spk_angry_str = chat.sample_random_speaker() # 通用情绪音色

# ==========================================
# 3. 核心黑科技：解压 -> 插值融合 -> 重新打包
# ==========================================
main_weight = 0.75
emotion_weight = 0.25

print(f"正在进行张量融合 (主音色 {main_weight*100}% + 情绪音色 {emotion_weight*100}%)...")

# 第一步：把乱码字符串解压为可以计算的 Tensor
tensor_main = decode_spk(spk_main_str)
tensor_angry = decode_spk(spk_angry_str)

# 第二步：进行张量高维空间的插值混合
tensor_mixed = (tensor_main * main_weight) + (tensor_angry * emotion_weight)

# 第三步：把混合后的新音色，重新打包回 ChatTTS 能识别的字符串
spk_mixed_str = encode_spk(tensor_mixed)

# ==========================================
# 4. 对比测试
# ==========================================
text = "这个需求完全不合理，你们到底有没有看文档。"

def generate_and_save(spk_string, output_name, desc):
    print(f"\n正在生成: {desc}")
    # ChatTTS 现在需要的是重新编码过的字符串
    params = ChatTTS.Chat.InferCodeParams(
        spk_emb=spk_string,
        temperature=0.5
    )
    wavs = chat.infer([text], params_infer_code=params)
    sf.write(output_name, wavs[0].squeeze(), 24000)
    print(f"✅ 已保存: {output_name}")

# 分别听一下三者的区别
generate_and_save(spk_main_str, "1_pure_main.wav", "纯主音色")
generate_and_save(spk_angry_str, "2_pure_angry.wav", "纯情绪音色")
generate_and_save(spk_mixed_str, "3_mixed_result.wav", "75%主音色 + 25%情绪音色")

print("\n🎉 融合完毕！快去对比听听第 3 个音频是不是那个带着怒气的专属声音！")
```

权重的魔法边界：

- 主音色占比 0.7 ~ 0.9 之间是最安全的。
- 如果你把情绪音色的权重调得太高（比如 0.5 + 0.5），结果往往听起来既不像原来的你，也不像那个愤怒的人，反而会变成一个完全陌生的第三个人。特征空间的中心点往往是一个比较平庸的平均声音。

情绪库的建立：

- 如果要在你的后端工程里落地，你需要花点时间用你的 5090 去“刷”出几个极致的单极情绪向量（例如：极其开朗大笑的向量、极其低沉悲伤的向量、极其急促紧张的向量），并将它们作为基准库保存下来。
- 未来遇到需要对应情绪的时候，就直接用公式 `(专属向量 * 0.8) + (极性库向量 * 0.2)` 进行实时运算。PyTorch 做这种维度的张量加减法耗时在微秒级，完全不会影响你的流式推理延迟。

## 如何在 AI Agent 中落地？

如果在你的项目中，文本是由另一个大语言模型（比如 Qwen 或 Llama 3）生成的，你肯定不能指望大模型完美地输出符合 ChatTTS 规范的 `[laugh]` 标签。

**业界标准落地架构（LLM + TTS 路由机制）：**

1.  **约束大模型输出 JSON**：
    在提示词（Prompt）中，要求大模型在输出回复文本的同时，附带当前的情绪判定。

    ```json
    // LLM 的输出
    {
      "reply": "哈哈哈哈，你这个想法太疯狂了，但我喜欢！",
      "emotion_tag": "excited"
    }
    ```

2.  **中间件拦截与处理（Python 逻辑）**：
    你的代码接收到这个 JSON 后，提取 `emotion_tag`。

3.  **动态映射 TTS 参数**：
    编写一个路由函数，根据提取到的标签做映射。
    - 如果 `emotion_tag == "excited"` -> 加载 `活泼音色.pt`，设置 `temperature = 0.65`，并在 `reply` 文本适当位置（如句首或句尾）通过代码拼接 `[laugh]` 标签。
    - 如果 `emotion_tag == "sad"` -> 加载 `低沉音色.pt`，设置 `temperature = 0.2`，并在逗号处随机插入 `[uv_break]` 模拟叹气。

4.  **调用 API**：
    将组装好的带标签文本和配置好的 `InferCodeParams` 发送给 ChatTTS 的推理端点。
