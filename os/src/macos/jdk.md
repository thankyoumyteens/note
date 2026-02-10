# jdk

### 1. 下载

随便选一个下载

- [Liberica](https://bell-sw.com/pages/downloads/)
- [Adoptium](https://adoptium.net/temurin/releases)
- [Adoptium(清华源)](https://mirrors.tuna.tsinghua.edu.cn/Adoptium)
- [Zulu](https://www.azul.com/downloads/?package=jdk#zulu)
- [Microsoft](https://learn.microsoft.com/zh-cn/java/openjdk/download)

### 2. 配置

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export JAVA_HOME=/Users/walter/walter/jdk/jdk-25.0.1+8/Contents/Home
export PATH=$JAVA_HOME/bin:$PATH

# 使环境变量生效
source ~/.zshrc

# 验证
java -version
```

## 报错: 无法打开"java", 因为无法验证开发者:

1.  左上角 apple -> 系统设置 -> 隐私与安全性 -> 安全性
2.  已阻止使用"java", 因为来自身分不明的开发者
3.  仍要打开
