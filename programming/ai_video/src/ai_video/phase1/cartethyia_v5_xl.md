# Cartethyia_V5_XL 说明

这个模型是在 civitai.com 上找的。模型地址: [Cartethyia/Fleurdelys | Wuthering Waves (NAI/IL/Pony)](https://civitai.com/models/1112399/cartethyiafleurdelys-or-wuthering-waves-naiilpony)。

下面是一份根据作者官方的使用说明整理的 V5 模型中文使用指南

### 🚨 核心警告与版本概述 (Overview)

- **训练状态**：基于包含饭制图和改进标签的更大数据集。由于时间原因提前发布，**模型处于既过拟合又欠拟合的状态**，比 v4 更难控制。
- **⚠️ 文本编码器警告**：作者表示可能把文本编码器（Text Encoder）给“炼炸了”（deep-fried），强烈建议你在使用时**降低此 LoRA 的 Text Encoder 权重**。
- **画风建议**：自带的 3D 画风可能很难剥离，建议配合其他**画风 LoRA** 或使用**画风强烈的底模**来覆盖它。
- **推荐负面提示词 (Negative Prompt)**：
  > `lowres, low quality, video artifacts, jpeg artifacts, chromatic aberration, film grain, absurdly detailed composition, sketch, red pupils, pink pupils`

---

### 👥 核心角色与触发词 (Characters)

**1. 卡提希娅 (Cartethyia) - 默认外观**

> `cartethyia, blue eyes, blonde hair, long hair, forehead tattoo, crown of thorns, teardrop earrings, dress, small breasts, tabard, bracelet, anklet, sandals`

**2. Fleurdelys - 默认外观**

> `fleurdelys, blue eyes, blonde hair, long hair, colored inner hair, aqua hair, single horn, floating earrings, spiked halo, dress, large breasts, armor, blue gloves, anklet`

**3. Fleurdelys (Leviathan 形态) - ⚠️ 训练不足**

> `fleurdelys (leviathan), dark persona, corruption, adapted costume, covered eyes, grey hair, long hair, colored inner hair, aqua hair, single horn, head fins, teardrop earrings, spiked halo, pale skin, black veins, dress, large breasts, chest jewel, armor, colored extremities, black hands, anklet`

- _作者注_：虽然剧情上是独立角色，但为了借用大模型的已有知识，将其标记为 Fleurdelys 的变体。她的口腔内部是蓝色的（可用 `blue mouth`），但舌头不是蓝色的。

---

### 👗 服饰与换装系统 (Costumes)

作者为卡提希娅训练了 6 套官方替换服装，但由于数据量太少，**基本上都训练不足（很难生效）**。

- `cartethyia (formal)`：正装/鸡尾酒裙
- `cartethyia (spring blossom)`：春日花朵装
- `cartethyia (seaside rendezvous)`：海滨相遇（夏日裙装）
- `cartethyia (summer serenade)`：夏日小夜曲（吊带裙、凉拖）
- `cartethyia (idol)`：偶像打扮（短马尾、短裤、靴子）
- `cartethyia (yogoods)`：另一套白裙

**💡 换装技巧 (非常实用)：**

- **微调默认服装**：使用 `adapted costume`（基于默认服装修改）。
- **穿完全不同的衣服**：使用 `alternate costume`（便服或饭制服装）。
- **脱掉特定饰品**：如果放在负面提示词里没用，可以尝试在正面提示词加入 `no crown` (不要王冠), `no necklace` (不要项链), `no terminal` (不要终端)。

---

### 🔍 局部重绘/细节提示词 (ADetailer Prompts)

当需要刻画局部特写或进行 Inpainting 时，建议使用以下组合：

- **脸部/眼睛**：`portrait, close-up` 或 `close-up, eye focus, two-tone eyes, blue eyes, pink eyes, grey pupils`
- **声痕/王冠**：`close-up, forehead, forehead tattoo, crown of thorns`
- **珠宝/项链**：`close-up, object focus, jewelry, fleur-de-lis`
- **衣服/武器**：`close-up, clothes focus, dress` 或 `close-up, weapon focus, [武器名称]`
- **手/脚**：`close-up, hand focus, bracelet` 或 `close-up, foot focus, feet only, barefoot, anklet` _(注：鞋子训练不足，建议随缘)_

---

### ⚔️ 武器、道具与场景 (Weapons, Items & Locations)

- **武器 (Weapons)**：包含 defier, bloodpact, haultir, tyrvine 等。**极度欠拟合，唯一勉强能画出来的是大剑 (`greatsword`)**。
- **道具 (Items)**：`pangu terminal` (盘古终端), `genesis terminal`, `fleur-de-lis` (鸢尾花挂饰), `mini crown`, `hand puppet` (手偶)。
- **场景 (Locations)**：包含 central hub, mindscape, ragunna city 等大量游戏内地名。作者表示这些词主要是用来“吸收背景杂讯”的，你可以写进提示词看看有没有奇效。
- **特殊状态 (Other tags)**：
  - `glowing tattoo`：发光的声痕（作者确认这个有效）。
  - `cartethyia (hologram)`：全息投影状态。
  - `thinking pose`：沉思姿势（右手托腮，左手交叉）。
  - `corrupted gunshot wound, no necklace`：被击中时的特殊伤口。

---

### 🎨 画风与质量控制词 (Style & Quality Tags)

既然底模是 NoobAI-XL，可以利用其特有的质量词进行控制：

- **画风控制**：
  - `3d`：游戏 3D 截图风（不需要的话放进负面）。
  - `game cg`：游戏内 2D 立绘风。
  - `anime coloring`：TV 动画上色风（容易导致色彩饱和度过高）。
- **质量词 (推荐放在正面最前)**：
  - `awa` 或 `very awa`：NoobAI-XL 专用的**最高质量**神仙级饭制图标签（作者强烈推荐）。
- **负面控制词 (推荐放在负面)**：
  - `absurdly detailed composition`：可以吸收并消除画师为了炫技而添加的“无意义的过度细节杂乱感”。
  - `video artifacts`：消除视频截图带来的压缩画质和瞎眼光晕。
  - `chromatic aberration` (色差) / `film grain` (胶片颗粒)：消除画面噪点。

---

针对这个 v5 模型，你在连线时，请务必把 `LoraLoader` 节点拆分为 `strength_model` (主模型权重) 和 `strength_clip` (文本编码器权重)。**把 `strength_clip` 降低到 `0.5` 左右，主模型保持在 `0.8`**，然后加上作者推荐的最高质量词 `very awa`，这样能最大程度避开这个版本的缺陷。
