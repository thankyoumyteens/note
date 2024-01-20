# ubuntu22 调试 OpenJDK21

## 下载 Bootstrap JDK

```sh
cd ~/src_pack/
wget https://download.bell-sw.com/java/21.0.1+12/bellsoft-jdk21.0.1+12-linux-amd64.tar.gz
mv bellsoft-jdk21.0.1+12-linux-amd64.tar.gz ~/jdk/
tar -zxvf bellsoft-jdk21.0.1+12-linux-amd64.tar.gz
```

## 编译 OpenJDK21

```sh
sudo apt-get install -y libX11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev libcups2-dev libfreetype6-dev libasound2-dev autoconf
bash ./configure --with-target-bits=64 --with-boot-jdk=/home/walter/jdk/jdk-21.0.1 --with-debug-level=slowdebug
make
make compile-commands
```

## 配置 IDE

使用 CLion File=> Open => 选择文件

/home/walter/src_pack/jdk21-jdk-21-ga/build/linux-x86_64-server-slowdebug/compile_commands.json

选择 open as Project

这时候, 你会发现你是看不到源码的, 所以下面需要修改项目的根目录,

Tools -> Compilation Database -> Change Project Root 功能, 选中你的源码目录: /home/walter/src_pack/jdk21-jdk-21-ga

## Custom Build Targets

1. File -> Settings -> Build,Execution,Deployment -> Custom Build Targets -> +
   1. Name -> slow-debug
   2. Build -> ... -> +
      1. Name -> make linux-x86_64-server-slowdebug
      2. Program -> make
      3. ArguMents -> CONF=linux-x86_64-server-slowdebug
      4. Working directory -> /home/walter/src_pack/jdk21-jdk-21-ga
   3. Clean -> ... -> +
      1. Name -> clean linux-x86_64-server-slowdebug
      2. Program -> make
      3. ArguMents -> CONF=linux-x86_64-server-slowdebug clean
      4. Working directory -> /home/walter/src_pack/jdk21-jdk-21-ga

## Run/Debug configurations

1. Run/Debug configurations -> + -> Custom Build Application
   1. Target 选择 slow-debug
   2. Executable 选择/home/walter/src_pack/jdk21-jdk-21-ga/build/linux-x86_64-server-slowdebug/jdk/bin/java

## 调试

创建文件

```java
// -Xmx256M -XX:+UseG1GC -Xlog:gc*=debug Test

import java.util.LinkedList;

public class Test {

    public static class DemoObj {
        public String v;
        public DemoObj(String v) {
            this.v = v;
        }
    }

  private static final LinkedList<DemoObj> strings = new LinkedList<>();
  public static void main(String[] args) throws Exception {
    int iteration = 0;
    while (true) {
      for (int i = 0; i < 100; i++) {
        for (int j = 0; j < 10; j++) {
           DemoObj o =  new DemoObj("String " + j);
        //    System.out.println(strings.size() + " -- " + o.toString());
          strings.add(o);
        }
      }
      Thread.sleep(100);
    }
  }
}
```

编译成 class

```sh
javac Test.java
```

1. Clion -> Run/Debug configurations
   1. Program Arguments 输入 Test
   2. Working directory 输入 class 文件所在的目录
2. 启动 debug
