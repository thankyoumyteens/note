# 创建坐标轴

函数定义:

```py
add_axes(rect, projection=None, polar=False, **kwargs)
```

- `rect` 一个元组 `(left, bottom, width, height)`，定义了新坐标轴在画布左下角的坐标(left, bottom)和宽高(取值范围 0 到 1, 是画布大小的百分比)
- `projection` 坐标轴的投影类型，常见的有 rectilinear（直角坐标）、polar（极坐标）
- `polar` 如果为 True，则创建一个极坐标轴
