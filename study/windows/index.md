# 你需要TrustedInstaller提供的权限才能修改此文件

## 方法一

* 右击需要修改的文件-属性
* 切换到“安全”选项卡，点击“高级”按钮。
* 切换到“所有者”选项卡, 一般情况下默认所有者为TrustedInstaller（没有影响），单击“编辑”按钮
* 弹出的窗口中的"将所有者更改为"选择当前计算机的登陆用户名，点击确定
* 如果弹出窗口，直接点确定
* 后面的窗口都点击确定
* 再次右击该文件，属性，安全，编辑
* 选择当前用户名，勾选“允许”下的完全控制，然后点击确定
* 如果出现此窗口，点击确定。
* 点击确定关闭前面打开的几个窗口，这时就可以自由修改或删除此文件/文件夹了。

## 方法二: 右键菜单添加"获取TrustedInstaller权限"

编写扩展名为reg的文件
```
Windows Registry Editor Version 5.00
[HKEY_CLASSES_ROOT\*\shell\runas]
@="获取TrustedInstaller权限"
[HKEY_CLASSES_ROOT\*\shell\runas\command]
@="cmd.exe /c takeown /f \"%1\" && icacls \"%1\" /grant administrators:F"
"IsolatedCommand"="cmd.exe /c takeown /f \"%1\" && icacls \"%1\" /grant administrators:F"
[HKEY_CLASSES_ROOT\Directory\shell\runas]
@="获取TrustedInstaller权限"
"NoWorkingDirectory"=""
[HKEY_CLASSES_ROOT\Directory\shell\runas\command]
@="cmd.exe /c takeown /f \"%1\" /r /d y && icacls \"%1\" /grant administrators:F /t"
"IsolatedCommand"="cmd.exe /c takeown /f \"%1\" /r /d y && icacls \"%1\" /grant administrators:F /t"
```

# 桌面图标变成白块

主要是由于桌面图标缓存出现问题所导致

按住键盘的“WIN+R”键，然后在弹出的 运行对话框中输入`ie4uinit -show`，再点击回车

如果不行，我们还有最后一招

Windows 8、Windows10电脑进入`C:\Users\用户名\AppData\Local` 位置，
Windows7及以下操作系统进入`C:\Documents and Settings\用户名\Local Settings\Application Data` 下。
找到名为`IconCache.db`的隐藏文件，记得先开启显示所有隐藏文件，然后将其删除，重启电脑就可以了。

# Windows系统删除残留启动项

* 按下win+r打开运行对话框，在里面输入regedit。
* 打开注册表后，将注册表定位于`\HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run` 地址下，这时会出现许多值，选择你要删除启动项软件的值，右击删除。
* 这时再打开启动项管理器，就会发现垃圾软件的启动项已经被删除了。

