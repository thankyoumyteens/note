# svn 使用

## 代码检出

```sh
svn checkout svn://xxx.com/xxx/xxx
# 指定存储目录
svn checkout svn://xxx.com/xxx/xxx target_dir
```

## 更新代码

```sh
svn update
# 更新到指定版本
svn update -r xxx
```

## 添加文件

```sh
# 添加指定文件或目录
svn add /path/to/file-or-dir
# 添加当前目录下所有 java 文件
svn add *.java
```

## 删除文件

```sh
# 删除指定文件或目录, 必须要用命令, 不能在本地直接删除
svn delete /path/to/file-or-dir
```

## 提交代码

```sh
svn commit -m "提交描述"
```

## 查看状态

```sh
svn status
```

## 查看日志

```sh
# 只输出最新的 5 条日志
svn log -l 5
# 查看日志, 并且输出变动的文件列表
svn log -v
```
