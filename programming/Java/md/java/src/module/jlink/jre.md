# 生成 JRE 目录

从 JDK 9 开始，Oracle JDK 和 OpenJDK 不再默认包含独立的 JRE 目录，而是提供了 jlink 工具来允许用户根据需求自定义生成最小化的 JRE。

## 查看 JDK 包含的模块

可以通过 `java --list-modules` 查看 JDK 中可用的模块，确定需要包含在 JRE 中的核心模块

## 使用 jlink 生成精简的 JRE

```sh
jlink \
  --add-modules java.base,java.desktop \
  --output ./jre \
  --strip-debug \
  --no-header-files \
  --no-man-pages \
  --compress=zip-6
```
