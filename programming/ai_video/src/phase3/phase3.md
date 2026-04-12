# 阶段三：原生 DiT 视频生成

在这一阶段，我们将引入三个核心组件来对抗“闪烁地狱”：

1.  **AnimateDiff（时序引擎）**：它在 KSampler 的计算中插入了时间轴（Z轴），强制要求第 N+1 帧的像素必须参考第 N 帧，从而实现平滑的运动。
2.  **OpenPose Video（动态约束）**：不再是单一的 `.jpg`，而是一组连续的视频帧，作为角色的“行走指令”。
3.  **IP-Adapter（风格锚点）**：将一张卡提希娅最完美的静态图作为“样式表”持续输入，确保她在走完 5 秒后，衣服扣子的形状都没有改变。

## 部署视频基建（物理层依赖）

既然我们使用的是 NoobAI (SDXL)，必须使用专用的 SDXL 运动模块。请在 Jupyter Lab 终端执行：

```bash
# 创建 AnimateDiff 专用的模型目录
mkdir -p /workspace/runpod-slim/ComfyUI/models/animatediff_models/

# 拉取 SDXL 专用的运动模块 (约 1.8 GB)
cd /workspace/runpod-slim/ComfyUI/models/animatediff_models/
wget -c -O mm_sdxl_v10_beta.ckpt "https://huggingface.co/guoyww/animatediff/resolve/main/mm_sdxl_v10_beta.ckpt"
```

## 安装插件

1. 回到 ComfyUI 界面，点击 Manager -> Custom Nodes Manager
2. 安装 AnimateDiff Evolved（作者是 Kosinkadink）
3. 安装 Video Helper Suite（作者也是 Kosinkadink）
4. 安装 Advanced-ControlNet（作者也是 Kosinkadink）
5. 安装完成后按提示 Restart 重启 ComfyUI

## 2. 架构拓扑重构（从单机到流式处理）

在 ComfyUI 画布上，你需要对原来的静态工作流进行“流式改造”：

### A. 输入端：Load Video 替代 Load Image

- 搜索 `VHS LoadVideo`
- 添加 `Load Video (Upload) 🎥🅥🅗🅢` 节点
- 上传一段 3-5 秒的真人走路视频（最好背景干净，动作清晰）。
- 参数建议 `frame_load_cap` 设为 48 或 64（约 4-5 秒），防止显存溢出。

### B. 逻辑层：插入 AnimateDiff 模块

- 搜索 `AnimateDiff Loader`
- 添加 `AnimateDiff Loader 🎭🅐🅓①` 节点：选择刚才下载的 `mm_sdxl_v10_beta.ckpt`。
- 搜索 `ADE_AnimateDiffUniformContextOptions`
- 添加 `Context Options◆Looped Uniform 🎭🅐🅓` 节点：设置 `context_length` 为 16（这是滑动窗口的大小，决定了 AI 每次“回顾”多少帧）。
- 搜索 `Advanced ControlNet`
- 添加 `Apply Advanced ControlNet 🛂🅐🅒🅝` 节点：
  - 拉出两个这个新节点，用来替换掉你原来的那两个 Apply ControlNet A 和 Apply ControlNet B
  - 这个新节点的输入/输出端口和老节点一模一样，请照猫画虎地把线重新连上（正向/负向提示词、控制模型、图像）
  - 【关键提醒】：千万别忘了把你辛苦调好的生命周期参数填回去！深度控制网（连着 Zoe-Depth 的那个）： strength 设为 0.9，start_percent 设为 0.0，end_percent 设为 0.65。

## 连线

### 第一步：组装时序引擎并拦截“主模型流”

AnimateDiff 的核心逻辑是：在底模（Checkpoint）和采样器（KSampler）之间横插一刀，注入时间维度。

1. 找到 Context Options (Uniform) 节点，将其右侧的 CONTEXT_OPTS 连入 -> AnimateDiff Loader 左侧的 context_options。
2. 找到你的 LoraLoader 节点（加载了 Cartethyia 的那个）。断开它原本直接连向 KSampler 的那根黄色的 MODEL 线。
3. 将 LoraLoader 的 MODEL 输出 -> 连入 AnimateDiff Loader 左侧的 model 输入。
4. 将 AnimateDiff Loader 右侧的 MODEL 输出 -> 连入 KSampler 左侧的 model 输入。

架构解析：现在主模型的权重在进入采样器之前，已经被 AnimateDiff 强行赋予了前后帧关联的超能力。

### 第二步：重构输入流（从“单张图片”切换为“视频流”）

我们不再需要静态图片作为控制依据，而是要提取视频每一帧的动作。

1. 找到原本的 Load Image 节点（加载 a.png 的那个），断开它右侧连向两个预处理器（DWPose 和 Zoe-Depth）的蓝色 IMAGE 线。然后删掉这个节点
2. 将 VHS_LoadVideo 右侧第一个输出端 IMAGE -> 连入 DWPreprocessor 左侧的 image。
3. 将 VHS_LoadVideo 右侧第一个输出端 IMAGE -> 连入 Zoe-DepthMapPreprocessor 左侧的 image。

架构解析：现在 ControlNet 收到的不再是 1 张图，而是一整个连续的视频帧数组 [Batch of Images]。

### 第三步：同步潜空间批次（防爆存/报错的致命细节）

既然你输入的是一段包含几十帧的视频，你的潜空间画板也必须准备几十张“空画布”，否则点击运行会立刻报张量维度不匹配的致命错误！

1. 找到你的 EmptyLatentImage 节点。
2. 你会发现它目前的 batch_size 还是 1。请把它修改为你视频加载的帧数。
   - 如果你的 VHS_LoadVideo 里 frame_load_cap（最大加载帧数）设为了 64。那么，请务必将 EmptyLatentImage 的 batch_size 也改为 64。

### 重构正向提示词 (Positive Prompt)

```
masterpiece, best quality, cartethyia, 1girl, solo, blonde hair, (view from behind, walking away from viewer:1.4), back, (white knit sweater, scarf, plaid skirt, white beret:1.3), night street, cinematic lighting, highres, knitted sweater texture, soft lighting, stable background
```

### 重构负向提示词 (Negative Prompt)

```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, worst quality, low quality, front view, face, abstract, glitch, colorful blocks, flickering, mutated
```

### 降低 CFG 释放采样压力

1. 找到 KSampler
2. 将 CFG Scale 从 5 修改为 4.0（甚至 3.5）。

### 削弱背景深度图的干扰 (防花屏最后一道防线)

深度图（Zoe-Depth）不仅提取了人物轮廓，还把原视频背景里的杂物也提取了，这会干扰 AI 画“夜景街道”。

1. 找到你的节点 54 ACN_AdvancedControlNetApply_v2 (连着深度图的那个)：
2. 将 strength 从 0.9 降到 0.5。
3. 将 end_percent 从 0.65 降到 0.4。

让深度图只在最开始提供一点点空间参考就赶紧滚蛋，不要妨碍背景的生成。
