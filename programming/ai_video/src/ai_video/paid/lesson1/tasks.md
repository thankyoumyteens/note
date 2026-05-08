# 操作步骤

## 第一步：建立总文件夹

建立文件夹：

```text
Cartethyia_Reference_Pack
```

---

## 第二步：建立 6 个子文件夹

在里面建立这 6 个子文件夹：

```text
01_Official_Artwork
02_In_Game_Screenshots
03_PV_Screenshots
04_Face_and_Expression
05_Outfit_Details
06_Weapon_and_Accessories
```

每个文件夹的用途如下。

---

### 01_Official_Artwork

放：

```text
官方立绘
官方宣传图
官方角色展示图
官方半身图
官方全身图
```

用途：

```text
确定卡提希娅的标准形象。
```

这类图优先级最高。

---

### 02_In_Game_Screenshots

放：

```text
游戏内模型截图
战斗待机截图
角色界面截图
不同角度截图
```

用途：

```text
确定她在游戏内真实模型中的样子。
```

很多时候官方立绘和游戏内模型会有差异，视频生成时两者都要参考。

---

### 03_PV_Screenshots

放：

```text
角色 PV 截图
剧情动画截图
官方演示视频截图
高光镜头截图
```

用途：

```text
确定镜头氛围、光影、电影感、角色动态姿态。
```

这类图对后面做视频特别重要。

---

### 04_Face_and_Expression

放：

```text
正脸特写
侧脸特写
眼部特写
表情截图
低头、回头、凝视等表情
```

用途：

```text
防止生成时脸漂。
```

如果你以后要做眼部特写、半身镜头，这个文件夹很关键。

---

### 05_Outfit_Details

放：

```text
上半身服装
裙摆
披风 / 飘带
手套
鞋
肩部
胸前装饰
衣服纹样
```

用途：

```text
防止模型把服装简化成普通白裙或普通战斗服。
```

---

### 06_Weapon_and_Accessories

放：

```text
武器
头饰
耳饰
发饰
腰部配件
特殊装饰
能量特效
```

用途：

```text
防止武器、头饰、配饰丢失或变形。
```

---

## 第三步：收集 20–30 张参考图

第一轮不要太纠结，先收集够。

建议数量：

```text
官方图：3–5 张
游戏内截图：5–10 张
PV 截图：5–10 张
脸部 / 表情：3–5 张
服装细节：2–3 张
武器 / 配饰：2–3 张
```

如果某一类暂时找不到，也没关系，先用能找到的图补上。

---

## 第四步：给图片命名

不要用默认文件名。

推荐命名方式：

```text
cartethyia_official_front_01.png
cartethyia_official_fullbody_01.png
cartethyia_ingame_face_01.png
cartethyia_pv_back_01.png
cartethyia_eye_closeup_01.png
cartethyia_outfit_detail_01.png
cartethyia_weapon_01.png
```

命名不用完美，但要看得出用途。

---

## 第五步：精选 8 张核心参考图

从 20–30 张里挑出这 8 张：

```text
01_core_front_or_halfbody
02_core_fullbody
03_core_side_or_3quarter_face
04_core_back_or_pose
05_core_eye_or_expression
06_core_weapon_or_prop
07_core_pv_highlight
08_core_outfit_or_accessory_detail
```

你可以单独建一个文件夹：

```text
00_Core_References
```

把这 8 张复制进去。

---

## 第六步：上传给 AI

上传时最好按顺序发，或者压缩成一个包。

你也可以直接这样说明：

```text
1：官方正面 / 半身
2：官方全身
3：侧脸或 3/4 脸
4：背影或大姿态
5：眼部 / 表情特写
6：武器 / 道具
7：PV / 动画高光镜头
8：服装 / 配饰细节
```

AI 收到后，需要输出 “基于参考图生成角色控制清单 v1”：

```text
Cartethyia Character Control Pack v1
```

里面要包括：

```text
角色视觉特征清单
正向提示词
负面提示词
容易跑偏点
适合镜头类型
```
