# Ubuntu 18.04 安装docker ce
卸载老版本
```
sudo apt-get remove docker docker-engine docker.io
```
更新apt包索引
```
sudo apt-get update
```
安装包以允许通过HTTPS使用存储库：
```
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common
```
添加Docker的GPG密钥：
```
curl -fsSL https://repo.huaweicloud.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```
对于amd64架构的计算机，添加软件仓库
```
sudo add-apt-repository "deb [arch=amd64] https://repo.huaweicloud.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
```
更新apt包索引
```
sudo apt-get update
```
安装最新版本的Docker CE
```
sudo apt-get install docker-ce
```
查看Docker CE 版本
```
docker -v 
```
运行hello-world
```
sudo docker run hello-world
```
