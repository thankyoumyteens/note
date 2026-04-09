# 写一个简单的 MCP Server

我们将使用官方提供的 mcp 极简框架，写一个暴露本地“祖传订单系统”的独立微服务。

### 1. 安装依赖

安装官方的高级封装库 FastMCP（它就像是 MCP 界的 Spring Boot）：

```sh
pip install mcp
```

### 2. 编写 MCP Server

新建一个文件叫 legacy_order_server.py：

```py
from mcp.server.fastmcp import FastMCP

# 1. 初始化 Server 实例（相当于 @SpringBootApplication）
mcp = FastMCP("LegacyOrderSystem")

# 模拟公司内网的祖传数据库
DB_ORDERS = {
    "ORD-001": {"status": "已发货", "amount": 1250.00},
    "ORD-002": {"status": "风控拦截", "amount": 99999.00}
}


# ==========================================
# 🌟 暴露 Tool (让大模型拥有“写/执行”的能力)
# ==========================================
# 这个装饰器就相当于 Java 里的 @GetMapping("/order")
@mcp.tool()
def get_order_status(order_id: str) -> str:
    """根据订单号查询旧版 ERP 系统的订单状态。"""
    print(f"[底层系统接收到请求] 正在查询订单: {order_id}")
    order = DB_ORDERS.get(order_id)
    return f"订单 {order_id} 状态: {order['status']}，金额: {order['amount']}" if order else "未找到该订单。"


# ==========================================
# 🌟 暴露 Resource (让大模型拥有“只读网盘”的能力)
# ==========================================
# 大模型可以通过这个类似 URI 的路径，瞬间读取公司的内部规定
@mcp.resource("config://company-refund-policy")
def get_refund_policy() -> str:
    """读取公司的退款红线规定"""
    return "高危红线：金额超过 50000 的订单遭遇风控拦截时，绝对不允许直接退款，必须由人工客服介入！"


if __name__ == "__main__":
    # 启动服务器，默认走 stdio（标准输入输出）协议
    mcp.run()
```

## 大模型是如何连上它的？

在 MCP 架构中，最经典、最高效的本地连接方式叫做 Stdio（标准输入输出）协议。不需要开端口，不需要配 Nginx，大模型的客户端程序会直接在后台“唤醒”你的 Python 脚本，并通过终端的黑框框（stdin / stdout）用 JSON-RPC 格式跟它疯狂对话。

如果你电脑上装了 Claude Desktop，你只需要找到它的配置文件 `claude_desktop_config.json`，在里面加一段类似 JDBC URL 的配置：

```json
{
  "mcpServers": {
    "my_legacy_erp": {
      "command": "python",
      "args": ["/your_path/legacy_order_server.py"]
    }
  }
}
```

重启 Claude Desktop。此时你在聊天框里对 Claude 说：“帮我查一下 ORD-002 的状态，并告诉我该怎么处理？”

底层发生的事情：

1. Claude 客户端读取了配置，默默在后台跑起了你的 python legacy_order_server.py。
2. 客户端向 Server 发送 MCP 握手协议，Server 汇报：“我有 `get_order_status` 这个工具，还有 `config://company-refund-policy` 这个资源！”
3. Claude 决定调用工具，终端里瞬间打印出 `[底层系统接收到请求] 正在查询订单: ORD-002`。
4. Claude 拿到返回数据（风控拦截，99999元），它觉得金额太大了，于是又去读取了你暴露的 Resource 资源。
5. 最终，Claude 在界面上回复你：“ORD-002 目前被风控拦截，金额为 99999 元。根据公司规定，超过 5 万的高危订单绝对不能直接退款，我建议您立即转交人工客服介入处理。”
