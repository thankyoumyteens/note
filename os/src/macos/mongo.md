# MongoDB

### 1. 下载tgz包

[https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)

### 2. 解压

### 3. 创建数据和日志目录

默认情况下，MongoDB将数据存储在 `/data/db` 目录中，在macOS上，特别是从Catalina (10.15) 版本开始，系统引入了只读的系统卷，这意味着你不能直接在根目录(/)下创建或修改文件夹，因此你会遇到 "Read-only file system" 的错误。

```sh
mkdir -p /Users/walter/walter/software/mongodb-macos-aarch64--8.2.5/mongodb-data
```

### 4. 配置环境变量

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export PATH=/Users/walter/walter/software/mongodb-macos-aarch64--8.2.5/bin:$PATH

# 使环境变量生效
source ~/.zshrc
```

### 5. 启动

使用 `--dbpath` 选项指定数据目录的路径

```sh
mongod --dbpath /Users/walter/walter/software/mongodb-macos-aarch64--8.2.5/mongodb-data
```

MongoDB 的默认端口是 27017
