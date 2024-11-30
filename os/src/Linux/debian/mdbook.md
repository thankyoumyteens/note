# 安装 mdbook

### 1. 安装

```sh
mkdir mdbook-v0.4.40
cd mdbook-v0.4.40
wget https://github.com/rust-lang/mdBook/releases/download/v0.4.40/mdbook-v0.4.40-x86_64-unknown-linux-gnu.tar.gz
tar -zxvf mdbook-v0.4.40-x86_64-unknown-linux-gnu.tar.gz
```

### 2. 配置环境变量:

```sh
# 打开配置文件
sudo vim /etc/profile

# 在最后一行添加
export MDBOOK_HOME=/software/mdbook-v0.4.40
export PATH=$MDBOOK_HOME:$PATH

# 使环境变量生效
source /etc/profile
```

### 3. 验证:

```sh
mdbook -V
```
