# 不支持安全连接问题

不一定生效, 很玄学

```py
# 忽略证书错误
opt.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=opt, service=ser)
```

## 方法 2

直接点击"继续访问网站"按钮

```py
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def fuck_chrome(chrome_driver: WebDriver):
    try:
        while True:
            time.sleep(1)
            proceed_button = chrome_driver.find_element(By.ID, 'proceed-button')
            print(proceed_button)
            proceed_button.click()
    except NoSuchElementException:
        return
```
