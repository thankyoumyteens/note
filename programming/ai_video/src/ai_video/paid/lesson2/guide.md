# 生成正面半身标准图

## 步骤 1：安装 Blender

操作：

```text
1. 打开 Blender 官网下载页
2. 下载当前系统对应版本
3. 安装并打开 Blender
```

官网：

```text
blender.org/download
```

建议：

```text
优先安装稳定版，不要装 alpha / beta 测试版。
```

---

## 步骤 2：安装 mmd_tools

有两种方式。

## 方式 A：通过 Blender Extensions 安装

如果你的 Blender 版本支持 Extensions：

```text
1. 打开 Blender
2. Edit → Preferences
3. 找到 Get Extensions 或 Extensions
4. 搜索 MMD Tools
5. 安装并启用
```

这是最简单的方式。

---

## 方式 B：从 GitHub 安装

如果 Extensions 里找不到，走 GitHub。

操作：

```text
1. 打开 GitHub 上的 blender_mmd_tools 项目
2. 下载压缩包
3. 解压
4. 找到 mmd_tools 文件夹
5. 把 mmd_tools 文件夹放到 Blender 的 addons 文件夹
6. 重启 Blender
7. Edit → Preferences → Add-ons
8. 搜索 mmd_tools
9. 勾选启用
```

mmd_tools 的安装说明里也提到：需要把 `mmd_tools` 文件夹复制到 Blender 的 `scripts/addons` 文件夹，并重启 Blender 后启用插件。([GitHub][4])

Mac 上常见 addons 路径类似：

```text
~/Library/Application Support/Blender/<版本号>/scripts/addons/
```

Windows 上常见路径类似：

```text
C:\Users\<你的用户名>\AppData\Roaming\Blender Foundation\Blender\<版本号>\scripts\addons\
```

---

## 步骤 3：确认模型包结构

下载地址: [【鸣潮】卡提希娅（全形态）](https://www.aplaybox.com/details/model/6qC03myCISp0)

打开你下载的模型文件夹，检查是否有这些内容：

```text
.pmx 文件
贴图文件夹
toon / spa / sph 文件
Readme.txt
```

不要移动里面的贴图文件。
PMX 文件和贴图文件的相对路径最好保持原样，否则导入 Blender 后可能材质丢失。

---

## 步骤 4：导入 PMX 模型

打开 Blender 后：

```text
File → Import → MikuMikuDance Model (.pmx)
```

如果你没有看到这个选项，说明 mmd_tools 没启用成功。

导入时注意：

```text
选择 .pmx 文件
不要只选贴图
导入后等待一会儿
如果模型很小或很大，先不要慌，后面可以调相机
```

mmd_tools 文档中也说明，导入模型可以在 mmd_tools 面板里点击 Import Model，然后选择 `.pmx` 或 `.pmd` 文件。([GitHub][5])

---

## 步骤 5：检查模型是否正常

导入后先检查 8 件事：

```text
1. 模型是否完整显示
2. 脸部是否正常
3. 头发贴图是否正常
4. 蓝色飘带是否透明
5. 水晶头冠是否显示
6. 耳饰是否显示
7. 黑色内层裙摆是否存在
8. 模型有没有全身变白 / 材质丢失
```

如果出现全白或材质缺失，通常是：

```text
贴图路径丢失
贴图文件夹位置变了
Blender 没找到原始贴图
```

先不要渲染，先截图发我，我帮你判断。

---

## 步骤 6：设置基础视图

为了先看清模型，不急着调复杂灯光。

在 Blender 右上角切换视图模式：

```text
Material Preview
```

这样能较快看到贴图和材质。

如果模型太暗，可以切到：

```text
Rendered View
```

但初期检查用 Material Preview 就够。

---

## 步骤 7：设置第一张标准图：正面半身

先不要渲染 6 张。先做 **正面半身**。

### 7.1 选择相机

如果场景里没有相机：

```text
Shift + A → Camera
```

设置相机位置大致：

```text
相机在角色正前方
高度对准胸口到脸部之间
视野覆盖头冠到腰部
```

如果你不熟 Blender，先用简单方法：

```text
1. 在视窗里调整到想要的正面半身角度
2. 按 Ctrl + Alt + Numpad 0
```

这会把当前视角设为相机视角。

Mac 没有小键盘的话，可以在菜单里找：

```text
View → Align View → Align Active Camera to View
```

---

### 7.2 设置渲染分辨率

看右侧属性栏那一列竖排小图标，找到这个图标：

```text
打印机 / 输出图标
```

它叫：

```text
Output Properties
```

点进去后，最上面会看到：

```text
Format
```

里面就是渲染分辨率：

```text
Resolution X
Resolution Y
%
```

把它改成：

```text
Resolution X: 1536
Resolution Y: 2048
Percentage: 100%
```

也就是竖版 3:4，适合角色半身标准图。

### 7.3 调整构图

#### 1. 打开右侧侧栏

按：

```text
N
```

左边 3D 视图右侧会弹出一个小面板。

#### 2. 找到 View 面板

在弹出的侧栏里点：

```text
View
```

#### 3. 勾选 Lock Camera to View

找到：

```text
Lock Camera to View
```

勾上。

这个功能的意思是：

> 你现在拖动视图时，相机不会跟着一起动。

#### 4. 在相机视图里调整构图

保持现在的相机视图，使用普通视图操作：

```text
鼠标滚轮：缩放
Shift + 中键拖拽：平移画面
中键拖拽：旋转视角
```

但你现在做正面标准图，**尽量不要旋转**，只需要：

```text
Shift + 中键向下拖：让角色头部往画面中间下来
鼠标滚轮稍微缩小：让头冠完整进入画面
```

目标是让画面变成：

```text
头冠完整可见
脸在画面上半部分
胸口和黑色高领清楚
下方到腰部附近即可
```

---

### 7.4 改成正交相机

选中右上角 Outliner 里的 Camera，保证 Camera 是高亮的。

然后在右侧竖排那一列小图标(不是右上角视窗里的相机按钮，而是**右侧 Properties 面板里的绿色相机图标**)里找到绿色小摄像机图标名字叫：

```text
Camera Data Properties
```

点绿色相机图标后，你会看到类似：

```text
Lens
Camera
Depth of Field
Viewport Display
```

在 **Lens** 或 **Camera** 区域里，会有一个选项：

```text
Type
```

默认应该是：

```text
Perspective
```

把它改成：

```text
Orthographic
```

改成 Orthographic 后，会出现：

```text
Orthographic Scale
```

正面半身建议先填：

```text
2.4
```

如果角色太小，调小：

```text
2.0
```

如果角色太大，调大：

```text
2.8
```

改成 Orthographic 后，先试：

```text
Orthographic Scale: 1.0
```

然后保持你已经勾选的：

```text
Camera to View
```

在相机视图里用：

```text
Shift + 鼠标中键拖动：平移画面
鼠标滚轮：缩放视图 / 调整构图
```

目标构图：

```text
头冠完整在画面内
脸部位于画面上半部分
下边到腰部或大腿上缘
不需要完整显示蓝色飘带
```

---

## 步骤 8：设置基础灯光

```text
Shift + A → Light → Area
```

### 先确认选中 Area

右上角 Outliner 里点击：

```text
Area
```

### 用右侧 Transform 输入位置

点右侧竖排图标里的 **橙色方块图标**，进入 Object Properties。

然后找到：

```text
Transform
```

把 Area Light 的位置改成类似这样：

```text
Location X: 0
Location Y: -2.5
Location Z: 2.5
```

这个位置的意思是：

```text
X = 中间
Y = 角色前方
Z = 角色上方
```

如果光照太暗，之后再加 Power。
调整 Area Light 亮度

选中 Area 后，点击右侧竖排里的 **绿色灯泡图标**，也就是 Light Properties。

设置：

```text
Power: 500 W
Size: 5 m
```

如果渲染出来太暗，改成：

```text
Power: 800 W
```

如果阴影太硬，把 Size 调大：

```text
Size: 6–8 m
```

---

## 步骤 9：设置背景

右侧属性栏找到这个图标：

```text
红色地球 / World Properties
```

点进去后找到：

```text
Color
```

把颜色改成深灰，比如：

```text
#2E2E2E
```

或者浅灰：

```text
#808080
```

建议第一张正面半身用 **深灰背景**，因为卡提希娅头发、白色服装和蓝色飘带都比较亮，深灰更容易看清轮廓。

---

## 步骤 10：渲染第一张图

### 10.1 设置渲染引擎

在右侧属性栏中，点击：

```text
Render Properties
```

图标一般是：

```text
一个相机背后带小圆点 / 渲染图标
```

它通常在右侧竖排图标的上方区域，不是绿色相机图标，也不是打印机图标。

进入后，找到：

```text
Render Engine
```

把它设置为：

```text
Eevee
```

或者在 Blender 5.1 中显示为：

```text
Eevee Next
```

原因：

```text
Eevee 渲染快，适合第 2 课测试标准图。
Cycles 质量更高，但慢，当前阶段没必要。
Workbench 只是视图渲染，不适合最终标准图。
```

---

### 10.2 开启透明材质显示检查

卡提希娅有蓝色透明飘带，所以要确认材质显示正常。

在右上角视图模式里，你可以先切到：

```text
Material Preview
```

或者：

```text
Rendered View
```

检查：

```text
1. 头发不是全黑 / 全白
2. 服装贴图正常
3. 蓝色飘带能显示
4. 头冠能显示
5. 眼睛贴图正常
```

如果 Material Preview 里已经正常，通常可以先继续渲染。

---

### 10.3 设置输出分辨率

右侧属性栏点击：

```text
Output Properties
```

图标像：

```text
打印机
```

展开：

```text
Format
```

设置：

```text
Resolution X: 1536
Y: 2048
Percentage: 100%
```

确认文件格式：

```text
File Format: PNG
Color: RGBA
Color Depth: 8
```

如果你只想普通不透明背景，也可以用：

```text
Color: RGB
```

但建议保持：

```text
RGBA
```

以后做合成更方便。

---

### 10.4 设置保存位置

在同一个 **Output Properties** 面板里，找到：

```text
Output
```

你现在可能看到：

```text
/tmp/
```

这只是默认临时目录。

建议点右侧的小文件夹图标，把输出路径改到你的课程素材目录，比如：

```text
Cartethyia_Project/02_Model_Renders/
```

---

### 10.5 隐藏骨骼线的视图干扰

你现在视图里有很多黑色骨骼线。正常情况下它们不会出现在最终渲染里，但为了保险，可以先检查一下。

在右上角 Outliner 里，找到模型相关的骨骼对象，通常可能叫：

```text
Armature
卡提希娅
骨骼
```

如果你不确定，不要乱删。

先做一个测试渲染即可。
如果最终 PNG 里没有骨骼线，就不用处理。
如果最终 PNG 里出现骨骼线，再处理它们的渲染可见性。

处理方式：

```text
在 Outliner 里找到骨骼 / Armature 对象
关闭它右侧的相机图标
```

注意：
不是关闭眼睛图标，眼睛只是视图可见；**相机图标才是渲染可见**。

---

### 10.6 开始渲染

顶部菜单点击：

```text
Render → Render Image
```

快捷键通常是：

```text
F12
```

Mac 上如果 F12 被系统占用，就用菜单更稳：

```text
Render → Render Image
```

点击后会弹出一个渲染窗口，等待它渲染完成。

---

### 10.7 保存渲染结果

渲染窗口完成后，在渲染窗口顶部菜单点击：

```text
Image → Save As
```

文件名填：

```text
cartethyia_model_front_halfbody.png
```

保存路径建议：

```text
Cartethyia_Project/02_Model_Renders/cartethyia_model_front_halfbody.png
```

## 问题记录：Blender 导入 MMD 模型后，Face\_ 材质开启 Double Sided 会导致额头印记附近出现黑色脏块。

解决方法：关闭 Face\_ 材质的 Double Sided。脸部材质通常不需要双面显示；飘带、薄纱、头发片等薄片材质再视情况保留 Double Sided。

操作步骤:

1. 先选中模型的身体 / 脸部材质对象。
2. 右侧属性栏点击：Material Properties 红色球形图标
3. 往下滑找到 MMD Material
4. 取消勾选：Double Sided
