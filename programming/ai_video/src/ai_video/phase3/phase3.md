# 阶段三：使用代码生成视频

把 ComfyUI 生成的图片改名成 cartethyia_front.png。在同级目录下创建一个名为 `run_video.py` 的文件，填入以下内容：

```py
import torch
import gc
from diffusers import DiffusionPipeline
from transformers import UMT5EncoderModel
from diffusers.utils import export_to_video
from PIL import Image
import os

model_path = r"C:\Users\ILove\software\ai_video\Wan\Wan-14B-I2V-720P"

print("🧹 阶段 0: 清扫环境，准备迎接 192GB 混合内存挑战...")
gc.collect()
torch.cuda.empty_cache()

# ==========================================
# 1. 稳健加载：全部使用原生 bfloat16 (不量化)
# ==========================================
print("⏳ 阶段 1/2: 加载 Text Encoder...")
text_encoder = UMT5EncoderModel.from_pretrained(
    model_path,
    subfolder="text_encoder",
    torch_dtype=torch.bfloat16
)

print("⚙️ 阶段 2/2: 加载核心 DiT 管道 (原生精度)...")
pipe = DiffusionPipeline.from_pretrained(
    model_path,
    text_encoder=text_encoder,
    torch_dtype=torch.bfloat16,
    use_safetensors=True
)

# ==========================================
# 3. 核心绝招：开启【层级序列卸载】
# ==========================================
# 这个函数比之前的 model_cpu_offload 更彻底。
# 它会让 140 亿参数以“流”的形式经过你的 5090。
# 这样即便显存只有 4GB 都能跑通，更别提你的 24GB 了！
pipe.enable_sequential_cpu_offload()
pipe.vae.enable_tiling()

# ==========================================
# 4. 注入指令与点火
# ==========================================
image_path = "cartethyia_front.png" # 可以改成你自己的图片文件名
input_image = Image.open(image_path).convert("RGB")

# 【正向算子】：精准描述穿搭，加入迎面走来和风吹拂的物理动态
prompt = "A beautiful anime girl, Cartethyia, facing the viewer, walking slowly towards the camera on a sunlit paved street. She is wearing a white beret, a black scarf, a white cable-knit sweater, and a blue plaid skirt. Wind is gently blowing her long blonde hair and scarf. Perfectly smooth motion, natural fabric physics, realistic sunlight and shadows, masterpiece video."

# 【反向黑名单】：除了视频防闪烁，特别加强了防衣服扭曲和面部崩坏
negative_prompt = "mutated, deformed, bad anatomy, jittering, flickering, boiling background, morphing clothes, distorted face, duplicate, extra limbs, unnatural movement"

print("🚀 启动 DiT 时序渲染！这次不搞任何骚操作，用物理内存硬刚！")
# 恢复 33 帧，享受 5090 的全精度推演
video_frames = pipe(
    image=input_image,
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=40,
    guidance_scale=7.0,
    # 将帧数推向模型上限 81 帧
    num_frames=81,
    # 生成竖屏视频(Wan 2.2 的 3D-VAE 极其严格，要求画面的长宽必须是 16 的倍数)
    height=1216,
    width=832,
    generator=torch.Generator("cuda").manual_seed(1024)
).frames[0]

output_path = "cartethyia_walking_wan_14B_ultra_stable.mp4"
export_to_video(video_frames, output_path, fps=16)
print(f"🎉 史诗级胜利！视频已通过‘时间换空间’策略成功保存至: {output_path}")
```

## 创建快速启动脚本

创建一个名为 `run_video.bat` 的批处理文件，填入以下内容：

```bat
cd 换成 run_video.py 所在的目录
conda activate wan_video
python run_video.py
pause
```

双击 `run_video.bat` 即可启动。
