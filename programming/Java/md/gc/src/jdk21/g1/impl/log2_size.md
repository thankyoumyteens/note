# 根据哈希值计算索引时保证索引在数组内

涉及的变量:

- 数组大小 size: 必须是 2 的 n 次方
- 以 2 为底数组大小的对数 log2_size: 就是 2 的 n 次方里的 n, size = 2^log2_size
- 掩码 mask: 用来保证索引在数组内
- 哈希值 hash: 用来计算数组索引

步骤:

1. 先确定 log2_size, 例如 log2_size = 13
2. 根据 log2_size 计算出 size。计算方法: 把 1 左移 log2_size 位(相当于 2 的 log2_size 次方)
3. 根据 log2_size 计算出 mask。计算方法: 把 mask 的低 log2_size 位全设为 1，其余位全设为 0(mask = size - 1, 数组的范围也是 0 到 size-1)
4. 转换成二进制后, 可以看到 mask 和 size 的关系: 0000000000000000000000000000000000000000000000000010000000000000, 0000000000000000000000000000000000000000000000000001111111111111
5. 把 hash 和 mask 进行按位与操作, 就得到了数组的索引(只保留 hash 的低 log2_size 位, 范围就是 0 到 size-1)

## 示例

```cpp
int main() {
    size_t log2_size = 13;

    // size = 2^13 = 8192
    size_t size = ((size_t) 1ul) << log2_size;

    // 根据 log2_size 计算出 mask
    // ~((size_t) 0) -> 1111111111111111111111111111111111111111111111111111111111111111
    // ~((size_t) 0) << log2_size -> 1111111111111111111111111111111111111111111111111110000000000000
    // mask -> 0000000000000000000000000000000000000000000000000001111111111111
    // mask = 8191
    size_t mask = ~(~((size_t) 0) << log2_size);

    size_t hash = getHash();

    // 只保留hash的低log2_size位
    size_t index = hash & mask;

    std::cout << "数组的索引: " << index << std::endl;

    return 0;
}
```
