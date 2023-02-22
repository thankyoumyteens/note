# 创建ChromeOptions

selenium启动配置参数接收是ChromeOptions类，创建方式如下：
```python
from selenium import webdriver
option = webdriver.ChromeOptions()
```
# ChromeOptions的方法

- `add_argument()` 添加启动参数
- `add_extension()` 和 `add_encoded_extension()` 添加扩展应用
- `add_experimental_option()` 添加实验性质的设置参数
- `debugger_address()` 设置调试器地址

# 常用配置参数

```py
# 无界面模式
options.add_argument('headless')

# 指定用户客户端-模拟手机浏览
options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')

# 禁用图片加载
options.add_argument('blink-settings=imagesEnabled=false')

# 隐身模式
options.add_argument('incognito')

# 自动打开开发者工具
options.add_argument("auto-open-devtools-for-tabs")

# 设置窗口尺寸，注意宽高之间使用逗号而不是x
options.add_argument('window-size=300,600')

# 设置窗口启动位置（左上角坐标）
options.add_argument('window-position=120,0')

# 禁用gpu渲染
options.add_argument('disable-gpu')

# 全屏启动
options.add_argument('start-fullscreen')

# 全屏启动，无地址栏
options.add_argument('kiosk') 

 # 启动时，不激活（前置）窗口
options.add_argument('no-startup-window') 
```
