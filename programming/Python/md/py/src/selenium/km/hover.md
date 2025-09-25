# 模拟鼠标悬停

```py
from selenium.webdriver.common.action_chains import ActionChains

menu = driver.find_element_by_css_selector("#menu")
# 模拟鼠标悬停
ActionChains(driver).move_to_element(menu).perform()
time.sleep(2)
```
