# 启动画面

在 Java 中，启动画面(Splash Screen)是应用程序启动时显示的临时图像（通常用于展示 Logo 或加载进度），其命令行选项用于配置启动画面的显示规则（如图像路径、显示时长、窗口位置等）。这些选项需在启动 Java 程序时通过命令行传入（而非在代码中设置），核心依赖 JDK 内置的 java 命令参数。

## 基础语法

```sh
java -splash:<image-path>[,options] <main-class>
```

- `image-path`: 启动画面图像文件的路径（支持本地文件或 JAR 包内资源），支持的图像格式：PNG（推荐，无损且支持透明）、JPG、GIF（静态，不支持动画）
- `options`: 可选配置（用逗号分隔，无空格），如窗口位置、显示时长等（部分选项为 Java 9+ 新增）
- `main-class`: 应用程序的主类

## 显示本地图像文件

直接指定本地 PNG/JPG 文件作为启动画面，默认居中显示，直到应用程序初始化完成

```sh
java -splash:/home/user/logos/app-splash.jpg com.example.MyApp
```

## JAR 包内的图像资源

若图像打包在 JAR 包中（如 resources/splash.png），路径格式为 `jar:<jar-path>!/<resource-path>`

```sh
# 图像在 app.jar 的 resources 目录下
java -splash:jar:app.jar!/resources/splash.png com.example.MyApp
```
