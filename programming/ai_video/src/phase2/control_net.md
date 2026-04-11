# ControlNet

在前面，我们通过写提示词和挂载 LoRA 来画图。这就像是在对 AI 提 **业务需求** ：“给我画一个戴贝雷帽的女孩”。至于她具体怎么站、手放在哪里，AI 内部的黑盒充满了随机性。

用 Java 后端的思维来理解：如果说 LoRA 像是一个 AOP（面向切面编程）的拦截器，负责在底层模型上注入“卡提希娅”的风格和材质；那么 ControlNet 就是一个极其严苛的 Interface（接口约束）。它会拦截进入 KSampler 的数据流，强行要求生成的像素在空间拓扑上必须 100% 吻合你提供的骨架或深度图。

我们可以直接拿一张骑摩托车的照片作为“测试用例”（Test Case）。让 AI 提取骑车时的硬核姿势，然后把卡提希娅完美地“嵌”进这个姿势里。

**ControlNet 就是那个强制的“结构校验器 (Schema Validator)”。** 它剥夺了 AI 在空间构图上的自由发挥权，强制要求生成的像素必须严格吻合你提供的底层拓扑结构。

任何一个完整的 ControlNet 流程，都强制要求解耦为两个配套组件：

1. 预处理器 (Preprocessor) —— 负责“解析”： 就像是一个数据清洗脚本。你丢给它一张真实的真人照片，它会把衣服、颜色、光影全部过滤掉，只提取出纯粹的“特征映射图”（比如一张黑底彩线的火柴人骨架图或灰度深度图）。
2. 控制模型 (Control Model) —— 负责“拦截与注入”： 这是一个 `.safetensors` 模型文件。它拿着预处理器提取出的“映射图”，在 `KSampler` 进行潜空间计算时强行注入约束，告诉 AI：“左手手腕的像素点必须生成在这个坐标上”。

ControlNet 家族有十几种模型，但对于“阶段二”的二次元创作，掌握以下两个就覆盖了 90% 的需求：

| 控制类型            | 预处理器提取的内容                         | 核心应用场景                                                                   | 约束强度             |
| :------------------ | :----------------------------------------- | :----------------------------------------------------------------------------- | :------------------- |
| **OpenPose (骨骼)** | 18 到 133 个关节点坐标（四肢、手指、面部） | 完美复刻真人的动作（如跳舞、打斗、**骑摩托车**）。它完全无视原图的胖瘦和衣服。 | 只锁姿态，画风最自由 |
| **Depth (深度图)**  | 距离镜头的远近关系（越近越白，越远越黑）   | 还原照片的 3D 空间层次感，或者强行保持某个复杂物体的轮廓。                     | 锁定了整体的空间结构 |

---

## 部署双拦截器架构 (OpenPose + Depth)

### 1. 拉取 ControlNet 控制模型 (后端拦截服务)

既然我们用的是 NoobAI (SDXL 架构)，就必须用专门为 XL 训练的控制模型。请回到你的 Jupyter Lab 终端，执行以下命令：

```bash
# 进入 ControlNet 专属挂载目录
cd /workspace/runpod-slim/ComfyUI/models/controlnet/

# 极速拉取公认最稳的 Thibaud 版 OpenPose XL
wget -c -O thibaud_xl_openpose.safetensors "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/thibaud_xl_openpose.safetensors"

# 拉取 diffusers 官方的满血版 Depth XL 控制模型
wget -c -O diffusers_xl_depth_full.safetensors "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/diffusers_xl_depth_full.safetensors"
```

### 2. 安装预处理器插件 (数据清洗中间件)

默认的 ComfyUI 无法直接“看懂”你骑摩托车的照片，我们需要安装视觉解析器代码库。

1.  在 ComfyUI 界面点击右上角的 **Manager** 按钮。
2.  点击 **Custom Nodes Manager**。
3.  在搜索框输入： `comfyui_controlnet_aux`。
4.  找到列表中的 **ComfyUI's ControlNet Aux Preprocessors**（作者是 Fannovel16），点击 **Install**。
5.  安装完成后，点击界面提示的 **Restart** 重启 ComfyUI 服务。

### 3\. 挂载预处理器底层数据库 (【关键防坑】绕过安全沙箱)

> **⚠️ 警告：** 近期 ComfyUI 升级了“零信任安全沙箱”。如果你跳过此步直接运行，系统会发现插件试图在后台偷偷下载模型，从而触发熔断报错 (`Queue was blocked`)。**我们必须提前把底层依赖下载到官方白名单目录。**

打开 Jupyter Lab 终端，执行以下命令，强制物理对齐依赖：

```bash
# 1. 创建并进入官方标准的预处理器依赖目录
mkdir -p /workspace/runpod-slim/ComfyUI/models/annotators/
cd /workspace/runpod-slim/ComfyUI/models/annotators/

# 2. 拉取“雷达侦察兵” YOLOX 模型 (负责全图找人)
wget -c -O yolox_l.onnx "https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx"

# 3. 拉取“解剖专家” DWPose 核心计算模型 (负责精准提骨骼)
wget -c -O dw-ll_ucoco_384_bs5.torchscript.pt "https://huggingface.co/hr16/DWPose-TorchScript-BatchSize5/resolve/main/dw-ll_ucoco_384_bs5.torchscript.pt"
```

_(注：下载完成后，务必在 ComfyUI 网页按 `F5` 刷新，让后端重新扫描挂载目录。)_

### 4. 架构拓扑重构 (双切面注入)

在工作区空白处左键双击打开搜索框，添加以下 5 个新节点：

1.  **Load Image** (加载图像)：上传那张作为测试用例的骑摩托车照片。
2.  **DWPreprocessor**（或 DWPose Estimator）：最强骨架提取器。
3.  **Zoe-DepthMapPreprocessor**：最强空间深度提取器（边缘切割最干净）。
4.  **Load ControlNet Model** (加载控制模型)：添加 **两个**。
    - 模型 A：选择 `thibaud_xl_openpose.safetensors`
    - 模型 B：选择 `diffusers_xl_depth_full.safetensors`
5.  **Apply ControlNet** (应用控制网)：添加 **两个**，用来做链式拦截。

### 5. 连线重构逻辑 (Chain of Responsibility)

这套数据流遵循 “预处理各干各的，拦截器串联执行” 的责任链模式。

**【前端预处理并联】**

1.  将原图 `Load Image` 的 `IMAGE` 连入 -\> `DWPreprocessor` 的 `image`。
2.  将原图 `Load Image` 的 `IMAGE` 连入 -\> `Zoe Depth Map` 的 `image`。

**【注入控制模型】**

3. 将 `Load ControlNet Model (OpenPose)` 的 `CONTROL_NET` 连入 -\> `Apply ControlNet 1` 的 `control_net`。
4. 将 `Load ControlNet Model (Depth)` 的 `CONTROL_NET` 连入 -\> `Apply ControlNet 2` 的 `control_net`。
5. 将骨架图 `DWPreprocessor` 的 `IMAGE` 连入 -\> `Apply ControlNet 1` 的 `image`。
6. 将深度图 `Zoe Depth Map` 的 `IMAGE` 连入 -\> `Apply ControlNet 2` 的 `image`。

**【串联核心拦截器网关】**

7. 找到你原有的正向/负向 `CLIP Text Encode` 节点，**断开**它们原本直接连向 `KSampler` 的那根桔色线。
8. **正向提示词链路：** 正向 CLIP 的 `CONDITIONING` -\> 连入 `Apply ControlNet 1` 的 `positive` -\> 从 `Apply ControlNet 1` 输出的 `positive` 连入 `Apply ControlNet 2` 的 `positive` -\> 最终连入 `KSampler` 的 `positive`。
9. **负向提示词链路：** 负向 CLIP 的 `CONDITIONING` -\> 连入 `Apply ControlNet 1` 的 `negative` -\> 从 `Apply ControlNet 1` 输出的 `negative` 连入 `Apply ControlNet 2` 的 `negative` -\> 最终连入 `KSampler` 的 `negative`。

---

## 高级生产环境调优 (解决塑料感与特征污染)

如果直接运行上述配置，大概率会生成“塑料透明摩托车”或“机甲脸怪胎”。这是因为双重约束导致了严重的**渲染算力挤兑**和**全局变量污染**。我们必须在参数层进行“依赖隔离”。

### 6. 参数重载与生命周期控制 (Early Stopping)

在最新版的 ComfyUI 中，`Apply ControlNet` 节点原生集成了介入与退场机制。我们需要让深度图“提前退场”，把最后 35% 的算力还给 LoRA 去渲染真实材质。

- **节点 A (负责 OpenPose 姿态)：**
  - `strength`: **1.0**
  - `start_percent`: 0.0
  - `end_percent`: **1.0** _(全程锁死，坚决防止 AI 在最后阶段“自作主张”导致歪头或耳朵变形)_
- **节点 B (负责 Depth 深度/摩托车)：**
  - `strength`: **0.9**
  - `start_percent`: 0.0
  - `end_percent`: **0.65** _(关键！在 65% 进度时让深度图下线，只保留车体轮廓，丢弃其附带的“灰色塑料感”)_

### 7. 提示词作用域隔离 (防污染策略)

为了让摩托车拥有金属质感，我们通常会加入高权重的 `metallic paint`（金属烤漆）。但在全局提示词下，这会导致卡提希娅的脸也被渲染成赛博金属。必须进行强制的“类型隔离”：

**正向提示词 (Positive Prompt) 注入材质对冲：**

> 明确给机车加金属，给人物加血肉布料。

```
black heavy motorcycle, metallic paint, chrome engine reflections, realistic mechanical details, (soft white fabric beret:1.3), (soft human skin, organic, beautiful detailed face:1.2), knitted sweater texture
```

**负向提示词 (Negative Prompt) 精准拉黑：**

> 杜绝深度图残留的透明感和金属词的越界污染。

```
transparent, glass, plastic, gray monochrome, robot, cyborg, metallic face, metallic hat, mecha, robot ears, deformed face, bad anatomy
```

### 8. 运行验证

完成生命周期控制与作用域隔离后，点击 **Run** (Queue Prompt)。

后台会依次调用 YOLOX 抠图、DWPose 算骨架、Zoe 算深度空间。在生成的前 65% 步数中，空间被严格锁定；在最后的 35% 步数中，限制解除，V5 LoRA 全功率介入，最终生成一幅既完美复刻姿态，又兼具重机车金属感与二次元旗舰唯美画风的完美图像。
