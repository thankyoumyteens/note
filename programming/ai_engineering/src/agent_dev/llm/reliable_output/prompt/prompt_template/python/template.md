# PromptTemplate 与 PromptRenderer

prompt_template.py

```py
from __future__ import annotations

from dataclasses import dataclass
from string import Template
from typing import Mapping


@dataclass(frozen=True)
class PromptTemplate:
    """带名称和版本的 Prompt 模板。"""

    name: str  # Prompt 名称，例如 intent-classifier。
    version: str  # Prompt 版本，例如 v1。
    system_template: str  # system prompt 模板。
    user_template: str  # user prompt 模板。

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("name must not be blank")
        if not self.version or not self.version.strip():
            raise ValueError("version must not be blank")
        if not self.system_template or not self.system_template.strip():
            raise ValueError("system_template must not be blank")
        if not self.user_template or not self.user_template.strip():
            raise ValueError("user_template must not be blank")

        if not Template(self.system_template).is_valid():
            raise ValueError("system_template contains invalid placeholders")
        if not Template(self.user_template).is_valid():
            raise ValueError("user_template contains invalid placeholders")


@dataclass(frozen=True)
class RenderedPrompt:
    """一次模板渲染后的最终 Prompt。"""

    prompt_name: str  # 本次使用的 Prompt 名称。
    prompt_version: str  # 本次使用的 Prompt 版本。
    system: str  # 渲染后的 system 消息。
    user: str  # 渲染后的 user 消息。

    def __post_init__(self) -> None:
        if not self.prompt_name or not self.prompt_name.strip():
            raise ValueError("prompt_name must not be blank")
        if not self.prompt_version or not self.prompt_version.strip():
            raise ValueError("prompt_version must not be blank")
        if not self.system or not self.system.strip():
            raise ValueError("system must not be blank")
        if not self.user or not self.user.strip():
            raise ValueError("user must not be blank")


class PromptRenderer:
    """校验变量并渲染 system、user 模板。"""

    def render(
        self,
        prompt_template: PromptTemplate,
        variables: Mapping[str, str],
    ) -> RenderedPrompt:
        if not isinstance(prompt_template, PromptTemplate):
            raise ValueError("prompt_template must be a PromptTemplate")

        safe_variables = dict(variables or {})
        system_template = Template(prompt_template.system_template)
        user_template = Template(prompt_template.user_template)
        required = set(system_template.get_identifiers()) | set(
            user_template.get_identifiers()
        )

        self._validate_variables(required, safe_variables)

        return RenderedPrompt(
            prompt_name=prompt_template.name,
            prompt_version=prompt_template.version,
            system=system_template.substitute(safe_variables),
            user=user_template.substitute(safe_variables),
        )

    @staticmethod
    def _validate_variables(
        required: set[str],
        actual: dict[str, str],
    ) -> None:
        missing = required - actual.keys()
        if missing:
            raise ValueError(f"Missing prompt variables: {sorted(missing)}")

        unused = actual.keys() - required
        if unused:
            raise ValueError(f"Unused prompt variables: {sorted(unused)}")

        for name in required:
            value = actual[name]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Prompt variable must not be blank: {name}")
```

`string.Template` 使用 `$variable` 或 `${variable}` 占位符。`substitute()` 会在变量缺失时失败；这里还主动拒绝多余变量和空值，避免变量名写错后静默生成错误 Prompt。
