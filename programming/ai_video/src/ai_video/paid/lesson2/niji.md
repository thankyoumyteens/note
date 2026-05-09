# niji 简介

niji 是 Midjourney 体系里偏二次元、动漫、亚洲审美插画方向的模型。niji 官方说明，使用 niji 7 时可以在 Discord 的 prompt 后面输入 `--niji 7`。Midjourney 的更新页也说明 niji V7 面向 Asia and Anime，并提升了 anime coherence、prompt understanding 和 sref 表现。

所以本课程第 2 课使用 niji，而不是普通 Midjourney 模型，原因是：

```text
卡提希娅是二次元游戏角色，niji 更适合作为角色标准图生成工具。
```

## niji 的基本 prompt 结构

niji 的 prompt 不应该写成一大段散文，而应该拆成：

```text
参考图链接 + 角色描述 + 画面任务 + 构图要求 + 风格要求 + 参数
```

标准结构：

```text
[参考图链接1] [参考图链接2] 角色描述，画面任务，构图要求，风格要求 --niji 7 --ar 比例 --s 数值 --iw 数值 --no 排除项
```

例子：

```text
[参考图链接1] [参考图链接2] Cartethyia from Wuthering Waves, elegant anime game character, front view upper body portrait, clean simple background --niji 7 --ar 2:3 --s 100 --iw 1.5 --no text, logo, watermark
```

## niji 的参考图用法

做指定角色时，建议使用参考图。Midjourney 官方文档说明，图片提示可以作为 prompt 的一部分；`--iw` 可以控制图片提示对最终结果的影响，数值越高，参考图影响越大。官方文档也列出 Version 7 / Version 6 / Niji 6 的 image weight 默认值为 1，范围为 0–3。

对本课程来说，建议这样用：

```text
第一次生成：--iw 1.5
如果角色不像：提高到 --iw 2
如果画面太像原图、构图不听话：降低到 --iw 1
```

建议每次只放 **2–3 张参考图**，不要一次塞 8 张。参考图太多时，模型容易混乱。

推荐组合：

```text
正面半身：正面图 + 官方全身图
全身标准图：官方全身图 + 游戏内模型图
侧脸近景：侧脸图 + 正面脸图
背影标准图：背面图 + 官方全身图
眼部特写：脸部特写 + 正面图
持剑中景：官方展示图 + 全身图
```

## niji 的负面词不是单独输入框

niji / Midjourney 没有专门的“负面词输入框”。正确方式是在 prompt 末尾加：

```text
--no
```

Midjourney 官方文档说明，`--no` 用来告诉 Midjourney 不要生成哪些元素。

正确写法：

```text
--no text, logo, watermark, school uniform, boots, staff, gun, bow, scythe
```

不要写成：

```text
no random anime girl, no short hair, no missing crown...
```

因为这不是 niji 的最佳参数写法。

## niji 的负面词要短

第 2 课不要把所有负面词都塞进去。

错误写法：

```text
--no random anime girl, short hair, silver gray hair, pink hair, human ears, missing crown, golden crown, simple tiara, missing blue earrings, school uniform, casual outfit, modern dress, cyberpunk bodysuit, heavy armor, boots, staff, gun, bow, scythe, red fire effects, logo, text, watermark, overly mature face, childish face, exaggerated sexy expression, simplified white dress
```

问题是太长，容易稀释重点。

正确策略是：

```text
正向 prompt 负责告诉模型“要什么”
--no 只排除最容易出现、最致命的错误
```

第 2 课统一使用这个短负面参数：

```text
--no text, logo, watermark, school uniform, casual outfit, boots, staff, gun, bow, scythe
```

如果某一轮出现具体错误，再追加针对性负面项：

```text
头冠变金色：--no golden crown
变成短发：--no short hair
变成靴子：--no boots
出现现代衣服：--no modern outfit
```

## 本课常用参数

本课只用 5 个参数。

### `--niji 7`

指定使用 niji 7。

```text
--niji 7
```

---

### `--ar`

控制画面比例。

角色标准图建议：

```text
--ar 2:3
```

横屏视频关键帧建议：

```text
--ar 16:9
```

本课主要做角色标准图，所以优先用：

```text
--ar 2:3
```

---

### `--s`

控制风格化强度。

建议从：

```text
--s 100
```

开始。

如果画面太自由、角色不像，降低到：

```text
--s 50
```

如果角色已经稳定，但想更华丽，再尝试：

```text
--s 150
```

第 2 课不建议一开始超过 `--s 200`。

---

### `--iw`

控制参考图影响力。

建议从：

```text
--iw 1.5
```

开始。

如果不像卡提希娅，试：

```text
--iw 2
```

如果构图太像参考图、缺少变化，试：

```text
--iw 1
```

---

### `--no`

排除不想要的元素。

统一基础版：

```text
--no text, logo, watermark, school uniform, casual outfit, boots, staff, gun, bow, scythe
```
