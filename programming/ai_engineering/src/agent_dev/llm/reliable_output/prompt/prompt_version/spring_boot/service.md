# IntentClassificationService

替换前文 WebClient 版本的 Service。Service 不再直接注入某个模板和示例，而是使用应用启用版本从 Registry 精确取得完整定义。

```java
package com.example.llm.service;

import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.prompt.PromptDefinition;
import com.example.llm.prompt.PromptRegistry;
import com.example.llm.prompt.PromptRenderer;
import com.example.llm.prompt.PromptSelection;
import com.example.llm.prompt.RenderedPrompt;
import com.example.llm.provider.ProviderFallbackRouter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * 解析当前 Prompt 版本，渲染消息并调用统一 Provider Router。
 */
@Service
public class IntentClassificationService {

    // 仅在 DEBUG 级别输出实际发送的 Prompt，便于本地调试。
    private static final Logger log = LoggerFactory.getLogger(IntentClassificationService.class);

    // 将模板变量渲染为最终 system、user 消息。
    private final PromptRenderer renderer;
    // 保存所有可用的不可变 Prompt 版本。
    private final PromptRegistry registry;
    // 应用配置指定的当前意图识别版本。
    private final PromptSelection selection;
    // 复用前文的异步重试和 Provider 降级入口。
    private final ProviderFallbackRouter router;

    public IntentClassificationService(
            PromptRenderer renderer,
            PromptRegistry registry,
            @Qualifier("intentClassifierSelection") PromptSelection selection,
            ProviderFallbackRouter router
    ) {
        this.renderer = renderer;
        this.registry = registry;
        this.selection = selection;
        this.router = router;
    }

    public Mono<UnifiedChatResponse> classify(
            String userInput,
            String requestId,
            String traceId
    ) {
        if (userInput == null || userInput.isBlank()) {
            return Mono.error(new IllegalArgumentException("userInput must not be blank"));
        }
        if (requestId == null || requestId.isBlank()) {
            return Mono.error(new IllegalArgumentException("requestId must not be blank"));
        }
        if (traceId == null || traceId.isBlank()) {
            return Mono.error(new IllegalArgumentException("traceId must not be blank"));
        }

        PromptDefinition definition = registry.require(selection);
        RenderedPrompt prompt = renderer.render(
                definition.template(),
                Map.of("user_input", userInput)
        );

        List<UnifiedChatMessage> messages = new ArrayList<>(definition.examples());
        // 当前输入始终位于该版本的全部 Few-shot 示例之后。
        messages.add(UnifiedChatMessage.user(prompt.user()));

        UnifiedChatRequest request = new UnifiedChatRequest(
                prompt.system(),
                messages,
                new UnifiedChatRequest.LlmGenerationOptions(0.0, 300, null),
                Map.of(
                        "requestId", requestId,
                        "traceId", traceId,
                        "promptName", prompt.promptName(),
                        "promptVersion", prompt.promptVersion()
                )
        );

        log.debug(
                "Rendered prompt: name={}, version={}, system={}, messages={}",
                prompt.promptName(),
                prompt.promptVersion(),
                prompt.system(),
                messages
        );

        return router.chat(request);
    }
}
```

本地调试时开启该 Service 的 DEBUG 日志：

```yaml
logging:
  level:
    com.example.llm.service.IntentClassificationService: DEBUG
```

Controller 和测试请求不变。调用 `v1` 时只发送当前输入；调用 `v2` 时先发送三组示例。两者都会把实际解析到的版本写入 metadata。日志包含用户输入，只应在受控调试环境开启。
