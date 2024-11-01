# MacOS 调试 OpenJDK21

## 下载 OPENJDK 源码

```sh
git clone https://gitee.com/mirrors/openjdk.git
cd openjdk/
git checkout -b jdk-21-ga jdk-21-ga
```

## 安装 Command Line Tools (CLT) for Xcode

```sh
xcode-select --install
```

## 安装 Xcode

App Store 安装 Xcode

## 安装其他依赖:

```sh
brew install autoconf
brew install freetype
```

## 下载 Bootstrap JDK

[bellsoft-jdk21.0.2+14-macos-aarch64.tar.gz](https://download.bell-sw.com/java/21.0.2+14/bellsoft-jdk21.0.2+14-macos-aarch64.tar.gz)

[华为云 openjdk 镜像](https://mirrors.huaweicloud.com/openjdk/21.0.2/openjdk-21.0.2_macos-aarch64_bin.tar.gz)

[清华 Adoptium 镜像](https://mirrors.tuna.tsinghua.edu.cn/Adoptium/21/jdk/aarch64/mac/OpenJDK21U-jdk_aarch64_mac_hotspot_21.0.3_9.tar.gz)

## 编译

进入 openjdk 源码根目录

```sh
bash ./configure --with-boot-jdk="/Users/walter/walter/jdk/jdk-21.0.2.jdk" --with-target-bits=64 --with-freetype-lib=/opt/homebrew/Cellar/freetype/2.13.2/lib --with-freetype-include=/opt/homebrew/Cellar/freetype/2.13.2/include --with-jvm-variants=server --disable-warnings-as-errors --with-debug-level=slowdebug
make
make compile-commands
```

## 验证

```sh
./build/macosx-aarch64-server-slowdebug/jdk/bin/java -version
```

## 报错: Only bundled freetype can be specified on Mac and Windows

1. 打开 make/autoconf/lib-freetype.m4, 找到这一句
2. 注释或删除这一段 if

## 报错: 无法打开"xxx", 因为无法验证开发者。

1. 不要关闭弹窗, 左上角 apple -> 系统设置 -> 隐私与安全性 -> 安全性
2. 已阻止使用"xxx", 因为来自身分不明的开发者。
3. 仍要打开

## 使用 CLion 调试

1. File -> Open
2. 选择 jdk 源码根目录下的 build/macosx-aarch64-serverANDclient-slowdebug/compile_commands.json
3. 在弹窗中选择 Open as Project
4. Tools -> Compilation Database -> Change Project Root
5. 选择 jdk 源码根目录
6. 左上角 CLion -> Settings -> Build,Execution,Deployment -> Custom Build Targets -> +

   1. Name: slow_debug
   2. Build -> ... -> +
      1. Name: make_project
      2. Program: make
      3. ArguMents: CONF=macosx-aarch64-serverANDclient-slowdebug
      4. Working directory: 选择 jdk 源码根目录
   3. Clean -> ... -> +
      1. Name: clean_project
      2. Program: make
      3. ArguMents: CONF=macosx-aarch64-serverANDclient-slowdebug clean
      4. Working directory: 选择 jdk 源码根目录

7. Add Configuration... -> Edit Configurations... -> + -> Custom Build Application

   1. Target: 选择 slow_debug
   2. Executable: 选择 jdk 源码根目录下的 build/macosx-aarch64-serverANDclient-slowdebug/jdk/bin/java

8. 创建 java 文件:

```java
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
          // System.out.println(strings.size() + " -- " + o.toString());
          strings.add(o);
        }
      }
      Thread.sleep(100);
    }
  }
}
```

9. 编译成 class

```sh
javac Test.java
```

10. Clion -> 右上角 Edit Configurations...
    1. Program Arguments: 输入 `-Xmx128M -XX:+UseG1GC -Xlog:gc*=debug Test`
    2. Working directory: 输入 class 文件所在的目录
11. 启动 debug

## 忽略 SIGILL 信号

调试过程中会出现 SIGILL 信号而导致调试不能继续进行, 这是因为调试器默认会捕获这些信号, 调试器以为程序运行出错, 于是退出了。但实际上, SIGILL 的出现是 Hotspot 运行的正常逻辑, Hotspot 自己会捕获该信号然后做处理, 所以我们要配置调试器忽略这些信号。

在 ~/.lldbinit 文件(不存在就手动创建)中输入:

```sh
settings set target.load-cwd-lldbinit true
```

在项目根目录路径下创建 .lldbinit 文件, 并输入:

```sh
br set -n main -o true -G true -C "pro hand -p true -s false SIGILL"
```

## 更新 xcode 后运行报错

1. 关闭 CLion
2. 重新编译

```sh
make clean
bash ./configure --with-boot-jdk="/Users/walter/walter/jdk/jdk-21.0.2.jdk" --with-target-bits=64 --with-freetype-lib=/opt/homebrew/Cellar/freetype/2.13.2/lib --with-freetype-include=/opt/homebrew/Cellar/freetype/2.13.2/include --with-jvm-variants=server --disable-warnings-as-errors --with-debug-level=slowdebug
make
make compile-commands
```

3. 打开 CLion, 会自动重新索引
