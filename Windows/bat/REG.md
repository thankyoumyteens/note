# REG /?
```bat
REG Operation [Parameter List]
```
Operation:
- QUERY
- ADD
- DELETE
- COPY
- SAVE
- LOAD
- UNLOAD
- RESTORE
- COMPARE
- EXPORT
- IMPORT
- FLAGS

返回代码: (除了 REG COMPARE)

- 0 成功
- 1 失败

要得到有关某个操作的帮助，请键入:
```bat
REG Operation /?
```
例如:
```bat
REG QUERY /?
```

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

# REG ADD 添加/修改注册表值

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

例如:

设置用户环境变量Path
```bat
REG ADD "HKCU\Environment" /v "Path" /t REG_EXPAND_SZ /d "%PATH%;D:\AppFolder" /f
```

# REG DELETE /?

REG DELETE KeyName [/v ValueName | /ve | /va] [/f] [/reg:32 | /reg:64]

## KeyName
```bat
[\\Machine\]FullKey
```

- `Machine` - 远程机器名称，省略当前机器的默认值。在远程机器上, 只有 HKLM 和 HKU 可用。
- `FullKey` - 以 `ROOTKEY\SubKey` 名称形式
- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
  ValueName  所选项下面的要删除的值名称。
             如果省略，则删除该项下面的所有子项和值。

  /ve        删除空值名称的值(默认)。

  /va        删除该项下面的所有值。

  /f         不用提示，强制删除。

  /reg:32    指定应使用 32 位注册表视图访问
             注册表项。

  /reg:64    指定应使用 64 位注册表视图访问
             注册表项。

示例:

  REG DELETE HKLM\Software\MyCo\MyApp\Timeout
    删除注册表项 Timeout 及其所有子项和值

  REG DELETE \\ZODIAC\HKLM\Software\MyCo /v MTU
    删除 ZODIAC 上的 MyCo 下面的注册表值 MTU

# REG COPY /?

REG COPY KeyName1 KeyName2 [/s] [/f] [/reg:32 | /reg:64]

## KeyName
```bat
[\\Machine\]FullKey
```

- `Machine` - 远程机器名称，省略当前机器的默认值。在远程机器上, 只有 HKLM 和 HKU 可用。
- `FullKey` - 以 `ROOTKEY\SubKey` 名称形式
- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
  /s         复制所有子项和值。

  /f         不用提示，强制复制。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG COPY HKLM\Software\MyCo\MyApp HKLM\Software\MyCo\SaveMyApp /s
    将注册表项 MyApp 下的所有子项和值复制到注册表项 SaveMyApp

  REG COPY \\ZODIAC\HKLM\Software\MyCo HKLM\Software\MyCo1
    将 ZODIAC 上注册表项 MyCo 下的所有值复制到当前机器上的
    注册表项 MyCo1

# REG SAVE /?

REG SAVE KeyName FileName [/y] [/reg:32 | /reg:64]

## KeyName
```bat
[\\Machine\]FullKey
```

- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
  FileName   要保存的磁盘文件名。如果没有指定路径，文件会在调用进程的
             当前文件夹中得到创建。

  /y         不用提示就强行覆盖现有文件。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG SAVE HKLM\Software\MyCo\MyApp AppBkUp.hiv
    将配置单元 MyApp 保存到当前文件夹中的文件 AppBkUp.hiv

# REG RESTORE /?

REG RESTORE KeyName FileName [/reg:32 | /reg:64]

## KeyName
```bat
[\\Machine\]FullKey
```

- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
  FileName   要还原的配置单元文件名。
             你必须使用 REG SAVE 来创建这个文件。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG RESTORE HKLM\Software\Microsoft\ResKit NTRKBkUp.hiv
    还原文件 NTRKBkUp.hiv，覆盖注册表项 ResKit

# REG LOAD /?

REG LOAD KeyName FileName [/reg:32 | /reg:64]

## KeyName
```bat
[\\Machine\]FullKey
```

- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
  FileName   要加载的配置单元文件名。
             你必须使用 REG SAVE 来创建这个文件。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG LOAD HKLM\TempHive TempHive.hiv
    将文件 TempHive.hiv 加载到注册表项 HKLM\TempHive

# REG UNLOAD /?

REG UNLOAD KeyName

## KeyName
```bat
[\\Machine\]FullKey
```

- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
例如:

  REG UNLOAD HKLM\TempHive
    卸载 HKLM 中的配置单元 TempHive

# REG COMPARE /?

REG COMPARE KeyName1 KeyName2 [/v ValueName | /ve] [Output] [/s]
            [/reg:32 | /reg:64]

## KeyName
```bat
[\\Machine\]FullKey
```

- `Machine` - 远程机器名称，省略当前机器的默认值。在远程机器上, 只有 HKLM 和 HKU 可用。
- `FullKey` - 以 `ROOTKEY\SubKey` 名称形式
- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
  ValueName  所选注册表项下的要比较的值的名称。
             省略时，该项下的所有值都会得到比较。

  /ve        比较空白值名称的值(默认)。

  /s         比较所有子项和值。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

  Output     [/oa | /od | /os | /on]
             省略时，只显示不同的结果。
    /oa      显示所有不同和匹配结果。
    /od      只显示不同的结果。
    /os      只显示匹配结果。
    /on      不显示结果。

返回代码:

  0 - 成功，比较的结果相同
  1 - 失败
  2 - 成功，比较的结果不同

注意:
  每个输出行前面显示的符号定义为:
  = 表示 FullKey1 等于 FullKey2 数据
  < 指的是 FullKey1 数据，与 FullKey2 数据不同
  > 指的是 FullKey2 数据，与 Fullkey1 数据不同

例如:

  REG COMPARE HKLM\Software\MyCo\MyApp HKLM\Software\MyCo\SaveMyApp
    将注册表项 MyApp 下的所有值跟 SaveMyApp 比较

  REG COMPARE HKLM\Software\MyCo HKLM\Software\MyCo1 /v Version
    比较注册表项 MyCo 和 MyCo1 下的值 Version

  REG COMPARE \\ZODIAC\HKLM\Software\MyCo \\. /s
    将 ZODIAC 上 HKLM\Software\MyCo 下的所有子项和值和当前机器上
    的相同项比较

# REG EXPORT /?

REG EXPORT KeyName FileName [/y] [/reg:32 | /reg:64]

## KeyName
```bat
[\\Machine\]FullKey
```

- `ROOTKEY` - 取值: `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`
- `SubKey`  - 在选择的 `ROOTKEY` 下的注册表项的全名

## 其他参数
  FileName   要导出的磁盘文件名。

  /y       不用提示就强行覆盖现有文件。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG EXPORT HKLM\Software\MyCo\MyApp AppBkUp.reg
    将注册表项 MyApp 的所有子项和值导出到文件 AppBkUp.reg

# REG IMPORT /?

REG IMPORT FileName[/reg:32 | /reg:64]

  FileName  要导入的磁盘文件名(只是本地机器)。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG IMPORT AppBkUp.reg
    从文件 AppBkUp.reg 导入注册表项

# REG FLAGS /?

REG FLAGS KeyName [QUERY |
                   SET [DONT_VIRTUALIZE] [DONT_SILENT_FAIL] [RECURSE_FLAG]]
                  [/reg:32 | /reg:64]

  Keyname    "HKLM\Software"[\SubKey] (仅限本地计算机上的这些密钥)。
    SubKey   HKLM\Software 下注册表项的全名。
  DONT_VIRTUALIZE DONT_SILENT_FAIL RECURSE_FLAG
   与 SET 一起使用；将设置在命令行上指定的标志，同时将清除没有指定的标志。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

示例:

  REG FLAGS HKLM\Software\MyCo\MyApp QUERY
    显示密钥 MyApp 的当前标志。

  REG FLAGS HKLM\Software\MyCo\MyApp SET DONT_VIRTUALIZE /s
    设置 MyApp 及其所有子密钥上的 DONT_VIRTUALIZE 标志
    (并清除 DONT_SILENT_FAIL 和 RECURSE_FLAG)
