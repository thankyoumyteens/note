# Maven 内置变量

- `${basedir}` 项目根目录(pom.xml 文件所在目录)
- `${project.xxx}` 当前 pom 文件的任意节点的内容
- `${project.build.directory}` 构建目录, 缺省为 target 目录
- `${project.build.outputDirectory}` 构建过程输出目录, 缺省为 target/classes
- `${project.build.finalName}` 产出物名称, 缺省为 `${project.artifactId}-${project.version}`
- `${project.packaging}` 打包类型, 缺省为 jar
- `${env.xxx}` 获取系统环境变量。例如 `env.PATH` 指代了 path 环境变量
- `${settings.xxx}` 指代了 settings.xml 中对应元素的值。例如 `<settings><offline>false</offline></settings>`通过 `${settings.offline}` 获得 offline 的值
- Java System Properties: 所有可通过 java.lang.System.getProperties()访问的属性都能在 POM 中使用, 例如 `${JAVA_HOME}`
