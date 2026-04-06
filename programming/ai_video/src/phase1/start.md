# 生成第一张图片

### 1. 进入 JupyterLab 终端

1. 在 AutoDL 控制台的“容器实例”页面，找到你刚开机的 RTX 5090 实例。
2. 点击右侧的 JupyterLab 快捷入口。这会打开一个类似完整操作系统的网页界面。
3. 在 JupyterLab 界面中，点击左上角的蓝色加号按钮，新建一个 Terminal（终端）。

### 2. 下载模型

```sh
# 大模型（Checkpoint）必须严格存放在特定的文件夹下 ComfyUI 才能识别
cd /root/ComfyUI/models/checkpoints/
# 下载 AWPainting 大模型（这是目前二次元、泛二次元质感最好的基底模型）
wget -O AWPainting.safetensors https://huggingface.co/jzli/AWPainting/resolve/main/AWPainting_v1.2.safetensors
# 国内用这个下载
wget -O AWPainting.safetensors https://hf-mirror.com/sam749/AWPainting-v1-2/resolve/main/awpainting_v12.safetensors
```

### 3. 确认并启动 ComfyUI 服务

```sh
cd /root/ComfyUI
# 启动服务（AutoDL 平台默认只对外部映射 6006 端口，这点非常关键）
python main.py --listen 127.0.0.1 --port 6006
```

等待几秒钟，如果终端里没有报错，并且输出了类似 `To see the GUI go to: http://127.0.0.1:6006` 的字样，说明底层引擎已经成功跑起来了！

### 4. 打开图形化操作界面

1. 服务启动后，不要关掉这个终端网页。
2. 切回到 AutoDL 的控制台管理页面。
3. 在你的实例所在行，点击 “自定义服务” 这个按钮。
4. 平台会自动为你生成一个内网穿透的访问链接，点击后，就会在一个新标签页打开 ComfyUI 的全屏节点界面。

### 5. 操作界面说明

当你看到满屏连线的节点时不要慌。这其实就是一个标准的有向无环图 (DAG) 任务流，数据从左向右流动：

- Load Checkpoint（Checkpoint 加载器）：这是整个流的起点，负责把几 GB 的权重文件加载进你 5090 的显存里。
- CLIP Text Encode（CLIP 文本编码）：有两个框，一个框填正向提示词（你想要的画面，比如 1girl, beautiful, cinematic lighting），另一个框填反向提示词（你不想要的，比如 ugly, bad anatomy）。
- KSampler（K采样器）：这是算力消耗的核心节点，它负责根据你的文本，一步步去噪生成图像。
- Save Image（保存图像）： 渲染出的最终结果。

你可以顺着这两个 CLIP 文本编码节点右侧黄色的 条件 (CONDITIONING) 输出点，沿着连线往右看，一直看到 K采样器 (KSampler) 节点：

- 上面的节点：它的线连到了 K采样器的 正向条件 (positive) 接口。所以它就是正向提示词。
- 下面的节点： 它的线连到了 K采样器的 负面条件 (negative) 接口。所以它就是反向提示词。

这就是 ComfyUI 作为节点式工作流最核心的逻辑——完全靠连线（数据的流向）来决定。

### 6. 生成图片

1. 手动绑定大模型
   1. 找到最左侧的 Checkpoint加载器 节点。
   2. 看到里面写着 v1-5-pruned-emaonly-fp16.safetensors 的输入框了吗？点击它。
   3. 在弹出的下拉菜单中，选择你刚才下载好的 AWPainting.safetensors。
   4. 确保节点里的文本已经成功刷新为新模型。
2. 输入提示词
   1. 正向提示词： (masterpiece, best quality:1.2), 1girl, solo, Cartethyia, long blonde hair, elf ears, bright blue eyes, blue mark on forehead, wearing a white beret, white knit sweater, scarf, plaid skirt, highly detailed face, sweet smile, looking at viewer, walking on a night street, bokeh, cinematic lighting, anime style, unreal engine 5 render
   2. 反向提示词： (worst quality, low quality:1.4), bad anatomy, bad hands, missing fingers, text, watermark, error, cropped, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, monochrome
3. 直接点击屏幕正下方那个蓝色的 “运行” (Run / Queue Prompt) 按钮。

点击之后，你会看到界面上的节点开始依次亮起一圈绿色的边框。这代表程序执行的进度，完美展示了底层的运作逻辑：

1. Checkpoint 加载器： 绿框首先亮在这里。此时，系统正在将几 GB 的基础大模型从硬盘加载到你那张 RTX 5090 的显存里。这就像服务启动时预热缓存。
2. CLIP 文本编码： 接着亮起。它将你写的正向提示词和反向提示词转化为 AI 能理解的数学向量。
3. 空 Latent 图像： 分配一块 512x512 大小的初始“画布”内存。
4. K 采样器： 绿框会在这里停留最久，上面还会有一个进度条。这是真正消耗算力的地方，AI 正在根据你的文本提示，一步步从噪点中“雕刻”出画面。
5. VAE 解码 & 保存图像： 算完之后，将底层张量数据反序列化为人类能看懂的像素点，并显示在最右侧的节点上。
