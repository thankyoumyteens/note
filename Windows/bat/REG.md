# REG /?

REG Operation [Parameter List]

  Operation  [ QUERY   | ADD    | DELETE  | COPY    |
               SAVE    | LOAD   | UNLOAD  | RESTORE |
               COMPARE | EXPORT | IMPORT  | FLAGS ]

返回代码: (除了 REG COMPARE)

  0 - 成功
  1 - 失败

要得到有关某个操作的帮助，请键入:

  REG Operation /?

例如:

  REG QUERY /?
  REG ADD /?
  REG DELETE /?
  REG COPY /?
  REG SAVE /?
  REG RESTORE /?
  REG LOAD /?
  REG UNLOAD /?
  REG COMPARE /?
  REG EXPORT /?
  REG IMPORT /?
  REG FLAGS /?

# REG QUERY /?

REG QUERY KeyName [/v [ValueName] | /ve] [/s]
          [/f Data [/k] [/d] [/c] [/e]] [/t Type] [/z] [/se Separator]
          [/reg:32 | /reg:64]

  KeyName  [\\Machine\]FullKey
           Machine - 远程机器名称，省略当前机器的默认值。在远程机器上
                     只有 HKLM 和 HKU 可用。
           FullKey - 以 ROOTKEY\SubKey 名称形式
                ROOTKEY - [ HKLM | HKCU | HKCR | HKU | HKCC ]
                SubKey  - 在选择的 ROOTKEY 下的注册表项的全名

  /v       具体的注册表项值的查询。
           如果省略，会查询该项的所有值。

           只有与 /f 开关一起指定的情况下，此开关的参数才是可选的。它指定
           只在值名称中搜索。

  /ve      查询默认值或空值名称(默认)。

  /s       循环查询所有子项和值(如 dir /s)。

  /se      为 REG_MULTI_SZ 在数据字符串中指定分隔符(长度只为 1 个字符)。
           默认分隔符为 "\0"。

  /f       指定搜索的数据或模式。
           如果字符串包含空格，请使用双引号。默认为 "*"。

  /k       指定只在项名称中搜索。

  /d       指定只在数据中搜索。

  /c       指定搜索时区分大小写。
           默认搜索为不区分大小写。

  /e       指定只返回完全匹配。
           默认是返回所有匹配。

  /t       指定注册表值数据类型。
           有效的类型是:
             REG_SZ, REG_MULTI_SZ, REG_EXPAND_SZ,
             REG_DWORD, REG_QWORD, REG_BINARY, REG_NONE
           默认为所有类型。

  /z       详细: 显示值名称类型的数字等值。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

示例:

  REG QUERY HKLM\Software\Microsoft\ResKit /v Version
    显示注册表值 Version 的值

  REG QUERY \\ABC\HKLM\Software\Microsoft\ResKit\Nt\Setup /s
    显示远程机器 ABC 上的、在注册表项设置下的所有子项和值

  REG QUERY HKLM\Software\Microsoft\ResKit\Nt\Setup /se #
    用 "#" 作为分隔符，显示类型为 REG_MULTI_SZ 的所有值名称的所有
    子项和值。

  REG QUERY HKLM /f SYSTEM /t REG_SZ /c /e
    以区分大小写的形式显示项、值和数据和数据类型 REG_SZ
    的、在 HKLM 更目录下的、"SYSTEM" 出现的精确次数

  REG QUERY HKCU /f 0F /d /t REG_BINARY
    显示在 HKCU 根目录下、数据类型为 REG_BINARY 的数据的项、值和
    数据的 "0F" 出现的次数。

  REG QUERY HKLM\SOFTWARE /ve
    显示在 HKLM\SOFTWARE 下的项、值和数据(默认)

# REG ADD /?

REG ADD KeyName [/v ValueName | /ve] [/t Type] [/s Separator] [/d Data] [/f]
        [/reg:32 | /reg:64]

  KeyName  [\\Machine\]FullKey
           Machine  远程机器名 - 忽略默认到当前机器。远程机器上
                    只有 HKLM 和 HKU 可用。
           FullKey  ROOTKEY\SubKey
           ROOTKEY  [ HKLM | HKCU | HKCR | HKU | HKCC ]
           SubKey   所选 ROOTKEY 下注册表项的完整名称。

  /v       所选项之下要添加的值名称。

  /ve      为注册表项添加空白值名称(默认)。

  /t       RegKey 数据类型
           [ REG_SZ    | REG_MULTI_SZ | REG_EXPAND_SZ |
             REG_DWORD | REG_QWORD    | REG_BINARY    | REG_NONE ]
           如果忽略，则采用 REG_SZ。

  /s       指定一个在 REG_MULTI_SZ 数据字符串中用作分隔符的字符
           如果忽略，则将 "\0" 用作分隔符。

  /d       要分配给添加的注册表 ValueName 的数据。

  /f       不用提示就强行覆盖现有注册表项。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG ADD \\ABC\HKLM\Software\MyCo
    添加远程机器 ABC 上的一个注册表项 HKLM\Software\MyCo

  REG ADD HKLM\Software\MyCo /v Data /t REG_BINARY /d fe340ead
    添加一个值(名称: Data，类型: REG_BINARY，数据: fe340ead)

  REG ADD HKLM\Software\MyCo /v MRU /t REG_MULTI_SZ /d fax\0mail
    添加一个值(名称: MRU，类型: REG_MULTI_SZ，数据: fax\0mail\0\0)

  REG ADD HKLM\Software\MyCo /v Path /t REG_EXPAND_SZ /d ^%systemroot^%
    添加一个值(名称: Path，类型: REG_EXPAND_SZ，数据: %systemroot%)
    注意: 在扩充字符串中使用插入符号 ( ^ )

# REG DELETE /?

REG DELETE KeyName [/v ValueName | /ve | /va] [/f] [/reg:32 | /reg:64]

  KeyName    [\\Machine\]FullKey
    远程机器名 - 如果省略，默认情况下将使用当前机器。
             远程机器上只有 HKLM 和 HKU 可用。
    FullKey  ROOTKEY\SubKey
    ROOTKEY  [ HKLM | HKCU | HKCR | HKU | HKCC ]
    SubKey   所选 ROOTKEY 下面的注册表项的全名。

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

  KeyName    [\\Machine\]FullKey
    Machine  远程机器名 - 如果省略，默认情况下将使用当前机器。
             远程机器上只有 HKLM 和 HKU 可用。
    FullKey  ROOTKEY\SubKey
    ROOTKEY  [ HKLM | HKCU | HKCR | HKU | HKCC ]
    SubKey   所选 ROOTKEY 下的注册表项的全名。

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

  KeyName    ROOTKEY\SubKey
    ROOTKEY  [ HKLM | HKCU | HKCR | HKU | HKCC ]
    SubKey   所选 ROOTKEY 下的注册表项的全名。

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

  KeyName    ROOTKEY\SubKey (只是本地机器)
    ROOTKEY  [ HKLM | HKCU | HKCR | HKU | HKCC ]
    SubKey   要将配置单元文件还原到的注册表项全名。
             覆盖现有项的值和子项。

  FileName   要还原的配置单元文件名。
             你必须使用 REG SAVE 来创建这个文件。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG RESTORE HKLM\Software\Microsoft\ResKit NTRKBkUp.hiv
    还原文件 NTRKBkUp.hiv，覆盖注册表项 ResKit

# REG LOAD /?

REG LOAD KeyName FileName [/reg:32 | /reg:64]

   KeyName    ROOTKEY\SubKey (只是本地机器)
    ROOTKEY  [ HKLM | HKU ]
    SubKey   要将配置单元文件加载进的注册表项名称。创建一个新的注册表项。

  FileName   要加载的配置单元文件名。
             你必须使用 REG SAVE 来创建这个文件。

 /reg:32  指定应该使用 32 位注册表视图访问的注册表项。

 /reg:64  指定应该使用 64 位注册表视图访问的注册表项。

例如:

  REG LOAD HKLM\TempHive TempHive.hiv
    将文件 TempHive.hiv 加载到注册表项 HKLM\TempHive

# REG UNLOAD /?

REG UNLOAD KeyName

  KeyName    ROOTKEY\SubKey (只是本地机器)
    ROOTKEY  [ HKLM | HKU ]
    SubKey   要卸载的配置单元的注册表项名称。

例如:

  REG UNLOAD HKLM\TempHive
    卸载 HKLM 中的配置单元 TempHive

# REG COMPARE /?

REG COMPARE KeyName1 KeyName2 [/v ValueName | /ve] [Output] [/s]
            [/reg:32 | /reg:64]

  KeyName    [\\Machine\]FullKey
    Machine  远程机器名 - 如果省略，默认情况下将使用当前机器。
             远程机器上只有 HKLM 和 HKU 可用。
    FullKey  ROOTKEY\SubKey
             如果没有指定 FullKey2，FullKey2 则跟 FullKey1 相同。
    ROOTKEY  [ HKLM | HKCU | HKCR | HKU | HKCC ]
    SubKey   所选 ROOTKEY 下的注册表项的全名。

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

  Keyname    ROOTKEY[\SubKey] (只是本地机器)。
    ROOTKEY  [ HKLM | HKCU | HKCR | HKU | HKCC ]
    SubKey   所选 ROOTKEY 下的注册表项的全名。

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
