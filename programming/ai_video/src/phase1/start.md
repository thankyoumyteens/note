# 生成第一张图片

### 1. 进入 JupyterLab 终端

1. RunPod 开机
2. 点击面板上的 `Port 8888 -> JupyterLab` 快捷入口。这会打开一个类似完整操作系统的网页界面。
3. 在 JupyterLab 界面中，点击左上角的蓝色加号按钮，新建一个 Terminal。

### 2. 下载模型

```sh
# 大模型（Checkpoint）必须严格存放在特定的文件夹下 ComfyUI 才能识别
cd /workspace/runpod-slim/ComfyUI/models/checkpoints/
# 下载 NoobAI XL 旗舰底模 (约 6.4GB)
wget -c -O NoobAI-XL.safetensors "https://huggingface.co/Laxhar/noobai-XL-1.1/resolve/main/NoobAI-XL-v1.1.safetensors"
```

### 3. 打开 ComfyUI 图形化操作界面

下载完成后，回到 RunPod 页面点击 `Port 8188 -> ComfyUI`。

左下角设置图标 -> comfy -> 区域设置 -> 语言 -> 换成 English。

### 4. 添加模块

在空白区域双击左键（或者点击右键 -> Add Node），按照以下逻辑添加四个核心模块：

1. loaders：
   - Load Checkpoint：选择我们刚下的 NoobAI-XL.safetensors。
2. conditioning：
   - CLIP Text Encode (Prompt)：你需要添加两个，一个用于正面描述，一个用于负面描述。
3. latent：
   - Empty Latent Image：这是你的“数字画布”，设置为 832 x 1216。
   - VAE Decode：将潜空间数据转回图片。
4. sampling
   - KSampler：这是 AI 的“大脑”，负责进行去噪运算。
5. image：
   - Save Image：预览你的成果。

### 5. 连线

在 ComfyUI 中，不同颜色的端口代表不同的数据类型。你现在需要把这些“孤岛”节点按照数据流向串联起来。

请按照以下逻辑进行物理连线（鼠标左键按住端口拖动到目标端口）：

1. Model 骨干网 (紫色线):
   - Load Checkpoint (MODEL) → KSampler (model)
2. CLIP 语义网 (黄色线):
   - Load Checkpoint (CLIP) → 两个 CLIP Text Encode 的 (clip) 输入端。
3. Conditioning 条件控制 (桔色线):
   - CLIP Text Encode (你用作正面词的) (CONDITIONING) → KSampler (positive)
   - CLIP Text Encode (你用作负面词的) (CONDITIONING) → KSampler (negative)
4. Latent 潜空间传输 (粉色线):
   - Empty Latent Image (LATENT) → KSampler (latent_image)
   - KSampler (LATENT) → VAE Decode (samples)
5. VAE & Pixel 输出 (红色线/蓝色线):
   - Load Checkpoint (VAE) → VAE Decode (vae)
   - VAE Decode (IMAGE) → Save Image (image)

### 6. 参数注入

1. 填入提示词 (Prompts)
   - 正向 (Positive): masterpiece, best quality, cartethyia, circlet, earrings, blue eyes, grey pupils, 1girl, solo, blonde hair, sweet smile, (white knit sweater, scarf, plaid skirt, white beret:1.3), night street, cinematic lighting, highres
   - 负面 (Negative): lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, worst quality, low quality
2. 配置 KSampler (The Brain)
   - seed: 不用管
   - control_after_generate: randomize。
   - steps: 30。
   - cfg: 5.0 (NoobAI 专用低 CFG)。
   - sampler_name: euler。
   - scheduler: normal。
   - denoise: 1.00。

### 6. 生成图片

一切就绪后，点击右侧控制面板顶部的 Run。

- 看状态：你会看到节点周围出现绿色边框在跳动，这代表数据流正在该节点进行计算。
- 看显存：5090 加载 NoobAI-XL 大约需要 2-3 秒，一旦加载完毕，采样过程会快得让你产生“幻觉”。
- 查看结果：最终，图片会出现在 Save Image 节点的预览框里。

![](../img/start.jpg)

## 模块说明

这其实就是一个标准的有向无环图 (DAG) 任务流，数据从左向右流动：

- Load Checkpoint（Checkpoint 加载器）：这是整个流的起点，负责把几 GB 的权重文件加载进你 5090 的显存里。
- CLIP Text Encode（CLIP 文本编码）：有两个框，一个框填正向提示词（你想要的画面，比如 1girl, beautiful, cinematic lighting），另一个框填反向提示词（你不想要的，比如 ugly, bad anatomy）。
- KSampler（K采样器）：这是算力消耗的核心节点，它负责根据你的文本，一步步去噪生成图像。
- Save Image（保存图像）： 渲染出的最终结果。

你可以顺着这两个 CLIP 文本编码节点右侧黄色的 条件 (CONDITIONING) 输出点，沿着连线往右看，一直看到 K采样器 (KSampler) 节点：

- 上面的节点：它的线连到了 K采样器的 正向条件 (positive) 接口。所以它就是正向提示词。
- 下面的节点： 它的线连到了 K采样器的 负面条件 (negative) 接口。所以它就是反向提示词。

这就是 ComfyUI 作为节点式工作流最核心的逻辑——完全靠连线（数据的流向）来决定。
