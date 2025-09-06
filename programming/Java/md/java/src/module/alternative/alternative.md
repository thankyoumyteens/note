# 可选的依赖

目前许多框架都是按照以下方式工作的：向类路径中添加一个 JAR 文件(比如 fastjsonlib.jar)，从而获得更多的功能。当 fastjsonlib.jar 不可用时，框架就会使用回退机制或者不提供增强的功能。框架对 fastjsonlib 存在可选的依赖关系, 如果应用程序已经使用了 fastjsonlib，那么框架也使用它，否则就不会使用。
