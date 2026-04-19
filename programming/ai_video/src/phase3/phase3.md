# 阶段三：原生 DiT 视频生成

### 1. 安装插件

1. 呼出包管理器 (ComfyUI Manager)
   - 在 ComfyUI 网页界面的右侧控制面板，点击 Manager 按钮。（如果你选的 RunPod 镜像自带了 Manager 的话）。
   - 点击 Install Custom Nodes (安装自定义节点)。
2. 搜索并安装核心组件
   - ComfyUI-MimicMotionWrapper, 作者是 Kijai

### 2. 节点部署

请在 ComfyUI 的画布上（建议新建一个干净的 Group 或者工作区）严格按照以下架构进行连线：

1. 注入核心输入源 (Input Ingestion)
   - **底图输入**：添加 `Load Image` 节点，导入你刚才通过 FaceDetailer 修复完毕的、包含完美脸部和完整双腿的卡提希娅全身图。
   - **骨架输入**：添加 `Load Video (Upload) 🎥🅥🅗🅢` 节点，导入你之前提取好的纯黑底色、彩色线条的火柴人视频。
2. 配置“尺寸归一化拦截器” (Resolution Normalization): 为了彻底防止我们之前踩过的张量对齐崩溃（27 vs 28 报错），必须在数据进入大模型前进行强制拦截。
   - 添加**两个** `Upscale Image` 节点。
   - 将两个节点的参数统一焊死为：`width`: **576**, `height`: **1024**, `crop`: **center**, `upscale_method`: **bilinear**。
   - **连线**：将底图的 `IMAGE` 和骨架视频的 `IMAGE`，分别连入这两个节点的输入端。
3. 加载 DiT 视频计算图 (Context Object)
   - 添加 `(Down)Load MimicMotionModel` 节点。
   - 保持默认参数，它会自动把几十 GB 的权重读入内存，并输出一条紫色的 `mimic_pipeline`（胖上下文对象）。
4. 点燃时序采样大熔炉 (The Core Sampler)
   - 添加 `MimicMotion Sampler` 节点。
   - **物理连线**：
     - `mimic_pipeline` ← 接入第三步的输出。
     - `ref_image` ← 接入**底图**对应的那个 `Upscale Image` 输出。
     - `pose_images` ← 接入**骨架**对应的那个 `Upscale Image` 输出。
   - _(这个节点会接管你的算力，在潜空间内进行疯狂的降噪推演，输出 `samples`)_。
5. 反序列化与 MP4 压制 (Decode & Encode)
   - 添加 `MimicMotion Decode` 节点。
     - `samples` ← 接入 Sampler 的输出。
     - `mimic_pipeline` ← 接入最前面的加载器。
     - _(这一步打破次元壁，将潜空间张量翻译回可见的 `IMAGE` 像素矩阵)_。
   - 添加 `Video Combine 🎥🅥🅗🅢` 节点。
     - 接入 Decode 出来的 `IMAGE` 流。
     - 设置帧率（与你的原版动作视频保持一致，通常为 24 或 30），格式选择 `video/h264-mp4`。

整套架构搭建完毕后，检查一遍有没有漏连的线缆，然后果断点击界面上的 **Run** 按钮。
