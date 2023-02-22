# 使用腾讯云 DockerHub 加速器

创建或修改 /etc/docker/daemon.json 文件
```
vim /etc/docker/daemon.json
```
写入以下内容
```
{
   "registry-mirrors": [
       "https://mirror.ccs.tencentyun.com"
  ]
}
```
重新启动 Docker 服务
```
sudo systemctl daemon-reload
sudo systemctl restart docker
# Ubuntu16.04 请执行 sudo systemctl restart dockerd 命令
```
执行 docker info 命令
```
docker info
```
返回结果中包含以下内容, 则说明配置成功
```
Registry Mirrors:
 https://mirror.ccs.tencentyun.com
```
