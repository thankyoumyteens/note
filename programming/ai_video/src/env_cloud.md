# 云环境搭建

1. 打开 RunPod 平台：[https://console.runpod.io](https://console.runpod.io)
2. 注册 -> 绑卡 -> 充值
3. 左侧菜单栏：Resources -> Pods
4. Featured GPUS -> 选择 RTX 5090 -> 页面会自动向下滚动到 Configure deployment
5. 点击右上角的 Change Template 按钮 -> 在搜索框里输入 ComfyUI -> 选择由 runpod 维护的官方镜像（通常名字就叫 ComfyUI）
6. 选好 ComfyUI 模板后，点击旁边的 Edit，找到 Volume Disk 选项 -> 手动改为 100GB
7. 保持选中左侧的 On-Demand（$0.89/hr），虽然 Spot 便宜，但 Spot 随时会被别人“抢占”关机，作为我们调试环境的初期，不要为了省这点钱让工作流还没保存就断电
8. 配置好后点击底部的 Deploy
9. 当 Pod 显示为 Running 状态时，点击 JupyterLab 即可打开 Jupyter Notebook

## 创建 Network Volume

虽然 Network Volume（网络卷）的读写速度比本地盘稍慢一点点，但它实现了真正的“存算分离”：如果 5090 被抢了，你可以瞬间把这个 100GB 的网络盘挂载到另一台有空闲卡的机器上点火启动。

注意，存算分离架构里有一个硬性物理约束：你的数据盘放在哪个机房，你以后就只能租用那个机房里的显卡。

1. 点击左侧菜单栏的 Storage，然后点击中间的 Create Network Volume +
2. 选中机房卡片（例如 EUR-NO-1）后，继续往下滚动页面：
   - Name: 填入 comfyui-data（或者任何你喜欢的标识）
   - Size: 依然稳稳地填上 100 GB
3. 点击最底部的 Create
4. 创建成功后，回到左侧的 Pods 菜单，点击 + Deploy
5. 选一台对应机房里的 RTX 5090
6. 模板选 RunPod ComfyUI
7. 核心操作： 在配置页面的底部，展开网络存储的选项，把刚刚创建的 comfyui-data 挂载上去

## 切换机器

1. 当你打算更换显卡（比如从 5090 换成性价比更高的 4090）时，直接在 Pods 页面点击 Terminate
   - 请放心： Terminate 只会销毁显卡和它的临时系统盘，挂载在其上的 Network Volume 会自动“松开”并保持在原地，数据完好无损
2. 点击 + Deploy 按钮，选择你想用的新显卡。注意：必须选择与你 Network Volume 相同的机房（例如 EUR-NO-1）
3. 在部署页面的底部，你会看到 Network Volume 选项。点击下拉菜单，选中你之前的那个 comfyui-data 即可
4. 点火启动后，你会发现 /workspace 目录下所有的模型、插件和之前的下载记录全都原封不动地在那儿
