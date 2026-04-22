# 音色“抽卡”与持久化

默认情况下，ChatTTS 每次生成的音色是随机的（就像抽卡）。当你偶然“抽”到一个极具磁性或非常甜美的声音时，如果没保存下来就太可惜了。

你可以将好听的音色特征（Speaker Embedding）保存为本地张量文件，以后每次都加载这个专属声音。

## 运行“批量抽卡机”脚本

在你的项目目录下新建一个文件 `gacha_voices.py`，粘贴以下代码并运行：

```py
import ChatTTS
import torch
import soundfile as sf
import os

# 1. 初始化并加载模型
print("正在加载 ChatTTS 模型...")
chat = ChatTTS.Chat()
chat.load(compile=False)

# 抽卡配置
num_draws = 5
test_text = "你好! 我是新生成的音色。[laugh] 听听看我的声音你还满意吗?"

# 创建一个专门放音色的文件夹
output_dir = "my_voice_bank"
os.makedirs(output_dir, exist_ok=True)

print(f"开始连抽 {num_draws} 次...")

for i in range(num_draws):
    seed = 1000 + i
    torch.manual_seed(seed)

    # 提取音色特征
    spk_emb = chat.sample_random_speaker()

    print(f"正在生成第 {i+1}/{num_draws} 个音色 (Seed: {seed})...")

    params = ChatTTS.Chat.InferCodeParams(
        spk_emb=spk_emb,
        temperature=0.3 # 温度越低越稳定，默认通常是 0.3
    )

    # 推理生成
    wavs = chat.infer([test_text], params_infer_code=params)

    # 保存试听音频 (.wav)
    audio_data = wavs[0].squeeze()
    wav_path = os.path.join(output_dir, f"voice_seed_{seed}.wav")
    sf.write(wav_path, audio_data, 24000)

    # 保存音色特征文件 (.pt)
    pt_path = os.path.join(output_dir, f"voice_seed_{seed}.pt")
    torch.save(spk_emb, pt_path)

print(f"\n🎉 抽卡完成！快去 {output_dir} 文件夹下听听看吧！")
```

## 如何加载并使用你的音色

假设你在上一步的文件夹里，听中了一个声音，并把它的 .pt 文件重命名为了 my_favorite_voice.pt。

以后你想用这个声音生成任何长文本，只需要这样写（新建一个 `use_my_voice.py`）：

```py
import ChatTTS
import torch
import soundfile as sf

chat = ChatTTS.Chat()
chat.load(compile=False)

# 1. 【核心】从本地加载你保存的音色文件
print("正在加载专属音色...")
# 注意：把这里的路径换成你刚才选中的那个 .pt 文件的路径
my_spk = torch.load("my_voice_bank/my_favorite_voice.pt")

# 2. 准备你想生成的文本
text = "太棒了，这下我以后所有的视频和 AI 助手，都可以用这个专属的声音来播报了！"

# 3. 推理（把加载的音色传进去）
print("正在使用专属音色生成音频...")
params = ChatTTS.Chat.InferCodeParams(spk_emb=my_spk)
wavs = chat.infer([text], params_infer_code=params)

# 4. 保存结果
sf.write("final_output.wav", wavs[0].squeeze(), 24000)
print("✅ 专属语音生成成功！")
```
