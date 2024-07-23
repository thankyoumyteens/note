# UTM 安装 Win11Arm

1. 下载 Win11Arm: magnet:?xt=urn:btih:64fb7c011f407628471432d8cd52b2b5c6c52673&dn=SW_DVD9_Win_Pro_11_23H2_Arm64_ChnSimp_Pro_Ent_EDU_N_MLF_X23-59518.ISO&xl=7142125568

2. UTM -> + -> Virtualize -> Windows -> 勾选 Install Windows 10 or higher 和 Install drivers and SPICE tools, 选择镜像 -> continue -> 一路下一步

3. 开机 -> 在倒计时结束前, 按任意健开始安装

4. 安装, 跳过联网: `Shift + F10` -> `oobe\bypassnro`

5. 安装完成后关闭虚拟机, 设置 -> CD/DVD -> 清除 iso 镜像挂载, 否则进不去系统

6. 等待 gust-tools 下载完成

7. 开机, 安装 gust-tools

## 共享文件夹, 错误 Ox80O700DF:  文件大小超出允许的限制, 无法保存。

修改注册表

```
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WebClient\Parameters]

"FileSizeLimitInBytes"=dword:ffffffff
```

重启。
