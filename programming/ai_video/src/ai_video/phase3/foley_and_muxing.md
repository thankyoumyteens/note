# 拟音与环境混流

接下来就是为这段视频注入“灵魂”的最后一步了——**拟音（Foley）与环境混流（Muxing）**。

在视频工业界，有一句名言：“声音占了画面的 50%”。一段无声的高清视频看起来像监控录像，但加上微风拂过麦克风的低频底噪，以及衣服摩擦的沙沙声，它瞬间就会变成电影。

咱们直接调用目前开源界最强的环境音/音效生成模型：**AudioLDM 2** 或者 Meta 的 **AudioGen**。它们同样基于 Diffusion 架构，能根据提示词直接生成极具物理质感的 WAV 音频。

## 环境准备

在你的 `wan_video` 环境中补充几个处理音频和视频合成的轻量级库：

```sh
pip install diffusers transformers soundfile moviepy scipy
```

## 生成环境音 (`add_foley_to_video.py`)

这个脚本分为两步：先让显卡“听着”提示词生成一段 5 秒的物理环境音，然后用代码把这段声音和你之前的完美视频“缝合”在一起。

```python
import os
import torch
import scipy.io.wavfile
import warnings

# --- 核心黑魔法：Hugging Face 猴子补丁 ---
from transformers.generation.utils import GenerationMixin
from transformers.models.gpt2.modeling_gpt2 import GPT2Model

# 如果 GPT2Model 丢失了该方法，我们强行从 GenerationMixin 中借用并注入
if not hasattr(GPT2Model, "_update_model_kwargs_for_generation"):
    GPT2Model._update_model_kwargs_for_generation = GenerationMixin._update_model_kwargs_for_generation
# ----------------------------------------

from diffusers import AudioLDM2Pipeline
from moviepy import VideoFileClip, AudioFileClip

warnings.filterwarnings("ignore")

# 生成的视频
input_video = "cartethyia_walking_wan_14B_ultra_stable.mp4"
# 生成的音频
temp_audio = "temp_ambient_foley.wav"
# 融合后的视频
output_video = "cartethyia_walking_cinematic_audio.mp4"

# 1. 声音提示词工程 (Audio Prompting)
audio_prompt = "Gentle breeze blowing. Subtle rustling of a heavy knit sweater and scarf. High fidelity, cinematic daytime street ambience, ASMR."
negative_audio_prompt = "noise, static, speaking, music, low quality, distorted"

device = "cuda"

print("🎵 正在装载 AudioLDM 2 拟音引擎...")
repo_id = "cvssp/audioldm2"
pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

print(f"🎙️ 正在根据物理材质生成环境音轨 (长度: 5秒)...")
audio = pipe(
    audio_prompt,
    negative_prompt=negative_audio_prompt,
    num_inference_steps=200,
    audio_length_in_s=5.0,
    generator=torch.Generator("cuda").manual_seed(42)
).audios[0]

scipy.io.wavfile.write(temp_audio, rate=16000, data=audio)
print("✅ 音频生成完毕！")

# 2. 视频与音频混流 (Muxing)
print("🎬 正在将 AI 拟音与视频流合并...")
video_clip = VideoFileClip(input_video)
audio_clip = AudioFileClip(temp_audio)

final_clip = video_clip.with_audio(audio_clip)

final_clip.write_videofile(
    output_video,
    codec="libx264",
    audio_codec="aac",
    fps=video_clip.fps,
    logger=None
)

os.remove(temp_audio)
print(f"🎉 史诗级闭环！带声音的最终大片已生成: {output_video}")
```

## 为视频脚步声

对于这种需要高度视觉反馈的精细活儿，直接用图形化界面（GUI）是最高效的：

1. 下个剪映 (CapCut) 电脑版：免费、轻量、不需要学。
2. 导入素材：把你那段无声的视频，以及生成的脚步声拖进去。
3. 视觉对齐：拖动脚步声区块，让它在时间轴上刚好对齐画面里卡提希娅脚落地的瞬间。
4. 调一下音量大小，直接点右上角“导出”。整个过程绝对不超过 2 分钟。

单脚步声生成脚本 (generate_single_step.py):

```py
import random

import torch
import scipy.io.wavfile
import warnings

# --- 核心黑魔法：Hugging Face 猴子补丁 ---
from transformers.generation.utils import GenerationMixin
from transformers.models.gpt2.modeling_gpt2 import GPT2Model

if not hasattr(GPT2Model, "_update_model_kwargs_for_generation"):
    GPT2Model._update_model_kwargs_for_generation = GenerationMixin._update_model_kwargs_for_generation
# ----------------------------------------

from diffusers import AudioLDM2Pipeline

warnings.filterwarnings("ignore")

# 1. 极限单音轨 Prompt 工程 (Foley Prompting)
# 关键词解析：single（单次）, isolated（隔离）, dry（干声/无混响）, sharp transient（锐利瞬态/清脆）
foley_prompt = "A single, isolated sharp footstep of a heavy leather boot stepping on solid concrete. Dry studio recording, close-up mic, clear transient, absolutely no background noise, no wind."

# 负面词极其重要：压制模型的“场景脑补”本能
negative_prompt = "multiple steps, walking, continuous, wind, echo, reverb, background noise, speaking, ambient"

output_audio = "single_step.wav"
device = "cuda"

print("🎵 正在装载 AudioLDM 2 拟音引擎...")
repo_id = "cvssp/audioldm2"
pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

# 生成一个随机种子 (取值范围 0 到 2的32次方-1)
current_seed = random.randint(0, 4294967295)
print(f"🎲 当前抽卡种子 (Seed): {current_seed} --- [如果听到了完美的声音，请死死记住这个数字！]")
print(f"🎙️ 正在生成单次高精度脚步声 (长度: 1.0秒)...")
# 生成仅仅 1 秒的极短音频
audio = pipe(
    foley_prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=200,  # 保持 200 步高精度推演
    audio_length_in_s=1.0,  # 强制截断在 1 秒
    guidance_scale=6.5,  # 稍微提高提示词引导度，强制让它听话
    generator=torch.Generator("cuda").manual_seed(current_seed)
).audios[0]

scipy.io.wavfile.write(output_audio, rate=16000, data=audio)
print(f"✅ 完美提取！单次脚步声已保存为: {output_audio}")
```

由于 AI 生成声音有一点“抽卡”的性质，如果你跑出来的声音不理想，你可以尝试跑几次，就像生图“抽卡”一样，抽出那声最符合卡提希娅那双黑色靴子质感的“嗒”声。
