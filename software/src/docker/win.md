# Windows 安装 Docker

### 1. 安装 WSL

1. 访问 [WSL GitHub Releases](https://github.com/microsoft/WSL/releases) 页面。
2. 找到 v2.6.3 版本（或最新稳定版），在 Assets 栏下下载对应的安装包：
   - 如果你是普通电脑，下载：wsl.2.6.3.x64.msi
   - 如果你是 ARM 笔记本（如 Surface Pro 9 ARM），下载：wsl.2.6.3.arm64.msi
3. 下载完成后，直接双击运行安装。
4. 安装完后重启电脑，运行 `wsl --version` 确认版本。

### 2. 下载并安装 Docker Desktop

1. 访问 [Docker 官网下载页面](https://www.docker.com/products/docker-desktop/)。
2. 点击 "Download for Windows"。
3. 运行安装包，确保勾选了 "Use WSL 2 instead of Hyper-V"（默认通常已勾选）。
4. 安装完成后，根据提示重启电脑或注销登录。

### 3. 全局代理配置

1. 打开 Docker Desktop 界面，点击右上角的 Settings (齿轮图标)。
2. 在左侧菜单选择 Resources > Proxies。
3. 打开 Manual proxy configuration 开关。
4. 在 Web Proxy (HTTP) 和 Secure Web Proxy (HTTPS) 中填入你的代理地址。
   - 注意： 如果你的代理软件运行在本地，地址通常是 http://127.0.0.1:端口号。
   - 关键点： 由于 Docker 运行在 WSL 2 虚拟化环境中，有时 127.0.0.1 可能无法直接访问宿主机。如果失败，可以尝试使用 http://host.docker.internal:端口号。
5. 在 Bypass proxy settings for these hosts 中，确保保留默认的 localhost,127.0.0.1，防止访问本地服务也走代理。
6. Containers Proxy 选择 Same as host proxy
7. 点击 Apply & Restart。

### 4. 运行一个测试容器

```sh
docker run hello-world
```
