# 安装

[gradle-8.7-all.zip](https://mirrors.cloud.tencent.com/gradle/gradle-8.7-all.zip)

## 配置环境变量

1. 打开配置文件

```sh
vim ~/.zshrc
```

2. 在最后一行添加:

```sh
export GRADLE_HOME=/Users/walter/walter/software/gradle-8.7
export PATH=$GRADLE_HOME/bin:$PATH
```

3. 使环境变量生效

```sh
source ~/.zshrc
```

## 验证

```sh
gradle -v
```

## hello world

创建 build.gradle 文件:

```groovy
task hello {
    doLast {
        println 'Hello World'
    }
}
```

执行:

```sh
gradle -q hello
```
