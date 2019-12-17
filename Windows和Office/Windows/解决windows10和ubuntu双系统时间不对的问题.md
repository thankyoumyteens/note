# 解决windows10和ubuntu双系统时间不对的问题

## 原因

UTC即Universal Time Coordinated, 协调世界时(世界统一时间)GMT 即Greenwich Mean Time, 格林尼治平时Windows 与 Mac/Linux 看待系统硬件时间的方式是不一样的: Windows把计算机硬件时间当作本地时间(local time), 所以在Windows系统中显示的时间跟BIOS中显示的时间是一样的。Linux/Unix/Mac把计算机硬件时间当作 UTC,  所以在Linux/Unix/Mac系统启动后在该时间的基础上, 加上电脑设置的时区数(比如我们在中国, 它就加上"8"), 因此, Linux/Unix/Mac系统中显示的时间总是比Windows系统中显示的时间快8个小时。所以, 当你在Linux/Unix/Mac系统中, 把系统现实的时间设置正确后, 其实计算机硬件时间是在这个时间上减去8小时, 所以当你切换成Windows系统后, 会发现时间慢了8小时。就是这样个原因。

## 解决

Ubuntu里终端输入代码如下: 

先在ubuntu下更新一下时间, 确保时间无误: 
```
sudo apt-get update
sudo apt-get install ntpdate
sudo ntpdate time.windows.com
```
然后将时间更新到硬件上: 
```
sudo hwclock --localtime --systohc
```
重新进入windows10, 发现时间恢复正常了！
