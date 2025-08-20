### 1. 安装 mdbook

```sh
mkdir -p /build/mdbook
cd /build/mdbook
wget https://github.com/rust-lang/mdBook/releases/download/v0.4.45/mdbook-v0.4.45-x86_64-unknown-linux-gnu.tar.gz
tar -zxvf mdbook-v0.4.45-x86_64-unknown-linux-gnu.tar.gz

# 打开配置文件
sudo vim /etc/profile

# 在最后一行添加
export MDBOOK_HOME=/build/mdbook
export PATH=$MDBOOK_HOME:$PATH

# 使环境变量生效
source /etc/profile

# 验证
mdbook -V
```

### 2. 克隆仓库

```sh
cd ~
git clone https://walter2743-admin@bitbucket.org/walter2743/note.git
```

### 3. 创建部署脚本

```sh
rm -f books.sh
vim books.sh
```

脚本内容:

```sh
#!/bin/bash

# 遇到错误终止运行
set -e

echo "***************start***************"

workdir=~
nginx_path=/usr/share/nginx/html/

# 更新代码
cd "${workdir}/note"
git pull origin master

# 首页
cd "${workdir}/note"
cp index.html ${nginx_path}/

cd "${workdir}/note"
git pull origin master

# 操作系统
cd "${workdir}/note"
cd base/operating_system/
mdbook build
rm -rf ${nginx_path}/operating_system/
cp -r book/ ${nginx_path}/operating_system/

# 组成原理
cd "${workdir}/note"
cd base/computer_organization/
mdbook build
rm -rf ${nginx_path}/computer_organization/
cp -r book/ ${nginx_path}/computer_organization/

# 算法
cd "${workdir}/note"
cd base/algorithm/
mdbook build
rm -rf ${nginx_path}/algorithm/
cp -r book/ ${nginx_path}/algorithm/

# jvm
cd "${workdir}/note"
cd programming/Java/md/jvm/
mdbook build
rm -rf ${nginx_path}/jvm/
cp -r book/ ${nginx_path}/jvm/

# Java虚拟机规范
cd "${workdir}/note"
cd programming/Java/md/jvm_spec/
mdbook build
rm -rf ${nginx_path}/jvm_spec/
cp -r book/ ${nginx_path}/jvm_spec/

# gc
cd "${workdir}/note"
cd programming/Java/md/gc/
mdbook build
rm -rf ${nginx_path}/gc/
cp -r book/ ${nginx_path}/gc/

# java
cd "${workdir}/note"
cd programming/Java/md/java/
mdbook build
rm -rf ${nginx_path}/java/
cp -r book/ ${nginx_path}/java/

# 面试
cd "${workdir}/note"
cd programming/Java/md/java_web/
mdbook build
rm -rf ${nginx_path}/java_web/
cp -r book/ ${nginx_path}/java_web/

# spring_boot
cd "${workdir}/note"
cd programming/Java/md/spring_boot/
mdbook build
rm -rf ${nginx_path}/spring_boot/
cp -r book/ ${nginx_path}/spring_boot/

# spring_cloud
cd "${workdir}/note"
cd programming/Java/md/spring_cloud/
mdbook build
rm -rf ${nginx_path}/spring_cloud/
cp -r book/ ${nginx_path}/spring_cloud/

# mq
cd "${workdir}/note"
cd programming/Java/md/mq/
mdbook build
rm -rf ${nginx_path}/mq/
cp -r book/ ${nginx_path}/mq/

# spring
cd "${workdir}/note"
cd programming/Java/md/spring/
mdbook build
rm -rf ${nginx_path}/spring/
cp -r book/ ${nginx_path}/spring/

# 数据库
cd "${workdir}/note"
cd programming/Java/md/db/
mdbook build
rm -rf ${nginx_path}/db/
cp -r book/ ${nginx_path}/db/

# bugs
cd "${workdir}/note"
cd programming/Java/md/bugs/
mdbook build
rm -rf ${nginx_path}/bugs/
cp -r book/ ${nginx_path}/bugs/

# Python
cd "${workdir}/note"
cd programming/Python/md/py/
mdbook build
rm -rf ${nginx_path}/py/
cp -r book/ ${nginx_path}/py/

# 使用操作系统
cd "${workdir}/note"
cd os/
mdbook build
rm -rf ${nginx_path}/os/
cp -r book/ ${nginx_path}/os/

# 使用软件
cd "${workdir}/note"
cd software/
mdbook build
rm -rf ${nginx_path}/software/
cp -r book/ ${nginx_path}/software/

# go
cd "${workdir}/note"
cd programming/go/
mdbook build
rm -rf ${nginx_path}/go/
cp -r book/ ${nginx_path}/go/

# 前端
cd "${workdir}/note"
cd programming/fe/
mdbook build
rm -rf ${nginx_path}/fe/
cp -r book/ ${nginx_path}/fe/

# flutter
cd "${workdir}/note"
cd programming/flutter/
mdbook build
rm -rf ${nginx_path}/flutter/
cp -r book/ ${nginx_path}/flutter/

# shell
cd "${workdir}/note"
cd programming/shell/
mdbook build
rm -rf ${nginx_path}/shell/
cp -r book/ ${nginx_path}/shell/

# 数学
cd "${workdir}/note"
cd base/math/
mdbook build
rm -rf ${nginx_path}/math/
cp -r book/ ${nginx_path}/math/

# c++
cd "${workdir}/note"
cd programming/cpp/
mdbook build
rm -rf ${nginx_path}/cpp/
cp -r book/ ${nginx_path}/cpp/

# linux_c
cd "${workdir}/note"
cd programming/linux_c/
mdbook build
rm -rf ${nginx_path}/linux_c/
cp -r book/ ${nginx_path}/linux_c/

# 汇编
cd "${workdir}/note"
cd programming/asm/
mdbook build
rm -rf ${nginx_path}/asm/
cp -r book/ ${nginx_path}/asm/

# 诗词
cd "${workdir}/note"
cd base/shici/
mdbook build
rm -rf ${nginx_path}/shici/
cp -r book/ ${nginx_path}/shici/
```

### 4. 运行脚本

```sh
sh books.sh
```
