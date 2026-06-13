# API Key 配置与安全管理

API Key 可以理解成：

> 你的后端系统调用大模型 API 时使用的“身份凭证”。

它类似密码。谁拿到你的 API Key，谁就可能以你的账号调用模型，产生费用，甚至访问部分项目资源。所以 API Key 管理不是小事，尤其是做 Agent / RAG / 企业应用时。

## API Key 不要写死在代码里

错误写法：

```java
// 错误示例：不要把 API Key 写死在代码里。
String apiKey = "sk-xxxxxxxxxxxxxxxx";
```

这样做的问题是：

1. 容易被提交到 Git
2. 容易被同事、截图、日志泄露
3. 换 Key 时必须改代码重新部署
4. 泄露后别人可以直接盗用你的额度

正确做法是放到环境变量：

```bash
export OPENAI_API_KEY="sk-xxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxx"
export DASHSCOPE_API_KEY="sk-xxxx"
export DEEPSEEK_API_KEY="sk-xxxx"
```

然后在配置文件中读取环境变量：

```yaml
llm:
  providers:
    openai:
      api-key: ${OPENAI_API_KEY}
    claude:
      api-key: ${ANTHROPIC_API_KEY}
    qwen:
      api-key: ${DASHSCOPE_API_KEY}
    deepseek:
      api-key: ${DEEPSEEK_API_KEY}
```

## 为什么推荐环境变量

环境变量的好处是：

1. 代码仓库里不会出现真实 Key
2. 不同环境可以使用不同 Key
3. 本地、测试、生产配置可以隔离
4. 换 Key 不需要改 Java 代码
5. 更容易接入 Docker / K8s / CI/CD

## 本地开发怎么设置 API Key

### macOS / Linux

临时设置：

```bash
export OPENAI_API_KEY="sk-xxxx"
```

这种只对当前终端有效。

长期设置可以写进：

```bash
~/.zshrc
```

例如：

```bash
export OPENAI_API_KEY="sk-xxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxx"
```

然后执行：

```bash
source ~/.zshrc
```

### IntelliJ IDEA

可以在 Run Configuration 里配置：

```text
Run/Debug Configurations
  ↓
Environment variables
  ↓
OPENAI_API_KEY=sk-xxxx;ANTHROPIC_API_KEY=sk-ant-xxxx
```

这种方式适合本地开发，不会污染代码。

## 不要把 API Key 放进前端

非常重要：

> API Key 只能放后端，不能放浏览器、iOS、Android、小程序、桌面前端里。

前端只调用你自己的后端：

```text
POST /api/llm/chat
```

真正的模型 API Key 只存在于 Spring Boot 后端环境里。

---

## 不要提交到 Git

不要把这些文件提交到 Git：

```text
.env
.env.local
application-local.yml
application-secret.yml
```

`.gitignore` 里应该加：

```gitignore
.env
.env.*
application-local.yml
application-secret.yml
```

但可以提交模板文件：

```text
.env.example
```

例如：

```bash
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DASHSCOPE_API_KEY=your_dashscope_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

模板里只放占位符，不放真实 Key。

## 不要打印 API Key 到日志

错误写法：

```java
// 错误示例：不要打印完整 API Key。
log.info("Using OpenAI API key: {}", config.apiKey());
```

正确写法：

```java
/**
 * 对 API Key 做脱敏展示。
 * 只保留前后少量字符，避免日志泄露完整密钥。
 */
private String maskApiKey(String apiKey) {
    if (apiKey == null || apiKey.length() < 8) {
        return "****";
    }

    return apiKey.substring(0, 4) + "****" + apiKey.substring(apiKey.length() - 4);
}
```

日志里最多打印：

```text
sk-p****abcd
```

不要打印完整 Key。

## 每个环境使用不同 API Key

不要所有环境共用一个 Key。

推荐：

- dev → 开发环境 Key
- test → 测试环境 Key
- staging → 预发布环境 Key
- prod → 生产环境 Key

原因：

1. 开发环境泄露不影响生产
2. 测试调用不会污染生产成本统计
3. 可以单独限流
4. 可以单独停用
5. 方便排查是谁在调用

## 不要多人共用一个 API Key

团队开发时，不建议所有人共用同一个 sk-xxx。

推荐：

- 每个人一个 Key
- 每个服务一个 Key
- 每个环境一个 Key

好处是：

1. 谁泄露了容易追踪
2. 谁调用多容易统计
3. 可以单独禁用某个人或某个服务的 Key
4. 权限可以单独控制

## 使用最小权限原则

如果平台支持权限控制，不要给所有 Key 全权限。

生产中建议：

- 普通聊天服务：只给调用模型需要的权限
- 后台管理服务：单独 Key
- 实验脚本：单独 Key
- CI/CD：单独 Key

不要让一个 Key 同时拥有所有项目、所有模型、所有工具权限。

## API Key 泄露后怎么处理

一旦怀疑泄露，步骤是：

1. 立即删除或禁用旧 Key
2. 创建新 Key
3. 更新服务器环境变量
4. 重启服务或刷新配置
5. 检查账单和调用日志
6. 排查泄露来源
7. 清理 Git 历史或公开位置

## 生产环境更推荐 Secret Manager

简单项目可以用环境变量。

但生产环境更推荐：

- AWS Secrets Manager
- Google Secret Manager
- Azure Key Vault
- Kubernetes Secret
- Vault
- CI/CD Secret Variables

不要把 Key 写进：

- Dockerfile
- docker-compose.yml 明文
- Kubernetes YAML 明文
- GitHub Actions 普通变量
- 服务器脚本明文

Docker 错误示例：

```dockerfile
# 错误示例：不要把 Key 写进镜像。
ENV OPENAI_API_KEY=sk-xxxx
```

更好的方式是运行时注入：

```bash
docker run \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  your-app:latest
```

Kubernetes 可以用 Secret 注入环境变量：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: llm-api-keys
type: Opaque
stringData:
  OPENAI_API_KEY: "sk-xxxx"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: app
          image: your-app:latest
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: llm-api-keys
                  key: OPENAI_API_KEY
```

注意：真实生产里 Secret YAML 本身也不要明文提交到 Git。
