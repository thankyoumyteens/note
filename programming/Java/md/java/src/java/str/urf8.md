# 区分 UTF-8 字符串中的 ASCII 与非 ASCII 字符

UTF-8 编码规则:

- ASCII 字符(0-127): 在 UTF-8 中以单字节表示，字节的最高位为 `0`，其余 7 位为字符的 ASCII 值(即字节范围为 `0x00` 到 `0x7F`)
- 非 ASCII 字符: 用多字节表示(2-4 字节)，且首字节的最高位为 `1`，具体规则:
  - 2 字节字符: 首字节以 `110` 开头(范围 `0xC0` - `0xDF`)，后续字节以 `10` 开头(`0x80` - `0xBF`)
  - 3 字节字符: 首字节以 `1110` 开头(`0xE0` - `0xEF`)，后续字节同上
  - 4 字节字符: 首字节以 `11110` 开头(`0xF0` - `0xF7`)，后续字节同上

判断方法: 对字符串中的每个字节(或字符的编码值)进行检查:

1. 若字节值在 `0x00` ~ `0x7F` 范围内 -> ASCII 字符
2. 若字节值 ≥ `0x80` -> 属于非 ASCII 字符的编码(可能是多字节中的首字节或后续字节)

```java
import java.util.ArrayList;
import java.util.List;

public class Main {

    // 判断UTF-8字符的字节长度（基于首字节）
    private static int getUtf8CharLength(byte firstByte) {
        if ((firstByte & 0xE0) == 0xC0) { // 110xxxxx → 2字节
            return 2;
        } else if ((firstByte & 0xF0) == 0xE0) { // 1110xxxx → 3字节
            return 3;
        } else if ((firstByte & 0xF8) == 0xF0) { // 11110xxx → 4字节
            return 4;
        } else {
            // 无效UTF-8字节（如后续字节10xxxxxx），按1字节处理
            return 1;
        }
    }

    public static void main(String[] args) {
        String str = "Hello, 世界！123";
        byte[] utf8Bytes = str.getBytes(java.nio.charset.StandardCharsets.UTF_8);

        List<Byte> asciiBytes = new ArrayList<>();
        List<Byte> nonAsciiBytes = new ArrayList<>();

        int i = 0;
        while (i < utf8Bytes.length) {
            byte b = utf8Bytes[i];
            // ASCII字节范围：0x00-0x7F（十进制0-127）
            if ((b & 0x80) == 0) {
                // 最高位为0，是ASCII
                asciiBytes.add(b);
                i++;
            } else {
                // 非ASCII，根据首字节判断总字节数
                int length = getUtf8CharLength(b);
                // 将当前字符的所有字节加入非ASCII列表
                for (int j = 0; j < length && i < utf8Bytes.length; j++) {
                    nonAsciiBytes.add(utf8Bytes[i]);
                    i++;
                }
            }
        }

        System.out.println("ASCII字节（十进制）: " + asciiBytes);
        System.out.println("非ASCII字节（十进制）: " + nonAsciiBytes);
    }
}
```
