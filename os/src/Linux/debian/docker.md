# Docker

### 1. 卸载旧版本（可选）

```sh
sudo apt-get remove docker docker-engine docker.io containerd runc
```

注：如果提示未找到这些包，说明你的系统很干净，直接进入下一步即可。

### 2. 设置 Docker 官方软件源

更新包索引并安装必要的依赖工具，确保 apt 可以通过 HTTPS 安全地下载：

```sh
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg -y
```

添加 Docker 官方的 GPG 密钥：

```sh
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

将 Docker 官方源添加到系统的源列表中：

```sh
sudo echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 3. 安装 Docker Engine

```sh
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

### 4. 验证安装

```sh
sudo docker run hello-world
```

如果终端打印出带有 "Hello from Docker!" 的欢迎信息，就说明安装大功告成了！

## docker-compose 的坑

新老版本的命令差异：

- 老版本 (V1): 命令是带有连字符的 `docker-compose`。它是用 Python 写的独立程序。
- 新版本 (V2): 命令变成了空格分隔的 `docker compose`。它是用 Go 语言重写的，官方现在推荐将其作为 Docker CLI 的一个插件 (Plugin) 来安装。

## docker hub 镜像

[DockerHub 国内加速镜像列表](https://github.com/dongyubin/DockerHub?tab=readme-ov-file)

```sh
vim /etc/docker/daemon.json
```

将以下内容复制并粘贴到文件中。这里我为你整理了几个目前（相对）还可以使用的公共镜像源：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://proxy.vvvv.ee",
    "https://dockerproxy.net",
    "https://dockerproxy.link",
    "https://docker.m.daocloud.io"
  ]
}
```

重启 Docker 服务使配置生效

```sh
systemctl daemon-reload
systemctl restart docker
```
