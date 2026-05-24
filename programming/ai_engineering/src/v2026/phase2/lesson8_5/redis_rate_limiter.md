# 新增 RedisRateLimiter

用 Redis 实现多实例共享的 Fixed Window 限流。

本课使用 Fixed Window：

```text
60 秒内最多允许 N 次
```

Redis 中用计数器表示窗口内调用次数。

为什么使用 Lua 脚本：

```text
INCR 和 EXPIRE 需要作为一个原子逻辑执行
避免高并发下计数器增加了但没设置过期时间
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/service/RedisRateLimiter.java
```

代码：

```java
package com.example.aigateway.service;

import com.example.aigateway.config.RateLimitProperties;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.dto.RateLimitRequest;
import com.example.aigateway.dto.RateLimitResult;
import java.util.List;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.stereotype.Service;

/**
 * Redis 分布式限流器。
 *
 * 当前实现：Fixed Window。
 *
 * 逻辑：
 * - 每个限流 key 在 Redis 中维护一个计数器
 * - 第一次写入时设置过期时间
 * - 窗口期内计数超过 limit，则拒绝
 *
 * 注意：
 * Fixed Window 简单，但窗口边界可能存在突刺。
 * 后续可升级为 Sliding Window 或 Token Bucket。
 */
@Service
public class RedisRateLimiter implements DistributedRateLimiter {

    private final StringRedisTemplate redisTemplate;
    private final RateLimitProperties properties;
    private final RateLimitKeyResolver keyResolver;
    private final DefaultRedisScript<List> script;

    public RedisRateLimiter(
            StringRedisTemplate redisTemplate,
            RateLimitProperties properties,
            RateLimitKeyResolver keyResolver
    ) {
        this.redisTemplate = redisTemplate;
        this.properties = properties;
        this.keyResolver = keyResolver;
        this.script = buildScript();
    }

    /**
     * 统一限流入口。
     *
     * 当前检查三层：
     * 1. 全局限流
     * 2. callType 限流
     * 3. model 限流
     *
     * 任意一层拒绝，整体拒绝。
     */
    @Override
    public RateLimitResult acquire(RateLimitRequest request) {
        if (!properties.isEnabled()) {
            return RateLimitResult.allowed(
                    "rate-limit-disabled",
                    0,
                    Long.MAX_VALUE,
                    0
            );
        }

        RateLimitProperties.Rule defaultRule = properties.getDefaultRule();

        RateLimitResult globalResult = acquireByKey(
                keyResolver.globalKey(),
                defaultRule
        );

        if (!globalResult.allowed()) {
            return globalResult;
        }

        RateLimitProperties.Rule callTypeRule = resolveCallTypeRule(request.callType());

        RateLimitResult callTypeResult = acquireByKey(
                keyResolver.callTypeKey(request),
                callTypeRule
        );

        if (!callTypeResult.allowed()) {
            return callTypeResult;
        }

        // 当前 model 使用 defaultRule。
        // 后续如果要给昂贵模型单独配置阈值，可以增加 modelRules。
        RateLimitResult modelResult = acquireByKey(
                keyResolver.modelKey(request),
                defaultRule
        );

        if (!modelResult.allowed()) {
            return modelResult;
        }

        return modelResult;
    }

    /**
     * 获取 callType 对应规则。
     *
     * 如果没有专门配置，则使用 defaultRule。
     */
    private RateLimitProperties.Rule resolveCallTypeRule(LlmCallType callType) {
        if (callType == null) {
            return properties.getDefaultRule();
        }

        return properties.getCallTypeRules().getOrDefault(
                callType,
                properties.getDefaultRule()
        );
    }

    /**
     * 对单个 Redis key 执行限流。
     */
    private RateLimitResult acquireByKey(
            String key,
            RateLimitProperties.Rule rule
    ) {
        List<Long> result = redisTemplate.execute(
                script,
                List.of(key),
                String.valueOf(rule.limit()),
                String.valueOf(rule.windowSeconds())
        );

        if (result == null || result.size() < 3) {
            throw new IllegalStateException("Redis rate limit script returned invalid result");
        }

        long allowed = result.get(0);
        long current = result.get(1);
        long ttlSeconds = result.get(2);

        if (allowed == 1) {
            return RateLimitResult.allowed(
                    key,
                    current,
                    rule.limit(),
                    ttlSeconds
            );
        }

        return RateLimitResult.rejected(
                key,
                current,
                rule.limit(),
                ttlSeconds
        );
    }

    /**
     * Redis Lua 脚本。
     *
     * 返回：
     * [allowed, current, ttl]
     */
    private DefaultRedisScript<List> buildScript() {
        String lua = """
                local current = redis.call('INCR', KEYS[1])

                if current == 1 then
                    redis.call('EXPIRE', KEYS[1], tonumber(ARGV[2]))
                end

                local ttl = redis.call('TTL', KEYS[1])

                if current > tonumber(ARGV[1]) then
                    return {0, current, ttl}
                end

                return {1, current, ttl}
                """;

        DefaultRedisScript<List> redisScript = new DefaultRedisScript<>();
        redisScript.setScriptText(lua);
        redisScript.setResultType(List.class);

        return redisScript;
    }
}
```

#### 代码说明

本实现会依次检查：

```text
global
callType
model
```

任何一个 key 超限，都返回 rejected。

注意：这会让每次模型调用写入 3 个 Redis key。这是为了清楚演示多维度限流。生产环境可以根据成本和需要裁剪。
