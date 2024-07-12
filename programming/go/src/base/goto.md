# goto

```go
func main() {
    for i := 0; i < 100; i++ {
        for j := 0; j < 100; j++ {
            fmt.Printf("%d ", j)
            if j == 2 {
                goto done
            }
        }
    }
done:
    fmt.Println("done")
}
```
