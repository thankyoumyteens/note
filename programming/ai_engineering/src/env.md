# 搭建开发环境

使用 python3.11

## 获取硅基流动的 API 密钥

1. 打开 [硅基流动官网](https://cloud.siliconflow.cn/me/models)
2. 注册/登录账号并实名认证
3. 进入 "账户管理 -> API 密钥"
4. 点击 "新建 API 密钥"

## 统一管理密钥

这是目前整个后端开发圈（无论是 Python 还是 Java/Node.js）管理密钥的绝对标准做法。你的代码里一行环境变量都不用配，全部抽离到一个专门的文件里。

### 1. 安装依赖

```sh
pip install python-dotenv
```

### 2. 在项目根目录新建一个名为 .env 的文件

```sh
# 你的密钥
API_KEY=sk-xxxxxxxxxxxxxxxxx
```

极度重要：一定要把 `.env` 加到你的 `.gitignore` 文件里，绝不能提交到 Git 仓库！

### 3. 在 Python 代码里优雅地调用

以后无论新建多少个文件，只需要在最顶部加两行代码，它就会自动把 `.env` 里的变量全部“吸”进系统的环境变量里：

```py
import os
from dotenv import load_dotenv

# 自动寻找项目根目录的 .env 文件并加载
load_dotenv()

# 现在你可以直接安全地拿来用了
SILICON_FLOW_API_KEY = os.environ.get("API_KEY")
print("API Key 加载成功！")
```

### 4. 抽取全局初始化模块

在你的项目根目录下，新建一个专门的文件，比如叫 env_setup.py。

```py
import os
from dotenv import load_dotenv

# 1. 清理终端的代理
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)

# 2. 加载 .env 文件里的安全环境变量
load_dotenv()
```

### 5. 使用全局初始化模块

以后你在这个项目里新建任何 Python 脚本，只需要在第一行写上这一句：

```py
import env_setup  # 🌟 必须放在第一行！它会自动执行里面的清理和加载逻辑

from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
# ... 干净清爽地开始写业务代码 ...
```
