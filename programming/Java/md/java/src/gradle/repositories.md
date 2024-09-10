# 设置国内源

## 全局设置

在 `GRADLE_USER_HOME` 目录(默认是`~/.gradle/`)下创建 `init.gradle` 文件:

```groovy
// 应用到项目中所有的子项目(subprojects)
allprojects{
    // 项目的仓库设置
    repositories {
        // 华为云仓库
        maven {
            url 'https://mirrors.huaweicloud.com/repository/maven/'
        }
    }
    // 配置构建脚本(即 Gradle 自身的类路径和插件)的仓库
    buildscript {
        repositories {
            // 华为云仓库
            maven {
                url 'https://mirrors.huaweicloud.com/repository/maven/'
            }
        }
    }
}
```

另外, gradle 下载的依赖存放在 `$GRADLE_USER_HOME/.gradle/caches/modules-2/files-2.1` 目录下。

## 单个项目设置

在 `build.gradle` 文件中配置 `repositories` 块:

```groovy
repositories {
    // 阿里云仓库
    maven {
        url "https://maven.aliyun.com/repository/public/"
    }
    // 本地仓库
    mavenLocal()
    // 中央仓库
    mavenCentral()
}
```

如果在`init.gradle`配置了仓库, 那么这里的配置会失效。
