# Linux连接wifi

首先输入`sudo iwlist wlan0 scan`扫描周边wifi信号, 出来的结果每个cell就是对应一个热点, 其中的ESSID就是wifi的名称。

然后编辑配置文件就行了, 输入`sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`, 在这个文件最后添加wifi的名字和密码
```
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=wheel
update_config=1

network={
	ssid="wifi name"
	scan_ssid=1
	psk="password"
	key_mgmt=WPA-PSK
}
```
最后重启, 输入`sudo shutdown -r now`, 重启后自动连接wifi网络
