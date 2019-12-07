# Eclipse无法正常启动，弹出对话框内容为 A Java Runtime...

* 找到你安装的jdk，找到bin目录，复制路径: `jdk1.8.0_232/bin`
* 找到你的eclipse安装地方： 找到`eclipse.ini`文件 
* 用记事本或者其他软件打开，在`openFile`下方加入你的jdk安装的路径。
* 点击保存，从新打开eclipse
```
-startup
plugins/org.eclipse.equinox.launcher_1.5.500.v20190715-1310.jar
--launcher.library
plugins/org.eclipse.equinox.launcher.win32.win32.x86_64_1.1.1100.v20190907-0426
-product
org.eclipse.epp.package.jee.product
-showsplash
org.eclipse.epp.package.common
--launcher.defaultAction
openFile
--launcher.defaultAction
openFile
-vm
jdk1.8.0_232/bin
--launcher.appendVmargs
-vmargs
-Dosgi.requiredJavaVersion=1.8
-Dosgi.instance.area.default=@user.home/eclipse-workspace
-XX:+UseG1GC
-XX:+UseStringDeduplication
--add-modules=ALL-SYSTEM
-Dosgi.requiredJavaVersion=1.8
-Dosgi.dataAreaRequiresExplicitInit=true
-Xms256m
-Xmx1024m
--add-modules=ALL-SYSTEM
```
