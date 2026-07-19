# IntentClassificationService

```java
package com.example.llm.service;

import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.prompt.VersionedPromptTemplate;
import com.example.llm.prompt.VersionedPromptTemplate.RenderedPrompt;
import com.example.llm.router.ProviderFallbackRouter;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

/**
 * 使用 Spring AI PromptTemplate 渲染意图识别请求。
 */
@Service
public class IntentClassificationService {

    // 意图识别任务使用的带版本模板。
    private final VersionedPromptTemplate template;
    // 复用前文 Spring AI 版本的同步 Provider 降级链。
    private final ProviderFallbackRouter router;

    public IntentClassificationService(
            @Qualifier("intentClassifierPrompt") VersionedPromptTemplate template,
            ProviderFallbackRouter router
    ) {
        this.template = template;
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

        RenderedPrompt prompt = template.render(
                Map.of("user_input", userInput)
        );

        UnifiedChatRequest request = new UnifiedChatRequest(
                prompt.system(),
                List.of(UnifiedChatMessage.user(prompt.user())),
                new UnifiedChatRequest.LlmGenerationOptions(0.0, 300, null),
                Map.of(
                        "requestId", requestId,
                        "traceId", traceId,
                        "promptName", prompt.promptName(),
                        "promptVersion", prompt.promptVersion()
                )
        );

        return router.chat(request);
    }
}
```

Service 只负责模板渲染和统一请求组装。实际 Spring AI 调用、超时、重试、降级和调用记录仍由前文的 `SpringAiProviderClient` 与 `ProviderFallbackRouter` 处理。
