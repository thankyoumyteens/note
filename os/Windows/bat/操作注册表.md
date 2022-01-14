# REG QUERY 查询注册表值
```bat
REG QUERY KeyName [/v [ValueName] | /ve] [/s]
          [/f Data [/k] [/d] [/c] [/e]] [/t Type] [/z] [/se Separator]
          [/reg:32 | /reg:64]
```
## KeyName
```bat
[\\Machine\]FullKey
```

- `Machine` - 远程机器名称，省略当前机器的默认值。在远程机器上, 只有 HKLM 和 HKU 可用。
- `FullKey` - 以 `ROOTKEY\SubKey` 名称形式
- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
- `/v` 具体的注册表项值的查询。如果省略，会查询该项的所有值。只有与 /f 开关一起指定的情况下，此开关的参数才是可选的。它指定只在值名称中搜索。
- `/ve` 查询默认值或空值名称(默认)。
- `/s` 循环查询所有子项和值(如 dir /s)。
- `/se` 为 `REG_MULTI_SZ` 在数据字符串中指定分隔符(长度只为 1 个字符)。默认分隔符为 "\0"。
- `/f` 指定搜索的数据或模式。如果字符串包含空格，请使用双引号。默认为 "*"。
- `/k` 指定只在项名称中搜索。
- `/d` 指定只在数据中搜索。
- `/c` 指定搜索时区分大小写。默认搜索为不区分大小写。
- `/e` 指定只返回完全匹配。默认是返回所有匹配。
- `/t` 指定注册表值数据类型。有效的类型是: REG_SZ, REG_MULTI_SZ, REG_EXPAND_SZ, REG_DWORD, REG_QWORD, REG_BINARY, REG_NONE 默认为所有类型。
- `/z` 详细: 显示值名称类型的数字等值。
- `/reg:32` 指定应该使用 32 位注册表视图访问的注册表项。
- `/reg:64` 指定应该使用 64 位注册表视图访问的注册表项。

## 示例
查询系统环境变量Path
```bat
REG QUERY "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v "Path"
```
查询用户环境变量Path
```bat
REG QUERY "HKCU\Environment" /v "Path"
```

# REG ADD 添加/修改注册表键值

```
REG ADD KeyName [/v ValueName | /ve] [/t Type] [/s Separator] [/d Data] [/f]
        [/reg:32 | /reg:64]
```

## KeyName
```bat
[\\Machine\]FullKey
```

- `Machine` - 远程机器名称，省略当前机器的默认值。在远程机器上, 只有 HKLM 和 HKU 可用。
- `FullKey` - 以 `ROOTKEY\SubKey` 名称形式
- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
- `/v` 所选项之下要添加的值名称。
- `/ve` 为注册表项添加空白值名称(默认)。
- `/t` RegKey 数据类型, REG_SZ, REG_MULTI_SZ, REG_EXPAND_SZ, REG_DWORD, REG_QWORD, REG_BINARY, REG_NONE, 如果忽略，则采用 REG_SZ。
- `/s` 指定一个在 REG_MULTI_SZ 数据字符串中用作分隔符的字符, 如果忽略，则将 "\0" 用作分隔符。
- `/d` 要分配给添加的注册表 ValueName 的数据。
- `/f` 不用提示就强行覆盖现有注册表项。
- `/reg:32` 指定应该使用 32 位注册表视图访问的注册表项。
- `/reg:64` 指定应该使用 64 位注册表视图访问的注册表项。

## 示例

设置用户环境变量Path
```bat
REG ADD "HKCU\Environment" /v "Path" /t REG_EXPAND_SZ /d "%PATH%;D:\AppFolder" /f
```

# REG DELETE 删除注册表键值

```bat
REG DELETE KeyName [/v ValueName | /ve | /va] [/f] [/reg:32 | /reg:64]
```

## KeyName
```bat
[\\Machine\]FullKey
```

- `Machine` - 远程机器名称，省略当前机器的默认值。在远程机器上, 只有 HKLM 和 HKU 可用。
- `FullKey` - 以 `ROOTKEY\SubKey` 名称形式
- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数

- `/v ValueName` 所选项下面的要删除的值名称。如果省略，则删除该项下面的所有子项和值。
- `/ve` 删除空值名称的值(默认)。
- `/va` 删除该项下面的所有值。
- `/f` 不用提示，强制删除。
- `/reg:32` 指定应该使用 32 位注册表视图访问的注册表项。
- `/reg:64` 指定应该使用 64 位注册表视图访问的注册表项。

## 示例

删除主机 ZODIAC 上的 MyCo 下面的注册表值 MTU
```bat
REG DELETE "\\ZODIAC\HKLM\Software\MyCo" /v "MTU"
```
