# BigDecimal

## 四舍五入

```java
BigDecimal b = new BigDecimal("111231.5585");
// 保留2位小数
double result = b.setScale(2, BigDecimal.ROUND_HALF_UP).doubleValue();
// 111231.56
System.out.println(result);
```

## 去除小数点后多余的 0

```java
BigDecimal val1 = new BigDecimal("12.00");
BigDecimal val2 = new BigDecimal("1200.00");
// 保留4位小数, 四舍五入
BigDecimal result2 = val2.divide(val1, 4, BigDecimal.ROUND_HALF_UP);
// 100.0000
System.out.println(result2);
// 1E+2
System.out.println(result2.stripTrailingZeros());
// 100
System.out.println(result2.stripTrailingZeros().toPlainString());
```

## 求平方根

```java
/**
 * 计算平方根(Java 9开始自带sqrt方法)
 *
 * @param value 待计算的值
 * @param scale 保留小数位数
 * @return 平方根
 */
public static BigDecimal sqrt(BigDecimal value, int scale) {
    BigDecimal ZERO = new BigDecimal("0");
    if (ZERO.equals(value.stripTrailingZeros())) {
        return ZERO;
    }
    BigDecimal num2 = BigDecimal.valueOf(2);
    int precision = 100;
    MathContext mc = new MathContext(precision, RoundingMode.HALF_UP);
    BigDecimal deviation = value;
    int cnt = 0;
    while (cnt < precision) {
        deviation = (deviation.add(value.divide(deviation, mc))).divide(num2, mc);
        cnt++;
    }
    deviation = deviation.setScale(scale, RoundingMode.HALF_UP);
    return deviation;
}
```
