# Linux 和 windows 双系统时间不一致

UTC（Universal Time Coordinated）即协调世界时, 以原子时长为基础, 精度好。

RTC（Real-Time Clock）实时时钟, 在计算机领域称为硬件时钟, 顾名思义电脑上有个硬件保存了时间信息。让我们下次启动之后, 时间还可以正常显示。

windows 把 RTC 时间当作本地时间——在中国, 就是东八区时间。而 Linux 会将 RTC 时间当作 UTC 时间。

所以：Linux 会将 RTC 设置成 UTC 时间。显示时间会根据时区显示, 例如在中国, 显示时间时会自动+8 小时。

Linux 关机, 启动 windows 后。Window 把 RTC 当成了本时区的时间, 直接显示。但是 RTC 已经被 Linux 设置成了 UTC 时间, 所以显示时间会晚 8 个小时。

修改 windows, 让其将 RTC 硬件时间当作 UTC 时间。因为 Linux 使用 RTC 时间可能会导致一些程序发生错误。

以管理员身份打开 「PowerShell」, 输入以下命令:

```sh
Reg add HKLM\SYSTEM\CurrentControlSet\Control\TimeZoneInformation /v RealTimeIsUniversal /t REG_DWORD /d 1
```

或者打开「注册表编辑器」, 定位到 计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation 目录下, 新建一个 DWORD 类型, 名称为 RealTimeIsUniversal 的键, 并修改键值为 1 即可。
