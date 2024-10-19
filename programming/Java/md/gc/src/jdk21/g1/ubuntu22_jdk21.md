# ubuntu22 调试 OpenJDK21

## 下载 OPENJDK 源码

```sh
git clone https://gitee.com/mirrors/openjdk.git
cd openjdk/
git checkout -b jdk-21-ga jdk-21-ga
```

## 下载 Bootstrap JDK

[bellsoft-jdk21.0.2+14-macos-aarch64.tar.gz](https://download.bell-sw.com/java/21.0.2+14/bellsoft-jdk21.0.2+14-macos-aarch64.tar.gz)

[华为云 openjdk 镜像](https://mirrors.huaweicloud.com/openjdk/21.0.2/openjdk-21.0.2_macos-aarch64_bin.tar.gz)

[清华 Adoptium 镜像](https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21/jdk/aarch64/mac/OpenJDK21U-jdk_aarch64_mac_hotspot_21.0.3_9.tar.gz)

## 安装其他依赖:

```sh
sudo apt-get install -y libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev libxcursor-dev libcups2-dev libfreetype6-dev libasound2-dev autoconf
```

## 编译

进入 openjdk 源码根目录

```sh
bash ./configure --with-boot-jdk="/software/jdk-21.0.4+7" --with-target-bits=64 --with-jvm-variants=server --disable-warnings-as-errors --with-debug-level=slowdebug
make
make compile-commands
```

## 验证

```sh
./build/linux-x86_64-server-slowdebug/jdk/bin/java -version
```

## 配置 IDE

1. 使用 CLion File=> Open => 选择文件: /jdk_root/build/linux-x86_64-server-slowdebug/compile_commands.json
2. 选择 open as Project
3. 修改项目的根目录
4. Tools -> Compilation Database -> Change Project Root, 选中源码根目录: /jdk_root

## Custom Build Targets

1. File -> Settings -> Build,Execution,Deployment -> Custom Build Targets -> +
   1. Name -> slow-debug
   2. Build -> ... -> +
      1. Name -> make linux-x86_64-server-slowdebug
      2. Program -> make
      3. ArguMents -> CONF=linux-x86_64-server-slowdebug
      4. Working directory 选择: /jdk_root
   3. Clean -> ... -> +
      1. Name -> clean linux-x86_64-server-slowdebug
      2. Program -> make
      3. ArguMents -> CONF=linux-x86_64-server-slowdebug clean
      4. Working directory 选择: /jdk_root

## Run/Debug configurations

1. Run/Debug configurations -> + -> Custom Build Application
   1. Target 选择: slow-debug
   2. Executable 选择: /jdk_root/build/linux-x86_64-server-slowdebug/jdk/bin/java

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
