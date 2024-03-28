# 临时修改

```bat
chcp 65001
```

- gbk编码: chcp 936
- utf8编码: chcp 65001

# 永久修改

注册表 -> HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor -> 右键-新建 -> 字符串值 -> 名称"列填写"autorun", 数值数据填写"chcp 65001" 
