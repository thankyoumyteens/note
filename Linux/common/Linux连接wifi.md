# Linux连接wifi

扫描周边wifi
```
sudo iwlist wlan0 scan
```
然后编辑配置文件
```
sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
```
在这个文件最后添加wifi的名字和密码
```
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=wheel
update_config=1

network={
	ssid="wifi名"
	scan_ssid=1
	psk="wifi密码"
	key_mgmt=WPA-PSK
}
```
重启后自动连接wifi网络
```
sudo shutdown -r now
```
