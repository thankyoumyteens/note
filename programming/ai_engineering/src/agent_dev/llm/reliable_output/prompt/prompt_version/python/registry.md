# PromptRegistry

prompt_registry.py

```py
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from llm_api_demo.prompt_template import PromptTemplate
from llm_api_demo.schemas import ChatRole, UnifiedChatMessage


@dataclass(frozen=True)
class PromptDefinition:
    """一个不可变的完整 Prompt 版本。"""

    template: PromptTemplate  # 带名称和版本的 Prompt 模板。
    examples: tuple[UnifiedChatMessage, ...] = ()  # 该版本的 Few-shot 消息。

    def __post_init__(self) -> None:
        if not isinstance(self.template, PromptTemplate):
            raise ValueError("template must be a PromptTemplate")

        examples = tuple(self.examples or ())
        if len(examples) % 2 != 0:
            raise ValueError("Few-shot messages must contain complete pairs")

        for index in range(0, len(examples), 2):
            if (
                examples[index].role is not ChatRole.USER
                or examples[index + 1].role is not ChatRole.ASSISTANT
            ):
                raise ValueError(
                    "Few-shot messages must alternate USER and ASSISTANT"
                )

        object.__setattr__(self, "examples", examples)


@dataclass(frozen=True)
class PromptSelection:
    """应用当前启用的 Prompt 名称和版本。"""

    name: str  # Prompt 稳定名称。
    version: str  # 当前启用版本。

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("name must not be blank")
        if not self.version or not self.version.strip():
            raise ValueError("version must not be blank")


class PromptRegistry:
    """按名称和版本精确查找 Prompt 定义的只读注册表。"""

    def __init__(self, definitions: Iterable[PromptDefinition]) -> None:
        index: dict[tuple[str, str], PromptDefinition] = {}

        for definition in definitions:
            if not isinstance(definition, PromptDefinition):
                raise ValueError("definition must be a PromptDefinition")

            key = (definition.template.name, definition.template.version)
            if key in index:
                raise ValueError(f"Duplicate prompt version: {key}")
            index[key] = definition

        if not index:
            raise ValueError("definitions must not be empty")

        # MappingProxyType 防止运行期间修改版本索引。
        self._definitions: Mapping[
            tuple[str, str], PromptDefinition
        ] = MappingProxyType(index)

    def require(self, selection: PromptSelection) -> PromptDefinition:
        """精确取得配置指定的 Prompt 版本。"""
        if not isinstance(selection, PromptSelection):
            raise ValueError("selection must be a PromptSelection")

        key = (selection.name, selection.version)
        try:
            return self._definitions[key]
        except KeyError as exc:
            raise ValueError(f"Prompt version not found: {key}") from exc
```

Registry 不实现最大版本计算或默认回退；应用配置必须引用已经注册的精确版本。
