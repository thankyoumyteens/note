# 补码

真值是机器数所代表的实际的值, 机器数是真值在计算机中的表示。例如:

| 真值 | 真值 | 机器数 |
| ---- | ---- | ------ |
| +5   | +101 | 0101   |
| -5   | -101 | 1101   |

机器数的有符号数, 有原码、补码、反码、移码四种形式。

## 定点数

定点小数:

```
[符号][小数点][数值部分]
```

定点整数:

```
[符号][数值部分][小数点]
```

## 原码

整数:

- 正数的真值: X = +x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>
- 正数的原码: \[X\]<sub>原</sub> = 0x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>
- 负数的真值: X = -x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>
- 负数的原码: \[X\]<sub>原</sub> = 1x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>

小数:

- 正数的真值: X = +0.x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>
- 正数的原码: \[X\]<sub>原</sub> = 0.x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>
- 负数的真值: X = -0.x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>
- 负数的原码: \[X\]<sub>原</sub> = 1.x<sub>1</sub>x<sub>2</sub>x<sub>3</sub>...x<sub>n</sub>
