# 基本使用

### 1. 安装

```sh
pip install selenium==4.27.1
```

### 2. 下载浏览器驱动

浏览器驱动需要与浏览器版本一致

- Chrome 浏览器: [chrome-for-testing](https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json)
- Firefox 浏览器驱动: [geckodriver](https://repo.huaweicloud.com/geckodriver/)
- IE 浏览器驱动: [IEDriverServer](http://selenium-release.storage.googleapis.com/index.html)
- Edge 浏览器驱动: [MicrosoftWebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver)
- Opera 浏览器驱动: [operadriver](https://repo.huaweicloud.com/operadriver/)
- PhantomJS 浏览器驱动: [phantomjs](http://phantomjs.org/)

### 3. 使用

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 指定浏览器路径
opt = Options()
# 注意: mac上的路径要写到最里层
chrome_path = '/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
opt.binary_location = chrome_path

# 指定驱动路径
driver_path = '/chromedriver-133.0.6871.0/chromedriver'
ser = Service(driver_path)

# 初始化 WebDriver
driver = webdriver.Chrome(options=opt, service=ser)

# 打开网页
driver.get('https://www.example.com')

# 关闭浏览器
driver.quit()
```
