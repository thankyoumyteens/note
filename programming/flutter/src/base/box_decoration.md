# BoxDecoration

```dart
const BoxDecoration({
  this.color,
  this.image,
  this.border,
  this.borderRadius,
  this.boxShadow,
  this.gradient,
  this.backgroundBlendMode,
  this.shape = BoxShape.rectangle,
})
```

- color: 背景色
- image: 背景图片
- border: 边框
- borderRadius: 边框圆角
- boxShadow: 阴影
- gradient: 渐变背景色

## 设置背景色

```dart
decoration: const BoxDecoration(
  color: Colors.blue,
),
```

## 设置背景图片

修改 pubspec.yaml:

```yaml
flutter:
  # 背景图
  assets:
    - images/a.png
```

设置背景图:

```dart
decoration: const BoxDecoration(
  image: DecorationImage(
    // 图片
    image: ExactAssetImage("images/a.png"),
    // 图片填充方式
    fit: BoxFit.fill,
    // 图片位置
    alignment: Alignment.center,
    // 图片平铺方式
    repeat: ImageRepeat.noRepeat,
  ),
),
```

## 设置边框和圆角

```dart
decoration: BoxDecoration(
  // 边框
  border: Border.all(
    // 边框颜色
    color: Colors.blue,
    // 边框宽度
    width: 10,
    // 线条类型
    style: BorderStyle.solid,
  ),
  // 圆角
  borderRadius: const BorderRadius.all(Radius.circular(10)),
),
```

## 设置阴影

```dart
decoration: BoxDecoration(
  // 列表, 多个阴影会叠加
  boxShadow: const [
    BoxShadow(
      // 阴影颜色
      color: Colors.green,
      // 阴影位置
      offset: Offset(20, 20),
      // 模糊半径
      blurRadius: 10,
      // 延伸半径
      spreadRadius: 10,
    ),
  ],
),
```
