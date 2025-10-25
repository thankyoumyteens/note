# 交叉编译

要为目标平台（如在 Windows 上为 Linux 生成镜像）生成镜像，需借助目标平台的 JDK 模块文件（jmods），具体步骤如下：

### 1. 获取目标平台的 JDK 模块文件（jmods 目录）

jlink 生成镜像依赖 JDK 的 jmods 目录（包含所有系统模块，如 `java.base.jmod`），跨平台生成需使用目标平台的 jmods：

1. 下载目标平台的 JDK（如 Linux x64 版本）
2. 解压后，提取其 jmods 目录（例如 `linux-jdk/jmods`）

### 2. 使用目标平台的 jmods 生成镜像

在当前平台（如 Windows）的 JDK 中执行 jlink，通过 `--module-path` 指定目标平台的 jmods 目录，即可生成目标平台的镜像：

```sh
# 示例：在 Windows 上为 Linux x64 生成镜像
jlink \
  --module-path ./my-app-modules:./linux-jdk/jmods \  # 应用模块 + 目标平台 jmods
  --add-modules com.myapp \                         # 根模块
  --output ./linux-runtime \                        # 输出目标平台镜像
```
