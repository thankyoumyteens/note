# 卸载旧版

```sh
sudo apt-get remove docker docker-engine docker.io
```

# 安装依赖

```sh
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
```

# 信任 Docker 的 GPG 公钥

```sh
curl -fsSL https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

# 添加软件仓库

```sh
sudo add-apt-repository "deb [arch=amd64] https://mirrors.huaweicloud.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
```

# 更新索引文件

```sh
sudo apt-get update
```

# 安装 Docker

```sh
sudo apt-get install -y docker-ce
```

# 查看版本

```sh
docker version
```
