# 模拟复杂交互

在 Selenium 中，ActionChains 是一个用于处理复杂用户交互的类，它允许你模拟一系列连续的鼠标和键盘操作，实现更贴近真实用户行为的自动化操作。

ActionChains 可以将多个操作按顺序组合成一个动作链，然后通过 perform()方法一次性执行，特别适合处理需要连续步骤的交互。

基本使用流程：

1. 创建 ActionChains 实例，绑定到浏览器驱动
2. 链式调用各种操作方法（如 click()、send_keys()等）
3. 调用 perform()执行整个动作链

```py
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 创建动作链对象
actions = ActionChains(driver)

# 组合操作（点击输入框 -> 输入文本 -> 按Enter）
input_box = driver.find_element(By.ID, "search-box")
actions.click(input_box) \
       .send_keys("Selenium") \
       .send_keys(Keys.ENTER) \
       .perform()  # 链式调用多个操作
```
