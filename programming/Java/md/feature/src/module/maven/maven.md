# 搭配 maven 使用

maven 项目中共有三个名称：

1. 在 module-info.java 中定义的模块名称
2. pom.xml 中定义的 Maven 项目名称
3. 由 Maven 生成的 JAR 文件名称

当从其他 module-info.java 文件中引用模块(例如 `requires 模块名`)时，将会使用模块名称。而在 Maven 级别上，向 pom.xml 中添加依赖项时使用 Maven 名称。最后，由 Maven 构建生成的 JAR 文件将用于部署。

在 Maven 中，maven 模块的名称(也称为 Maven 坐标)包含三个部分：`groupId:artifactId:version`。通常，groupId 是项目的反向域名。artifactId 是 maven 模块的名称。最后，version 是 maven 模块的版本号。

Java 模块系统中的模块没有 groupId，也没有版本。

Maven 的模块名称、JPMS 的模块名称以及 JAR 文件名称之间没有关联。

添加依赖项的步骤:

1. 将依赖项添加到 pom 中，以 `groupId:artifactId:version` 的形式使用其 Maven 坐标。这与在 Java 9 之前的项目中使用 Maven 没有什么不同
2. 在 module-info.java 中将依赖项作为 requires 语句添加，以使用该依赖项模块导出的包。如果没有在 pom 文件中添加依赖项，则编译器将在 requires 语句上失败，因为找不到该模块。但如果没有将依赖项添加到 module-info.java，那么依赖项仍然不会允许访问
