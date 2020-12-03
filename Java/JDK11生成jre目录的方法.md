JDK11 下没有jre,需要手动生成。

在jdk目录下执行 
```
.\bin\jlink.exe --module-path jmods --add-modules java.desktop --output jre
```
