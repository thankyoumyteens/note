# ControlNet

在前面，我们通过写提示词和挂载 LoRA 来画图。这就像是在对 AI 提 **业务需求** ：“给我画一个戴贝雷帽的女孩”。至于她具体怎么站、手放在哪里，AI 内部的黑盒充满了随机性。

用 Java 后端的思维来理解：如果说 LoRA 像是一个 AOP（面向切面编程）的拦截器，负责在底层模型上注入“卡提希娅”的风格和材质；那么 ControlNet 就是一个极其严苛的 Interface（接口约束）。它会拦截进入 KSampler 的数据流，强行要求生成的像素在空间拓扑上必须 100% 吻合你提供的骨架或深度图。

我们可以直接拿一张骑摩托车的照片作为“测试用例”（Test Case）。让 AI 提取骑车时的硬核姿势，然后把卡提希娅完美地“嵌”进这个姿势里。

**ControlNet 就是那个强制的“结构校验器 (Schema Validator)”。** 它剥夺了 AI 在空间构图上的自由发挥权，强制要求生成的像素必须严格吻合你提供的底层拓扑结构。

任何一个完整的 ControlNet 流程，都强制要求解耦为两个配套组件：

**1. 预处理器 (Preprocessor) —— 负责“解析”** 就像是一个数据清洗脚本。你丢给它一张真实的真人照片，它会把衣服、颜色、光影全部过滤掉，只提取出纯粹的“特征映射图”（比如一张黑底彩线的火柴人骨架图）。
**2. 控制模型 (Control Model) —— 负责“拦截与注入”** 这是一个 `.safetensors` 模型文件。它拿着预处理器提取出的“火柴人图”，在 `KSampler` 进行潜空间计算时强行注入约束，告诉 AI：“左手手腕的像素点必须生成在这个坐标上”。

ControlNet 家族有十几种模型，但对于“阶段二”的二次元创作，掌握以下两个就覆盖了 90% 的需求：

| 控制类型            | 预处理器提取的内容                         | 核心应用场景                                                                   | 约束强度             |
| :------------------ | :----------------------------------------- | :----------------------------------------------------------------------------- | :------------------- |
| **OpenPose (骨骼)** | 18 到 133 个关节点坐标（四肢、手指、面部） | 完美复刻真人的动作（如跳舞、打斗、**骑摩托车**）。它完全无视原图的胖瘦和衣服。 | 只锁姿态，画风最自由 |
| **Depth (深度图)**  | 距离镜头的远近关系（越近越白，越远越黑）   | 还原照片的 3D 空间层次感，或者强行保持某个复杂物体的轮廓。                     | 锁定了整体的空间结构 |

## 使用 OpenPose

### 1. 拉取 ControlNet 控制模型 (后端服务)

既然我们用的是 NoobAI (SDXL 架构)，就必须用专门为 XL 训练的控制模型。请回到你的 Jupyter Lab 终端，执行以下命令，把 OpenPose 模型直接拉取到对应目录：

```sh
# 进入 ControlNet 专属挂载目录
cd /workspace/runpod-slim/ComfyUI/models/controlnet/

# 极速拉取公认最稳的 Thibaud 版 OpenPose XL
wget -c -O thibaud_xl_openpose.safetensors "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/thibaud_xl_openpose.safetensors"

# 确保在 ControlNet 模型目录
cd /workspace/runpod-slim/ComfyUI/models/controlnet/

# 拉取 diffusers 官方的满血版 Depth XL 控制模型
wget -c -O diffusers_xl_depth_full.safetensors "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/diffusers_xl_depth_full.safetensors"
```

### 2. 安装预处理器节点 (数据清洗中间件)

默认的 ComfyUI 无法直接“看懂”你骑摩托车的照片，我们需要安装一个视觉解析器，把照片变成纯粹的骨骼数据。

1. 在 ComfyUI 界面点击右上角的 Manager 按钮（如果没有弹出菜单，可能需要刷新一下页面）。
2. 点击 Custom Nodes Manager。
3. 在搜索框输入：comfyui_controlnet_aux
4. 找到列表中的 comfyui_controlnet_aux 插件（作者是 Fannovel16），点击 Install。
5. 安装完成后，点击界面提示的 Restart 重启 ComfyUI 服务。

### 3. 架构拓扑重构 (切面注入)

重启完成后，我们要在原来的工作流上，强行插入这个拦截器。在空白处左键双击就可以打开搜索框，添加以下 4 个新节点：

1. Load Image (加载图像)：用来上传那张骑摩托车的照片。
2. DWPreprocessor（或者叫做 DWPose Estimator）：目前最强的 OpenPose 预处理器，能精准捕捉身体和手指动作。
3. Load ControlNet Model (加载控制模型)：要添加两个
   - Load ControlNet Model 1：选出我们刚下载的 thibaud_xl_openpose.safetensors。
   - Load ControlNet Model 2：选出我们刚下载的 diffusers_xl_depth_full.safetensors。
4. Apply ControlNet (应用控制网)：也要添加两个
   - Apply ControlNet 1
   - Apply ControlNet 2
5. Zoe Depth Map

### 4. 连线重构逻辑 (The Wiring)

1. Load Image：上传骑摩托车的照片。
2. Load Image 的 IMAGE 连入 -> DWPose Estimator 的 image。
3. Load Image 的 IMAGE 连入 -> Zoe Depth Map 的 image。
4. 将 DWPose Estimator 输出的 IMAGE 连入 -> Apply ControlNet 1 的 image。
5. 将 Zoe Depth Map 输出的 IMAGE 连入 -> Apply ControlNet 2 的 image。
6. Load ControlNet Model 1 的 CONTROL_NET 连入 -> Apply ControlNet 1 的 control_net。
7. Load ControlNet Model 2 的 CONTROL_NET 连入 -> Apply ControlNet 2 的 control_net。
8. 找到你原有的正向 CLIP Text Encode 节点。断开它直接连向 KSampler 的那根桔色线（在 KSampler 的 positive 端点把线拖到空白处）。
9. 将正向 CLIP 的 CONDITIONING 连入 -> Apply ControlNet 1 的 positive。
10. 将 Apply ControlNet 1 输出的 positive 连入 -> Apply ControlNet 2 的 positive
11. 将 Apply ControlNet 2 输出的 positive 连入 -> KSampler 的 positive。
12. 找到你原有的负向 CLIP Text Encode 节点。断开它直接连向 KSampler 的那根桔色线。
13. 将 负向 CLIP 输出的 CONDITIONING 连入 -> Apply ControlNet 1 的 negative。
14. 将 Apply ControlNet 1 的 negative 连入 -> Apply ControlNet 2 的 negative。
15. 将 Apply ControlNet 2 输出的 negative 连入 -> KSampler 的 negative。

### 5. 运行
