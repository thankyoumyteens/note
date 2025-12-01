# java.awt

java.awt 是 Abstract Window Toolkit（抽象窗口工具包） 的缩写，是 Java 早期提供的图形用户界面（GUI）开发工具包，属于 Java 基础类库（JFC）的核心组成部分，主要用于构建桌面应用的界面、处理图形绘制与用户交互，是 Java GUI 开发的底层基础。

如今 java.awt 已较少直接用于 GUI 开发(主流用 JavaFX)。

## headless 模式

正常情况下，Java AWT/Swing 假定有：

- 显示器（显示窗口、对话框）
- 鼠标、键盘（用户可以点、输）

但在很多场景中是 没有图形界面 的，比如：

- Linux 服务器上没有 X Window / 桌面环境
- Docker 容器中只跑后端程序
- CI/CD 构建、测试环境（如 Jenkins、GitLab CI）

在这些环境下，你如果创建 Swing/AWT 的窗口、对话框，会因为找不到显示设备而抛错。headless 模式 就是专门给这种环境设计的: 禁止使用需要真实屏幕的功能，但保留很多图形相关的计算功能。

虽然不能创建 UI 窗口，但很多“图形计算”还是可以用的，例如：

- 生成图片（BufferedImage）
- 对图片进行缩放、裁剪、合成（Graphics2D）
- 使用字体、文本布局等（部分字体功能）
- 服务器端生成验证码图片、报表图片、图表等

开启 headless 模式的命令:

```sh
java -Djava.awt.headless=true YourMainClass
```
