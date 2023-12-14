# 解决Tomcat控制台中文乱码

- Run -> Edit Configurations, 修改当前 Web 项目 Tomcat Server 的虚拟机输出选项 VM options 添加 -Dfile.encoding=UTF-8
- File -> Settings -> Editor -> File Encodings, 分别将 Global Encoding、Project Encoding、Default encoding for properties files 都设置为 UTF-8
- Help -> Etit Custom VM Options, 在 idea64.exe.vmoptions 文件尾加上-Dfile.encoding=UTF-8
- 重启idea
