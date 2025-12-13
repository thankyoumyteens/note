# 用 NIO 写入文件

```java
package com.example;

import java.io.FileOutputStream;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;

public class NioFileWrite {
    static void main(String[] args) throws Exception {

        // 要写入的文件
        FileOutputStream fos = new FileOutputStream("demo.txt");
        // 获取通道
        FileChannel channel = fos.getChannel();

        try (fos; channel) {
            String text = "Hello NIO FileChannel\n";
            // 分配一个缓冲区
            ByteBuffer buffer = ByteBuffer.wrap(text.getBytes(StandardCharsets.UTF_8));

            // 直接写入
            var _ = channel.write(buffer);
        }
    }
}
```
