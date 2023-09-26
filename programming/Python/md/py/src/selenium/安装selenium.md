# 安装selenium

```
pip install selenium
```

# 下载浏览器驱动

浏览器驱动需要与浏览器版本一致

- Chrome浏览器驱动：[chromedriver](https://mirrors.huaweicloud.com/chromedriver/)
- Firefox浏览器驱动：[geckodriver](https://repo.huaweicloud.com/geckodriver/)
- IE浏览器驱动：[IEDriverServer](http://selenium-release.storage.googleapis.com/index.html)
- Edge浏览器驱动：[MicrosoftWebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver)
- Opera浏览器驱动：[operadriver](https://repo.huaweicloud.com/operadriver/)
- PhantomJS浏览器驱动：[phantomjs](http://phantomjs.org/)

# 测试能否正常使用

```python
from selenium import webdriver


driver = webdriver.Firefox('驱动路径')   # Firefox浏览器
driver = webdriver.Chrome('驱动路径')    # Chrome浏览器
driver = webdriver.Ie('驱动路径')        # Internet Explorer浏览器
driver = webdriver.Edge('驱动路径')      # Edge浏览器
driver = webdriver.Opera('驱动路径')     # Opera浏览器
driver = webdriver.PhantomJS('驱动路径')   # PhantomJS

# 打开网页
driver.get(url) # 打开url网页 比如 driver.get("http://www.baidu.com")
```
