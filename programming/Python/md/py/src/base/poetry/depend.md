# 管理依赖包

这是 Poetry 最核心的功能，它会自动帮你处理依赖冲突，并更新 poetry.lock 文件以锁定版本。

## 安装生产环境依赖

```sh
poetry add requests
```

这相当于 `pip install requests`，但它会自动将 requests 添加到 pyproject.toml 并更新 poetry.lock。

## 安装开发环境依赖（如测试框架、格式化工具）

```sh
poetry add pytest --group dev
```

这些包只在开发时需要，生产部署时可以跳过。

## 移除依赖

```sh
poetry remove requests
```

## 查看已安装的依赖树

```sh
poetry show --tree
```

## 克隆与部署现有项目

当你从 GitHub 上克隆了一个使用 Poetry 管理的项目（包含 pyproject.toml 和 poetry.lock）后，你只需要在项目根目录下运行一条命令：

```sh
poetry install
```

Poetry 会读取 poetry.lock 文件，严格按照锁定的版本安装所有依赖，确保你的运行环境与原作者完全一致。

## 生产环境部署

如果你在生产服务器上部署，不需要安装开发依赖，可以运行

```sh
poetry install --without dev
```

## 更新依赖版本

如果你的包有安全更新或你想升级所有依赖，可以使用：

```sh
poetry update
```

这会根据 pyproject.toml 中允许的版本范围，升级依赖包并重新生成 poetry.lock 文件。

如果你只想更新特定的包，可以运行：

```sh
poetry update requests
```
