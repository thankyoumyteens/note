# IntentClassificationService

替换前文 Spring AI 版本的 Service。版本选择发生在统一请求组装之前，ProviderClient 仍通过 Spring AI 执行模型调用。

```java
package com.example.llm.service;

import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.prompt.PromptDefinition;
import com.example.llm.prompt.PromptRegistry;
import com.example.llm.prompt.PromptSelection;
import com.example.llm.prompt.VersionedPromptTemplate.RenderedPrompt;
import com.example.llm.router.ProviderFallbackRouter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * 解析当前 Spring AI Prompt 版本并调用统一 Provider Router。
 */
@Service
public class IntentClassificationService {

    // 仅在 DEBUG 级别输出实际发送的 Prompt，便于本地调试。
    private static final Logger log = LoggerFactory.getLogger(IntentClassificationService.class);

    // 保存所有可用的不可变 Prompt 版本。
    private final PromptRegistry registry;
    // 应用配置指定的当前意图识别版本。
    private final PromptSelection selection;
    // 复用前文 Spring AI 版本的同步 Provider 降级入口。
    private final ProviderFallbackRouter router;

    public IntentClassificationService(
            PromptRegistry registry,
            @Qualifier("intentClassifierSelection") PromptSelection selection,
            ProviderFallbackRouter router
    ) {
        this.registry = registry;
        this.selection = selection;
        this.router = router;
    }

    public UnifiedChatResponse classify(
            String userInput,
            String requestId,
            String traceId
    ) {
        if (userInput == null || userInput.isBlank()) {
            throw new IllegalArgumentException("userInput must not be blank");
        }
        if (requestId == null || requestId.isBlank()) {
            throw new IllegalArgumentException("requestId must not be blank");
        }
        if (traceId == null || traceId.isBlank()) {
            throw new IllegalArgumentException("traceId must not be blank");
        }

        PromptDefinition definition = registry.require(selection);
        RenderedPrompt prompt = definition.template().render(
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

Controller、ProviderClient、重试和降级逻辑不变。Spring AI 接收到的消息顺序由统一 `UnifiedChatRequest` 保证。日志包含用户输入，只应在受控调试环境开启。
