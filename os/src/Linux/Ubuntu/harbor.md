# 下载解压

```sh
cd ~/src_pack
wget https://github.com/goharbor/harbor/releases/download/v2.9.1/harbor-offline-installer-v2.9.1.tgz
tar -zxvf harbor-offline-installer-v2.9.1.tgz
```

# 编辑配置文件

```sh
cd harbor/
cp harbor.yml.tmpl harbor.yml
vim harbor.yml
```

注释掉 https 的配置内容
配置 http 相关的参数, 主要是 hostname 和 port

# 安装

```sh
./install.sh
```
