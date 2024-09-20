# 路径操作

## 获取当前可执行文件所在的路径

```go
path, _ := os.Executable()
fmt.Println(path)
```

## 获取当前当前登录用户的家路径

```go
current, _ := user.Current()
dir := current.HomeDir
fmt.Println(dir)
```

## 获取当前当前工作目录的路径

```go
dir, _ := os.Getwd()
fmt.Println(dir)
```

## 获取绝对路径

```go
relativePath := "hello.go"
absolutePath, _ := filepath.Abs(relativePath)
fmt.Println(absolutePath)
```

## 获取相对路径

```go
absolutePath := "/usr/local/go/bin/go"
// 获取相对/usr/local的路径: go/bin/go
relativePath, _ := filepath.Rel("/usr/local", absolutePath)
fmt.Println(relativePath)
```

## 拼接路径

```go
basePath := "/home"
// /home/user/bin/nginx
distPath := filepath.Join(basePath, "user", "bin", "nginx")
fmt.Println(distPath)
```

## 获取上级目录

```go
basePath := "/home/user/bin/nginx"
// /home/user/bin
parentPath := filepath.Join(basePath, "../")
fmt.Println(parentPath)
```

## 获取文件名

```go
basePath := "/home/demo.txt"
fileName := filepath.Base(basePath)
fmt.Println(fileName)
```

## 获取扩展名

```go
basePath := "/home/demo.txt"
ext := filepath.Ext(basePath)
fmt.Println(ext)
```

## 遍历目录下所有文件和文件夹

```go
// 递归获取所有下级文件和文件夹
var files []string
err := filepath.Walk("/home", func(path string, info os.FileInfo, err error) error {
    if !info.IsDir() {
        files = append(files, path)
    }
    return nil
})
if err != nil {
    return
}
fmt.Println(files)

// 获取直接下级的所有文件
var files []string
dir, _ := os.ReadDir("/Users/walter/walter/tmp/gradle_demo")
for _, file := range dir {
    files = append(files, file.Name())
}
fmt.Println(files)
```

## 判断是不是文件

```go
destPath := "/home/demo2/1_copy.txt"
stat, _ := os.Stat(destPath)
isFile := !stat.IsDir()
fmt.Println(isFile)
```

## 判断是不是文件夹

```go
destPath := "/home/demo2/1_copy.txt"
stat, _ := os.Stat(destPath)
isDir := stat.IsDir()
fmt.Println(isDir)
```

## 判断文件或文件夹是否存在

```go
destPath := "/home/demo2/1_copy.txt"
_, err := os.Stat(destPath)
if err != nil {
    fmt.Println("不存在")
} else {
    fmt.Println("存在")
}
```
