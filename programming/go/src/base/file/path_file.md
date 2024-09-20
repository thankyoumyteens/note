# 文件操作

## 复制文件

```go
srcPath := "/home/demo1/1.txt"
destPath := "/home/demo2/1_copy.txt"
srcFile, _ := os.Open(srcPath)
destFile, _ := os.Create(destPath)
defer srcFile.Close()
defer destFile.Close()
copiedBytes, _ := io.Copy(destFile, srcFile)
fmt.Println(copiedBytes)
```

## 移动文件

```go
srcPath := "/home/demo1/1.txt"
destPath := "/home/demo2/1_copy.txt"
err := os.Rename(srcPath, destPath)
if err != nil {
    return
}
```

## 删除文件

```go
destPath := "/home/demo2/1_copy.txt"
err := os.Remove(destPath)
if err != nil {
    return
}
```
