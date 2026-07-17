# IntentClassificationService

```java
package com.example.llm.service;

import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.prompt.PromptRenderer;
import com.example.llm.prompt.PromptTemplate;
import com.example.llm.prompt.RenderedPrompt;
import com.example.llm.provider.ProviderFallbackRouter;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.List;
import java.util.Map;

/**
 * 渲染意图识别 Prompt，并复用统一 Provider 降级链发起调用。
 */
@Service
public class IntentClassificationService {

    // 将模板变量渲染为最终消息。
    private final PromptRenderer renderer;
    // 意图识别任务使用的模板。
    private final PromptTemplate template;
    // 复用前文的超时、重试和 Provider 降级入口。
    private final ProviderFallbackRouter router;

    public IntentClassificationService(
            PromptRenderer renderer,
            @Qualifier("intentClassifierPrompt") PromptTemplate template,
            ProviderFallbackRouter router
    ) {
        this.renderer = renderer;
        this.template = template;
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

        RenderedPrompt prompt = renderer.render(
                template,
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

Service 只增加模板渲染和统一请求组装。Provider 选择、重试、降级、延迟与调用记录继续由 `ProviderFallbackRouter` 处理。
