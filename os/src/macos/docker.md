# Docker

由于 macOS 底层不是 Linux，任何在 Mac 上运行的 Docker 都必须在后台跑一个 Linux 虚拟机（VM）。这就是为什么它在闲置时依然会消耗 CPU、内存和电池电量的根本原因。

Colima 是一个基于命令行的工具，它的核心理念就是按需启动：它在后台运行一个极度精简的 Linux 虚拟机（基于 Lima），并且完美接管 Docker CLI。

## 环境准备与安装

```sh
brew install colima docker docker-compose
```

## 日常基础操作（用时开，不用时关）

### 启动 Colima (启动 Docker 环境)：

首次启动需要下载虚拟机镜像，可能需要一两分钟，之后基本是秒开。

```sh
colima start
```

启动后，您就可以完全像以前一样使用 docker 命令了，比如 `docker ps`、`docker run -d nginx` 等，无需任何额外配置，Colima 已经自动帮您把环境变量对接好了。

### 检查运行状态：

```sh
colima status
```

### 停止 Colima (彻底释放资源，停止耗电)：

```sh
colima stop
```

## 分配硬件资源

默认情况下，Colima 会分配 2核 CPU、2GB 内存和 60GB 硬盘。如果您的项目比较庞大，或者需要运行数据库，可以通过启动参数轻松调整。

### 命令行直接指定资源

如果您希望分配 4核 CPU 和 8GB 内存，可以这样启动：

```sh
colima start --cpu 4 --memory 8 --disk 50
```

### 修改永久配置文件

如果您不想每次都敲那么长的命令，可以修改默认配置：

```sh
colima start --edit
```

这会打开一个 YAML 配置文件（通常在 Vim 或 nano 中），您可以在里面修改 cpu、memory、disk 等参数。保存并退出后，配置即刻生效。

## Apple Silicon (M系列芯片) 专属技巧

如果您使用的是 M1/M2/M3 等 Apple Silicon 芯片的 Mac，默认启动的是 aarch64 (ARM) 架构的虚拟机。

但有时候，某些老旧的镜像只有 x86 (Intel) 版本。在 Docker Desktop 中，它会自动用 Rosetta 转译，而在 Colima 中，您可以直接启动一个原生的 x86 虚拟机：

```sh
# 启动一个 x86 架构的虚拟机（注意：运行速度会比原生 ARM 慢）
colima start --arch x86_64
```

## 清理与重置

如果您把环境弄乱了，或者需要释放磁盘空间，可以彻底删除当前的虚拟机实例（注意：这会删除所有容器和镜像数据）：

```sh
colima delete
```

下次运行 colima start 时，它会像新安装一样重新创建一个干净的环境。

## 报错及解决

### error getting credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH, out: ``

这是一个非常经典的报错！当您从官方 Docker Desktop 切换到 Colima 时，几乎 100% 会遇到这个问题。不要慌，这很容易解决。

报错信息 `executable file not found in $PATH` 的意思是：Docker 找不到名为 docker-credential-desktop 的程序。

因为您之前安装过 Docker Desktop，它悄悄在您的本地配置文件中写下了一行规则：“以后所有关于 Docker 的账号密码，都要通过 desktop（Docker Desktop 专属的凭据管理器）来读取”。

现在 Docker Desktop 被卸载或停止了，但那条旧规则还留在配置文件里，导致现在的 docker 客户端像个无头苍蝇一样找不到原来的凭据程序。

**解决方法**

如果您之前没有在本地配置过极其复杂的私有镜像仓库账号，直接把旧的配置文件重命名（相当于让 Docker 忘记旧设置，重新生成一个干净的）是最高效的。

在终端中执行以下命令：

```sh
mv ~/.docker/config.json ~/.docker/config.json.bak
```

这行命令的作用是把原来的配置文件改名为 .bak 备份文件，Docker 发现没有配置文件时，会恢复默认行为。

### failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory

docker 客户端（你的遥控器）需要通过一个叫 docker.sock 的文件来跟 Docker 守护进程（后台引擎）通信。

这个报错的意思非常直白：你的遥控器找不到引擎了。 这通常只有两种可能：要么引擎根本没启动，要么遥控器指错了方向（还在找以前 Docker Desktop 留下的旧位置）。

Docker 有一个叫做 context（上下文）的概念，用来管理不同的 Docker 环境。安装 Colima 时，它其实已经悄悄为你创建好了一个叫 colima 的专属频道。

强制切换到 Colima 频道，在终端运行：

```sh
docker context use colima
```

运行后，终端应该会提示：colima is the current context

### failed to connect to the docker API at unix:///Users/walter/.colima/default/docker.sock; check if the path is correct and if the daemon is running: dial unix /Users/walter/.colima/default/docker.sock: connect: no such file or directory

没启动 Colima，启动一下就好了：

```sh
colima start
```
