# 用 NIO 读取文件

```java
package com.example;

import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

public class NioFileRead {
    static void main(String[] args) throws Exception {

        // 要读的文件
        FileInputStream fis = new FileInputStream("demo.txt");
        // 获取通道
        FileChannel channel = fis.getChannel();

        try (fis; channel) {
            // 分配一个缓冲区
            ByteBuffer buffer = ByteBuffer.allocate(1024);

            // 读取文件内容, 并写到缓冲区中
            while (channel.read(buffer) != -1) { // 读到 -1 表示文件结束
                // buffer 由写模式切换到读模式
                buffer.flip();

                // 从 buffer 中读取数据
                while (buffer.hasRemaining()) {
                    // 输出
                    System.out.print((char) buffer.get());
                }

                // 清空 buffer，准备下一轮读取
                buffer.clear();
            }
        }
    }
}
```
