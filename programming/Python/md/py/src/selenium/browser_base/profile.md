# 复用浏览器配置

浏览器配置文件会存储所有会话信息(包括 Cookie、登录状态、历史记录、扩展等)。让 Selenium 直接加载本地浏览器的配置文件，即可完全保持之前的登录状态。

chrome 浏览器配置文件的位置:

- Windows: `C:\Users\你的用户名\AppData\Local\Google\Chrome\User Data`
- Mac: `/Users/你的用户名/Library/Application Support/Google/Chrome/Default`

注意: 需要把配置文件的目录复制一份到其它目录, 否则会因文文件占用冲突而启动失败。

```py
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

opt = Options()
chrome_path = '/chrome-133.0.6871.0/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'
opt.binary_location = chrome_path

# 加载本地配置文件
# 指定配置文件所在的目录
opt.add_argument(r"--user-data-dir=/tmp/Default")
# 使用默认配置文件（一般无需修改）
opt.add_argument(r"--profile-directory=Default")

driver_path = '/chromedriver-133.0.6871.0/chromedriver'
ser = Service(driver_path)
driver = webdriver.Chrome(options=opt, service=ser)

driver.get('https://www.example.com')

sleep(10)
driver.quit()
```
