# 基于 MCP 接入自定义工具

### 第一阶段：初始化项目与环境隔离

在你的 macOS 系统中，为这个独立的数据库技能创建一个专属的工作空间。

**1. 创建并进入目录**

```bash
mkdir -p ~/ai_agent_skills/sqlite_memory
cd ~/ai_agent_skills/sqlite_memory
```

**2. 创建并激活虚拟环境 (venv)**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. 安装核心依赖**

```bash
# 由于我们要走 MCP 协议，只需安装官方包即可：
pip install mcp
```

---

### 第二阶段：编写 SQLite 读写服务代码

在 `~/ai_agent_skills/sqlite_memory` 目录下新建 `server.py`。

这里我们会通过 `FastMCP` 暴露两个 `@mcp.tool()`：一个负责存，一个负责取。脚本会在启动时自动初始化数据库表。

```python
# server.py
from mcp.server.fastmcp import FastMCP
import sqlite3
import os

# 初始化 MCP Server
mcp = FastMCP("SQLiteMemoryManager")

# 设定数据库文件存放路径（存放在当前运行目录下）
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_memory.db")

def init_db():
    """初始化数据库，如果表不存在则创建"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# 启动时确保数据库已就绪
init_db()

@mcp.tool()
def save_text_to_db(topic: str, content: str) -> str:
    """
    当用户要求你记住某些重要信息、代码规范或项目设定时调用此技能。
    将文本内容保存到 SQLite 数据库中进行持久化存储。
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO memories (topic, content) VALUES (?, ?)",
                (topic, content)
            )
            conn.commit()
        return f"✅ 成功将主题为 '{topic}' 的内容保存至数据库。"
    except Exception as e:
        return f"❌ 保存失败: {str(e)}"

@mcp.tool()
def read_text_from_db(topic: str) -> str:
    """
    当需要回忆、查询之前保存的某个主题信息时调用此技能。
    根据主题(topic)从 SQLite 数据库中检索相关文本。
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # 使用 LIKE 进行模糊匹配，方便 AI 召回
            cursor.execute(
                "SELECT content, created_at FROM memories WHERE topic LIKE ? ORDER BY created_at DESC",
                (f"%{topic}%",)
            )
            rows = cursor.fetchall()

        if not rows:
            return f"⚠️ 数据库中没有找到关于 '{topic}' 的记录。"

        result = f"🔍 找到关于 '{topic}' 的历史记录：\n"
        for idx, (content, created_at) in enumerate(rows, 1):
            result += f"--- 记录 {idx} ({created_at}) ---\n{content}\n"

        return result
    except Exception as e:
        return f"❌ 读取失败: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

---

### 第三阶段：挂载带有 venv 绝对路径的技能

为了确保 AI 客户端后台启动该 Python 进程时不会报错，我们必须使用刚刚创建的虚拟环境中的解释器绝对路径。

假设你的 macOS 用户名是 `walter`，那么 Python 解释器的绝对路径就是：
`/Users/walter/ai_agent_skills/sqlite_memory/venv/bin/python`

#### 方案 A：针对官方版 Claude Code

找到你的全局配置文件(官方 Claude Code： 通常位于 `~/.claude.json` 或 `~/.config/claude/claude.json`)

使用 Vim 或任意文本编辑器打开该文件，找到或创建一个名为 mcpServers 的顶级字段，将你的技能挂载进去：

```json
{
  "mcpServers": {
    "global_sqlite_memory": {
      "command": "/Users/walter/ai_agent_skills/sqlite_memory/venv/bin/python",
      "args": ["/Users/walter/ai_agent_skills/sqlite_memory/server.py"]
    }
  }
}
```

#### 方案 B：针对 OpenCode 等魔改版客户端

打开项目根目录下的 `.mcp.json`，将以下内容追加进配置：

```json
{
  "mcpServers": {
    "sqlite_memory": {
      "command": "/Users/walter/ai_agent_skills/sqlite_memory/venv/bin/python",
      "args": ["/Users/walter/ai_agent_skills/sqlite_memory/server.py"]
    }
  }
}
```

---

### 第四阶段：实战验收

彻底退出并重启你的 AI 终端客户端。现在的 Agent 已经拥有了读写外部数据库的“超级外挂”。

进入 Claude Code 后输入 `/mcp` 可以看到 `sqlite_memory`。

**测试写入：**

输入指令：_“记住当前的后端开发规范：所有的时间戳必须使用 ISO 8601 格式，并且返回的 JSON 必须使用驼峰命名法。请把它存起来，主题设为 `backend-specs`。”_

> Agent 会调用 `save_text_to_db`，你在 `~/ai_agent_skills/sqlite_memory` 目录下会看到自动生成的 `agent_memory.db` 文件。

**测试读取：**

你可以清空上下文（比如输入 `/clear`），然后重新问它：
_“帮我查一下数据库，我们之前定的后端时间戳规范是什么？”_

> Agent 会调用 `read_text_from_db`，传入类似于 `backend-specs` 的主题词，从 SQLite 中抽出原文并回答你。
