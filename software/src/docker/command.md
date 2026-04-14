# 常用基础命令

**镜像操作：**

- **搜索镜像:** `docker search <镜像名>` (例如: `docker search ubuntu`)
- **拉取（下载）镜像:** `docker pull <镜像名>:<标签>` (例如: `docker pull nginx:latest`，如果不写标签，默认拉取 latest 最新版)
- **查看本地镜像:** `docker images`
- **删除本地镜像:** `docker rmi <镜像ID或名称>`

**容器操作：**

- **运行容器:** `docker run [参数] <镜像名>`
  - `-d`: 后台运行容器。
  - `-p`: 端口映射（`宿主机端口:容器内端口`）。
  - `--name`: 给容器起个名字。
- **查看正在运行的容器:** `docker ps`
- **查看所有容器 (包括已停止的):** `docker ps -a`
- **停止容器:** `docker stop <容器ID或名称>`
- **启动已停止的容器:** `docker start <容器ID或名称>`
- **删除容器:** `docker rm <容器ID或名称>` (注意：只能删除已停止的容器，强制删除加 `-f`)
- **进入正在运行的容器:** `docker exec -it <容器ID或名称> /bin/bash` (或者 `/bin/sh`)
