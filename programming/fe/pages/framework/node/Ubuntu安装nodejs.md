# 下载nodejs

```
wget https://repo.huaweicloud.com/nodejs/latest/node-v16.4.0-linux-x64.tar.gz
tar -zxvf node-v16.4.0-linux-x64.tar.gz
cp -r node-v16.4.0-linux-x64/ /usr/local/nodejs/
```

# 设置环境变量

```
vim /etc/profile
```

```conf
export PATH=/usr/local/nodejs/bin:$PATH
```

```
source /etc/profile
node -v
npm -v
```

# 设置镜像

```
npm install -g cnpm --registry=https://registry.npmmirror.com
npm cache clean -f
```
