# 字符串和 16 进制互转

```java
/**
 * 字符串转换成为16进制
 */
public static String strToHexStr(String str) {
    char[] chars = "0123456789ABCDEF".toCharArray();
    StringBuilder sb = new StringBuilder();
    byte[] bs = str.getBytes();
    int bit;
    for (byte b : bs) {
        bit = (b & 0x0f0) >> 4;
        sb.append(chars[bit]);
        bit = b & 0x0f;
        sb.append(chars[bit]);
    }
    return sb.toString().trim();
}

/**
 * 16进制直接转换成为字符串
 */
public static String hexStrToStr(String hexStr) {
    String str = "0123456789ABCDEF";
    char[] hexs = hexStr.toCharArray();
    byte[] bytes = new byte[hexStr.length() / 2];
    int n;
    for (int i = 0; i < bytes.length; i++) {
        // 高4位
        n = str.indexOf(hexs[2 * i]) * 16;
        // 低4位
        n += str.indexOf(hexs[2 * i + 1]);
        // int转byte
        bytes[i] = (byte) (n & 0xff);
    }
    return new String(bytes);
}

public static void main(String[] args) {
    String msg = "测试字符串";

    System.out.println("字符串转16进制: " + strToHexStr(msg));
    System.out.println("16进制转字符串: " + hexStrToStr(strToHexStr(msg)));
}
```