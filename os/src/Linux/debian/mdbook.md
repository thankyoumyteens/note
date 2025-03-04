# 安装 mdbook

### 1. 安装

```sh
mkdir -p /build/mdbook
cd /build/mdbook
wget https://github.com/rust-lang/mdBook/releases/download/v0.4.45/mdbook-v0.4.45-x86_64-unknown-linux-gnu.tar.gz
tar -zxvf mdbook-v0.4.45-x86_64-unknown-linux-gnu.tar.gz
```

### 2. 配置环境变量:

```sh
# 打开配置文件
sudo vim /etc/profile

# 在最后一行添加
export MDBOOK_HOME=/build/mdbook
export PATH=$MDBOOK_HOME:$PATH

# 使环境变量生效
source /etc/profile
```

### 3. 验证:

```sh
mdbook -V
```
