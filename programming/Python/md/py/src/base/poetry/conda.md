# Poetry 与 Miniconda 结合使用

强制关闭 Poetry 创建虚拟环境的功能：如果你主要依赖 Conda 来管理环境，可以直接告诉 Poetry：“如果当前已经有激活的虚拟环境了，就不要再自己建了。”

```sh
# 仅针对当前项目关闭（会在项目根目录生成 poetry.toml 配置文件）
poetry config virtualenvs.create false --local

# 或者全局关闭（以后所有的 Poetry 项目都不再自动创建虚拟环境）
poetry config virtualenvs.create false
```

设置完成后，只要你处于 `conda activate` 的状态下，Poetry 就会自动把你安装的包放入 Conda 环境中。
