# springboot获取运行Jar包的目录

```java
//linux和windows下通用
private String getJarFilePath() {
    ApplicationHome home = new ApplicationHome(getClass());
    File jarFile = home.getSource();
    return jarFile.getParentFile().toString();
}
```

如项目为: C:\classes\app.jar, 则函数返回: C:\classes
