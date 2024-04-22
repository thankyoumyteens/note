# JAR 文件

JAR（Java Archive）文件是一种打包文件格式，用于将 Java 类文件、相关的元数据和资源（如文本、图片等）打包到一个单一的文件中。

一个 JAR 文件就是一个 ZIP 文件，它们使用了相同的压缩算法和文件格式。然而，JAR 文件通常包含特定的内容和结构，使其更适合作为 Java 应用程序或库的分发格式。

## META-INF 目录

在 Java 的 JAR 文件中，`META-INF`目录是一个特殊的目录，用于存放关于 JAR 文件的元数据（Metadata）。元数据是描述其他数据的数据，它提供了关于 JAR 文件内容的重要信息，这些信息对于 Java 应用程序的运行和类加载器的类加载过程至关重要。

`META-INF`目录通常包含以下几个关键文件：

1. **MANIFEST.MF**：这是最重要的元数据文件，它包含了 JAR 文件的清单信息。清单可以指定 JAR 的属性，如主类（Main-Class），这个类包含了程序的入口点（main 方法）。清单还可以包含其他信息，如版本信息、签名信息、项目描述等。

2. **SIGNATURE.\***：这些文件包含了 JAR 文件的数字签名，用于验证 JAR 文件的来源和完整性。它们通常在 JAR 文件被签名后生成。

3. **INDEX.LIST**：这是一个可选文件，如果存在，它包含了 JAR 文件的索引，可以加快 JAR 文件内容的查找速度。

4. **services/**：这个目录包含了服务提供者配置文件，它们遵循 JSR-330 标准，用于服务提供者发现机制。

5. **MANIFEST.MF 的数字签名文件**：如果 JAR 文件被签名，`META-INF`目录下还可能包含与`MANIFEST.MF`相关的签名文件，如`MANIFEST.MF.asc`和`MANIFEST.MF.md5`。

在某些情况下，开发者可能需要手动编辑`MANIFEST.MF`文件，比如指定主类或添加其他属性，但通常这是在构建 JAR 文件的过程中由构建工具（如 Maven 或 Gradle）自动完成的。

## jar 命令

jar 命令和 tar 命令类似, 以下是一些常见的 `jar` 命令及其用法：

### 查看 JAR 文件内容

```shell
jar tf myapp.jar
```

- `t`：列出 JAR 文件中的条目。
- `f`：指定 JAR 文件的名称。

### 解压 JAR 文件

```shell
jar xvf myapp.jar
```

- `x`：解压缩 JAR 文件。
- `v`：生成详细输出。
- `f`：指定 JAR 文件的名称。

### 向现有 JAR 文件添加文件

```shell
jar uvf myapp.jar myclass.class
```

- `u`：更新现有的 JAR 文件。
- `v`：生成详细输出。
- `f`：指定 JAR 文件的名称。

### 从 JAR 文件删除文件

```shell
jar dvf myapp.jar myclass.class
```

- `d`：从 JAR 文件中删除条目。
- `v`：生成详细输出。
- `f`：指定 JAR 文件的名称。

### 将目录内容打包成 JAR 文件

```shell
jar cvf myapp.jar src/ lib/
```

这个命令将 `src/` 目录和 `lib/` 目录的内容打包成 `myapp.jar`。

### 查看 JAR 文件的清单信息

```shell
jar xvf manifest.txt myapp.jar META-INF/MANIFEST.MF
```

这个命令将 JAR 文件中的清单文件提取出来查看。

### 将清单文件和所有文件打包成 JAR

```shell
jar cvfm myapp.jar manifest.txt *
```

这个命令使用 `manifest.txt` 作为清单文件，并将所有文件打包成 `myapp.jar`。
