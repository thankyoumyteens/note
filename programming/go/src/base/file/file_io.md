# 基本文件读写

## 一次性读取

```go
destPath := "/home/1.txt"
bytes, _ := os.ReadFile(destPath)
fmt.Println(string(bytes))
```

## 一次性写入

```go
destPath := "/home/1.txt"
err := os.WriteFile(destPath, []byte("hello world"), os.ModePerm)
if err != nil {
    fmt.Println(err)
}
```

## 按行读取

```go
destPath := "/home/1.txt"
file, _ := os.OpenFile(destPath, os.O_RDONLY, 0)
defer file.Close()

reader := bufio.NewReader(file)
for {
    line, _, err := reader.ReadLine()
    if err != nil {
        // 读取到文件末尾后, 会返回一个EOF错误
        break
    }
    println(string(line))
}
```

## 按行写入

```go
destPath := "/home/1.txt"
// O_CREATE: 如果文件不存在则会自动创建
file, _ := os.OpenFile(destPath, os.O_CREATE|os.O_WRONLY, 0)
defer file.Close()

writer := bufio.NewWriter(file)
_, err := writer.WriteString("hello\n")
if err != nil {
    panic(err)
}
writer.Flush()
```
