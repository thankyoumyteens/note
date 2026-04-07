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
