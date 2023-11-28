# 安装selenium

```
pip install selenium==4.9.0
```

# 下载浏览器驱动

浏览器驱动需要与浏览器版本一致

- Chrome浏览器: [ungoogled-chromium](https://ungoogled-software.github.io/ungoogled-chromium-binaries/releases/windows/32bit/112.0.5615.138-1)
- Chrome浏览器驱动: [chromedriver](https://chromedriver.chromium.org/downloads)
- Firefox浏览器驱动: [geckodriver](https://repo.huaweicloud.com/geckodriver/)
- IE浏览器驱动: [IEDriverServer](http://selenium-release.storage.googleapis.com/index.html)
- Edge浏览器驱动: [MicrosoftWebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver)
- Opera浏览器驱动: [operadriver](https://repo.huaweicloud.com/operadriver/)
- PhantomJS浏览器驱动: [phantomjs](http://phantomjs.org/)

# 测试能否正常使用

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

# 指定chrome路径
opt = Options()
opt.binary_location = "C:/ungoogled-chromium_112.0.5615.138-1.1_windows/chrome.exe"
# 指定chromedriver路径
driver_path = "C:/ChromeDriver_112.0.5615.28_win32/chromedriver.exe"

driver = webdriver.Chrome(options=opt, executable_path=driver_path)
# 设置浏览器的大小
driver.set_window_size(1400,800)
# 打开网页
driver.get("https://www.baidu.com")
sleep(3)
```
