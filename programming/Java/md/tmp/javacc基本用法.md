# javaCC 基本用法

下载:

[javacc-7.0.13.zip](https://github.com/javacc/javacc/archive/javacc-7.0.13.zip)

[javacc-7.0.13.jar](https://repo1.maven.org/maven2/net/java/dev/javacc/javacc/7.0.13/javacc-7.0.13.jar)

解压 javacc-7.0.13.zip 得到 javacc-javacc-7.0.12 目录, 把 javacc-7.0.13.jar 复制到 javacc-javacc-7.0.12/target/目录下。

创建 adder.jj 文件:

```
options {
    STATIC = false;
    OUTPUT_DIRECTORY = "./demo-adder";
}
PARSER_BEGIN(Adder)
import java.io.*;
class Adder {
    static public void main(String[] args) {
        for (String arg : args) {
            try {
                System.out.println(evaluate(arg));
            }
            catch (ParseException ex) {
                System.err.println(ex.getMessage());
            }
        }
    }
    static public long evaluate(String src) throws ParseException {
        Reader reader = new StringReader(src);
        return new Adder(reader).expr();
    }
}
PARSER_END(Adder)
SKIP: { <[" ","\t","\r","\n"]> }
TOKEN: {
    <INTEGER: (["0"-"9"])+>
}
long expr():
{
    Token x, y;
}
{
    x=<INTEGER> "+" y=<INTEGER> <EOF>
        {
            return Long.parseLong(x.image) + Long.parseLong(y.image);
        }
}
```

进入 javacc-javacc-7.0.12/scripts/ 目录, 执行命令:

```sh
javacc 路径/adder.jj
```

会在 OUTPUT_DIRECTORY 指定的目录下生成 demo-adder 目录, 进入 demo-adder 目录, 执行命令:

```sh
javac Adder.java
```

测试 Adder:

```sh
java Adder 1+1
```
