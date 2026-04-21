# 小脸崩坏定律

如果在正向提示词的开头加上 `(full body shot:1.3), from head to toe, standing on ground, ` 来生成一张包含全身的图片，那么生成的图片就会出现一个问题：人物的脸会变丑。这就是AI 绘图界最臭名昭著的 “小脸崩坏（Small Face Collapse）”定律。

当你生成“半身像”时，卡提希娅的脸分配到了大约 512x512 的像素矩阵，大模型有充足的“算力带宽”去雕刻她的蓝眼睛、声痕和五官比例。
但当你加上 `full body`（全身）后，画面必须容纳她的腿和脚，她的脸在 832x1216 的画布上被急剧压缩到了只有大约 64x64 甚至更小的像素区域。在这么低的像素密度下，大模型根本画不清精细的特征，眼睛就会变成两个黑点，五官就会挤在一起，直接变成“歪瓜裂枣”。

### 1. 安装插件

1. 呼出包管理器 (ComfyUI Manager)
   - 在 ComfyUI 网页界面的右侧控制面板，点击 Manager 按钮。（如果你选的 RunPod 镜像自带了 Manager 的话）。
   - 点击 Install Custom Nodes (安装自定义节点)。
2. 搜索并安装核心组件
   - ComfyUI Impact Pack, 作者是 Dr.Lt.Data
   - ComfyUI Impact Subpack, 作者是 Dr.Lt.Data

### 2. 重启与依赖加载

1. **硬重启后端**
   - 插件安装完成后，切记**不能**只按 F5 刷新网页。必须点击 Manager 底部的 `Restart` 按钮，或者在终端直接重启 ComfyUI 的 Python 进程。
   - 重启完成后，刷新浏览器页面。
2. **确认环境依赖**
   - Impact Subpack 强依赖 `ultralytics` 库。如果在 RunPod 等虚拟环境中找不到节点，需进入对应环境执行 `pip install ultralytics`。

### 3. 构建自动修复微服务 (节点部署)

回到生图管线，在最终输出图片前（`VAE Decode` 和 `Save Image` 之间）强行插入这套修复中间件。

1. **添加目标检测器 (YOLO)**
   - 双击空白处，搜索并添加 **`UltralyticsDetectorProvider`** 节点（由 Impact Subpack 提供）。
   - 在 `model_name` 下拉菜单中，选择 **`bbox/face_yolov8m.pt`**（如果没有，去 Manager 的 `Install Models` 里搜索 `face yolo` 下载）。
2. **添加面部重绘引擎**
   - 搜索并添加 **`FaceDetailer`** 节点。

### 4. 节点连线指南 (数据流向)

将 `FaceDetailer` 接入现有的生图管线，确保它能拿到所有的上下文数据：

- `image` ← 连入 `VAE Decode` 输出的（脸部崩坏的）全身图。
- `model` ← 从前面的 LoRA 节点拉入。
- `clip` ← 从 LoRA 节点拉入。
- `vae` ← 从 `Load Checkpoint` 拉入。
- `positive` ← 连入正向提示词 `CLIP Text Encode`。
- `negative` ← 连入反向提示词 `CLIP Text Encode`。
- `bbox_detector` ← 连入刚才创建的 **`UltralyticsDetectorProvider`** 的输出端。
- 终点：将 `FaceDetailer` 最上方的 `image` 输出连入最终的 **`Save Image`**。

### 5. 核心参数调优 (决定修复生死的关键)

修改 `FaceDetailer` 节点的以下参数：

- **`guide_size` (重绘分辨率)**：设为 **`512`**。这代表模型把脸部框出来后，放大到 512x512 的超清画布上进行雕刻。
- **`steps` (采样步数)**：保持与基础生图(`KSampler`)一致（如 `30`）。
- **`sampler_name` / `scheduler`**：保持与基础生图(`KSampler`)一致（如 `euler` / `normal`）。
- **`denoise` (重绘幅度 - 核心红线)**：
  - **必须限制在 `0.35` 到 `0.45` 之间**（建议首选 `0.4`）。
  - _原理解释_：设为 1.0 会导致 AI 完全无视原图，在脖子上画出一个完全陌生的人（甚至怪物）；设得太低（<0.3）则无法挽救崩坏的像素。0.4 能在保留角色原有轮廓和发型的基础上，为五官注入极致的清晰度。

### 6. 运行与验证

点击 `Run` 启动管线。

1. 系统会先正常渲染出一张小脸崩坏的全身图。
2. 进度条会停留在 `FaceDetailer` 节点。此时 YOLO 算法正在扫描图像，精准锁定脸部坐标（Bounding Box）。
3. 系统在后台自动执行第二次微型渲染，最后将高清五官无缝缝合回原图。
4. 最终输出一张拥有完整物理空间（包含腿脚）且脸部如特写般精致的“真理底图”。

利用你本地 RTX 5090 强大的算力（或 RunPod 云端资源）开始疯狂抽卡，直到抽出那张没有任何结构崩坏、材质光影完美、让你一眼惊艳的“真理源”底图（Base_Texture_Map）。

当你抽到这张完美的定妆照时，我们就以此为基石，正式进军原生视频大模型环节。
