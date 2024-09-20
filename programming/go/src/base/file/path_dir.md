# 目录操作

## 创建多级文件夹

```go
err := os.MkdirAll("/a/b/c", os.ModePerm)
if err != nil {
    fmt.Println(err)
}
```

## 删除文件夹

```go
destPath := "/home/demo2/"
err := os.RemoveAll(destPath)
if err != nil {
    return
}
```
