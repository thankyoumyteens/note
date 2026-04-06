# 云环境搭建

1. 打开 AutoDL 平台：[https://www.autodl.com/home](https://www.autodl.com/home)
2. 进入“算力市场”。对于视频生成（尤其是后续要跑 AnimateDiff 和 ControlNet），24GB 显存是底线配置。
   - 显卡： RTX 5090
3. 不要从零开始配置 Python 虚拟环境和 CUDA 驱动，那会浪费大量时间。在创建实例时，选择 **“社区镜像”**。
   - 在搜索框输入 ComfyUI。
   - 选择一个下载量高、更新日期较新的镜像。这里选择：tzwm_ComfyUI
   - 镜像版本选择 v21
4. 购买并开机
5. 用完记得关机，一小时大概 2-4 块钱
