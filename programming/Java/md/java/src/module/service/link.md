# 链接多模块

jlink 会根据 `requires` 声明自动把 user.use 模块依赖的 data.transfer.api 模块包含在映像中, 但是不会根据 `uses` 声明自动将服务提供者 data.transfer.computer 包含在映像中, 需要手动添加。

```sh
jlink --module-path out/:$JAVA_HOME/jmods \
    --add-modules user.use,data.transfer.computer \
    --launcher run_app=user.use/com.example.use.Main \
    --output transfer-image
```

运行

```sh
./transfer-image/bin/run_app
```
