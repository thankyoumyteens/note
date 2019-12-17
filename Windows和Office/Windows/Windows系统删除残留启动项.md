# Windows系统删除残留启动项

* 按下win+r打开运行对话框, 在里面输入regedit。
* 打开注册表后, 将注册表定位于`\HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run` 地址下, 这时会出现许多值, 选择你要删除启动项软件的值, 右击删除。
* 这时再打开启动项管理器, 就会发现垃圾软件的启动项已经被删除了。
