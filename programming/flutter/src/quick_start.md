# 基本用法

需要先安装 Android Studio 和 Android SDK

下载并解压 flutter:

[flutter_windows_3.16.9-stable.zip](https://mirrors.tuna.tsinghua.edu.cn/flutter/flutter_infra/releases/stable/windows/flutter_windows_3.16.9-stable.zip)

## 设置环境变量

- Path: 解压位置\flutter\bin
- FLUTTER_STORAGE_BASE_URL: https://mirrors.tuna.tsinghua.edu.cn/flutter
- PUB_HOSTED_URL: https://mirrors.tuna.tsinghua.edu.cn/dart-pub

## 设置 vscode

安装 Flutter 插件

## 设置 idea

安装 Flutter 插件

## vscode 创建项目

1. View -> Command Palette
2. 输入"flutter", 选择 Flutter: New Project
3. 选择 Application
4. 新建或选择新项目将存放的上层目录
5. 输入项目名称, 回车
6. 等待项目创建完成, 并且 main.dart 文件展现在编辑器中

## idea 创建项目

1. New Project
2. 选择 Flutter
3. Flutter SDK Path 中选择 解压位置\flutter 目录
4. 下一步

## 添加安卓模拟器

1. 在 Android Studio 中创建安卓模拟器
2. 选择安卓模拟器, 并启动
3. 点击 vscode 状态栏右下角的 No Device, 选择启动的模拟器
4. 点击 idea 右上角, 选择启动的模拟器

## 设置 gradle

如果在 Android Studio 里设置了代理的话, 就需要注释掉 ~/.gradle/gradle.properties 里面的代理设置:

```conf
# 注意这里在打开Android Studio后会被重新设置
# 需要再次注释

# systemProp.http.proxyHost=127.0.0.1
# systemProp.https.proxyHost=127.0.0.1
# systemProp.https.proxyPort=1080
# systemProp.http.proxyPort=1080
```

找到项目目录下 android/gradle/gradle-wrapper.properties 文件, 根据 distributionUrl 中指定的 gradle 版本号, 下载对应版本的压缩包到本地任一路径下, 然后修改 gradle-wrapper.properties 文件:

```conf
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
# distributionUrl=https\://services.gradle.org/distributions/gradle-7.5-all.zip
distributionUrl=file:///C:/Users/Public/software/gradle-7.5-all.zip
```

找到项目目录下 android/build.gradle 文件, 修改:

```groovy
buildscript {
    ext.kotlin_version = '1.7.10'
    repositories {
        google()
        mavenCentral()
        // 增加这行
        maven { url 'https://mirrors.tuna.tsinghua.edu.cn/flutter/download.flutter.io' }
    }

    dependencies {
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
        // 增加这行
        maven { url 'https://mirrors.tuna.tsinghua.edu.cn/flutter/download.flutter.io' }
    }
}
```

## vscode 运行

1. 启动安卓模拟器
2. vscode 切换到 main.dart 页签
3. Run -> Start Debugging 或按下 F5

## idea 运行

点击 debug 按钮
