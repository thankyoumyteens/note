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
