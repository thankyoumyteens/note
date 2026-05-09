# 六张标准图的 niji prompt

下面的 prompt 都是 niji 适配版。

你使用时，把参考图链接放在最前面。

---

## 图 1：正面半身标准图

用途：

```text
定脸、定气质、定头冠、定耳饰、定上半身服装。
```

推荐参考图：

```text
正面图 + 官方全身图
```

prompt：

```text
[正面参考图链接] [官方全身参考图链接] Cartethyia from Wuthering Waves, faithful character reference, anime game 3D model inspired key visual, young woman with long pale blonde hair, center-parted bangs, soft side hair strands, calm reserved expression, slightly narrow face, delicate blue crystalline eyes, elf-like pointed ears, black vertical forehead mark, thin irregular blue-purple crystalline branch crown close to the forehead, not large antlers, blue teardrop earrings, white black and blue ornate ceremonial outfit, black high collar, white front panels with black inner bodice, blue thin straps, gold ring ornaments, translucent blue gradient fin-like ribbons, elegant sacred and mysterious atmosphere, front view, upper body portrait, centered composition, clean simple dark background, high quality anime game character reference sheet, detailed outfit design --niji 7 --ar 2:3 --s 50 --iw 2 --no text, logo, watermark, school uniform, casual outfit, boots, staff, gun, bow, scythe, antlers, golden crown
```

验收标准：

```text
1. 正脸稳定
2. 蓝眼清楚
3. 额头黑色竖纹存在
4. 水晶枝冠存在
5. 尖耳和蓝色耳饰存在
6. 黑色高领存在
7. 不像随机浅金发二次元少女
```

---

## 图 2：全身标准图

用途：

```text
定完整服装、身体比例、蓝色飘带、鞋子、整体轮廓。
```

推荐参考图：

```text
官方全身图 + 游戏内模型图
```

prompt：

```text
[官方全身参考图链接] [游戏内模型参考图链接] Cartethyia from Wuthering Waves, elegant anime game character, young woman with long pale blonde hair, blue crystalline eyes, elf-like pointed ears, black vertical forehead mark, blue crystalline branch crown, blue teardrop earrings, white black and blue ornate outfit, black high collar, translucent blue gradient ribbon sleeves, flowing blue gradient ribbons, gold ornaments, white strappy high-heel sandals, delicate ceremonial fantasy outfit, calm gentle expression, sacred and mysterious atmosphere, full body standing pose, front view, clean simple background, clear silhouette, high quality anime game character reference sheet, detailed outfit design --niji 7 --ar 2:3 --s 100 --iw 1.5 --no text, logo, watermark, school uniform, casual outfit, boots, staff, gun, bow, scythe
```

验收标准：

```text
1. 全身完整
2. 头冠和耳饰没有丢
3. 白黑蓝服装结构正确
4. 蓝色渐变飘带明显
5. 鞋子是细带高跟凉鞋，不是靴子
6. 不是普通白裙
```

如果生成成靴子，下一轮把 `--no boots` 放前一点，或者在正向 prompt 里强化：

```text
white strappy high-heel sandals, visible delicate ankle straps
```

---

## 图 3：侧脸近景标准图

用途：

```text
定侧脸轮廓、尖耳、耳饰、头冠侧面结构。
```

推荐参考图：

```text
侧脸图 + 正面脸图
```

prompt：

```text
[侧脸参考图链接] [正面脸部参考图链接] Cartethyia from Wuthering Waves, elegant anime game character, young woman with long pale blonde hair, blue crystalline eyes, elf-like pointed ears, black vertical forehead mark, blue crystalline branch crown, blue teardrop earrings, white black and blue ornate outfit, black high collar, gold ornaments, calm and distant expression, sacred and mysterious atmosphere, side profile close-up, 90 degree profile view, clean simple background, soft blue lighting, detailed face, detailed pointed ear, detailed blue teardrop earrings, high quality anime game character reference sheet --niji 7 --ar 2:3 --s 100 --iw 1.5 --no text, logo, watermark, school uniform, casual outfit, boots, staff, gun, bow, scythe
```

验收标准：

```text
1. 侧脸清楚
2. 尖耳明显
3. 蓝色水滴耳饰明显
4. 头冠不是普通王冠
5. 脸不要变成熟
6. 气质冷静
```

---

## 图 4：背影标准图

用途：

```text
定背面长发、编发、背部轮廓、飘带位置。
```

推荐参考图：

```text
背面图 + 官方全身图
```

prompt：

```text
[背面参考图链接] [官方全身参考图链接] Cartethyia from Wuthering Waves, elegant anime game character, young woman with very long pale blonde hair, braided back hair, blue crystalline branch crown, elf-like pointed ears, white black and blue ornate outfit, translucent blue gradient ribbon sleeves, flowing blue ribbons, gold ornaments, delicate ceremonial fantasy outfit, sacred and mysterious atmosphere, back view, full body from behind, standing calmly, clean simple background, clear silhouette, detailed long hair, detailed braided hair, high quality anime game character reference sheet --niji 7 --ar 2:3 --s 100 --iw 1.5 --no text, logo, watermark, school uniform, casual outfit, boots, staff, gun, bow, scythe
```

验收标准：

```text
1. 长发从背后垂下
2. 有背后编发结构
3. 蓝色飘带位置清楚
4. 头冠可见
5. 服装背面完整
6. 不要变成披风角色
```

如果背影图总是丢头冠，下一轮加：

```text
blue crystalline branch crown visible from behind
```

---

## 图 5：眼部 / 表情特写

用途：

```text
定眼睛、额头印记、表情、头冠局部。
```

推荐参考图：

```text
脸部特写 + 正面图
```

prompt：

```text
[脸部特写参考图链接] [正面参考图链接] Cartethyia from Wuthering Waves, elegant anime game character, close-up of her face and eyes, blue crystalline eyes, black vertical forehead mark, pale blonde hair framing her face, blue crystalline branch crown partially visible, elf-like pointed ears slightly visible, blue teardrop earrings, calm gentle expression, sacred and mysterious atmosphere, soft lighting, detailed eyes, emotional subtle smile, high quality anime game cinematic close-up --niji 7 --ar 2:3 --s 100 --iw 1.5 --no text, logo, watermark, school uniform, casual outfit, staff, gun, bow, scythe
```

验收标准：

```text
1. 蓝色晶体眼清楚
2. 额头黑色竖纹清楚
3. 表情温柔克制
4. 头冠局部存在
5. 不要变成普通大眼萌妹
```

眼部特写可以稍微放宽服装要求，因为主要验证脸。

---

## 图 6：持剑中景标准图

用途：

```text
定武器、上半身战斗状态、能量意象。
```

推荐参考图：

```text
官方角色展示图 + 官方全身图
```

prompt：

```text
[官方角色展示参考图链接] [官方全身参考图链接] Cartethyia from Wuthering Waves, elegant anime game character, young woman with long pale blonde hair, blue crystalline eyes, elf-like pointed ears, black vertical forehead mark, blue crystalline branch crown, blue teardrop earrings, white black and blue ornate outfit, black high collar, translucent blue gradient ribbon sleeves, gold ornaments, calm determined expression, holding a glowing blue sword, elegant sword, blue energy blade, water-like energy around the blade, crystalline blue light, sacred and mysterious atmosphere, medium shot, clean simple background, high quality anime game character reference sheet, detailed character design --niji 7 --ar 2:3 --s 100 --iw 1.5 --no text, logo, watermark, school uniform, casual outfit, boots, staff, gun, bow, scythe, red fire
```

验收标准：

```text
1. 武器是剑
2. 剑是蓝色能量感
3. 不是法杖、枪、弓、镰刀
4. 脸仍然像卡提希娅
5. 服装和头冠没有因为持剑而跑偏
```

如果总是生成法杖，下一轮加强正向：

```text
holding an elegant sword, visible blade, sword hilt, blue energy blade
```

同时保留：

```text
--no staff
```
