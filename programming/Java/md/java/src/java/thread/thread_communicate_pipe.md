# 管道

管道是一种特殊的流, 用于在线程之间传递数据。它通常由两个管道流组成: 一个输入管道流和一个输出管道流。输入管道流用于从一个线程读取数据, 而输出管道流用于将数据写入另一个线程。这两个管道流之间的数据传输是单向的, 即数据只能从输入流传输到输出流。

默认情况下, 当没有数据可读时, 从输入管道流读取数据的操作会阻塞当前线程, 直到有数据可用。这种行为称为阻塞模式。如果不想阻塞, 可以循环调用 available 方法来检查是否有可用的数据。

```java
import java.io.IOException;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Semaphore;

public class Demo {
    public static void main(String[] args) {
        // 输入管道
        PipedInputStream pipeIn = new PipedInputStream();
        // 输出管道
        PipedOutputStream pipeOut = new PipedOutputStream();
        // 将输入管道流与输出管道流连接起来, 以便数据可以从一个流传输到另一个流
        try {
            pipeIn.connect(pipeOut);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        // 线程B
        Thread threadB = new Thread(() -> {
            try {
                // 等待A线程的数据
                byte[] buffer = new byte[1024];
                int len = pipeIn.read(buffer);
                String message = new String(buffer, 0, len);
                System.out.println(message);
                pipeIn.close();
            } catch (IOException ignored) {
            }
        });

        // 线程A
        new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ignored) {
            }
            // 向B线程发送数据
            try {
                pipeOut.write("来自线程A".getBytes());
                pipeOut.close();
            } catch (IOException ignored) {
            }
        }).start();


        threadB.start();
    }
}
```
