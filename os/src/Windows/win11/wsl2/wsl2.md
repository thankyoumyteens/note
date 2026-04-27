# 安装 WSL2

安装 WSL2 和 Ubuntu 现在非常简单，微软已经将整个过程简化为了一条命令。以下是最快捷的安装步骤：

### 第一步：以管理员身份打开 PowerShell

1. 点击 Windows 开始菜单。
2. 搜索 **PowerShell**。
3. 右键点击“Windows PowerShell”，选择**“以管理员身份运行”**。

### 第二步：执行安装命令

在弹出的 PowerShell 窗口中，输入以下命令并按回车：

```powershell
wsl --install
```

_💡 说明：这条命令会自动启用所需的 Windows 功能（如虚拟机平台），下载最新的 Linux 内核更新包，并**默认安装 Ubuntu 发行版**。_

### 第三步：重启电脑

命令执行完成后，系统会提示你重启计算机。请保存好手头的工作并**重启电脑**，以便让 WSL2 的核心组件生效。

### 第四步：设置 Ubuntu 账号和密码

1. 重启后，通常会自动弹出一个 Ubuntu 的终端窗口，显示正在进行最后的安装（这可能需要几分钟）。
2. 安装完成后，它会提示你创建一个 UNIX 用户名（`Enter new UNIX username:`）。这个名字不需要和你 Windows 的用户名一样。
3. 接着输入密码并确认（输入密码时屏幕上不会显示任何字符，这是正常的 Linux 安全机制，直接输入并按回车即可）。

---

### 验证与进阶配置

**1. 检查是否成功运行在 WSL 2 版本上**
打开 PowerShell，输入：

```powershell
wsl -l -v
```

如果你看到 `Ubuntu` 且后面的 `VERSION` 是 `2`，那就大功告成了！

**2. （可选）如果你想安装特定版本的 Ubuntu（如 22.04 或 24.04）**
如果你的电脑之前已经启用了 WSL，单纯输入 `wsl --install` 可能不会触发新的下载。你可以用以下命令查看可用的版本：

```powershell
wsl --list --online
```

然后指定版本安装，例如：

```powershell
wsl --install -d Ubuntu-22.04
```
