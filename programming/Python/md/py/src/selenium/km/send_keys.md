# 模拟键盘输入

```py
# 定位到输入框
input_element = driver.find_element(By.ID, "input-field")

# 输入文本
input_element.send_keys("Hello World")

# 模拟按下Enter键
input_element.send_keys(Keys.ENTER)

# 模拟按下Tab键（切换到下一个输入框）
input_element.send_keys(Keys.TAB)

# 模拟组合键：Ctrl+A（全选）
input_element.send_keys(Keys.CONTROL, 'a')

# 模拟组合键：Ctrl+C（复制）
input_element.send_keys(Keys.CONTROL, 'c')

# 模拟组合键：Ctrl+V（粘贴）
input_element.send_keys(Keys.CONTROL, 'v')

# 模拟按下删除键
input_element.send_keys(Keys.BACK_SPACE)

# 模拟按下空格键
input_element.send_keys(Keys.SPACE)
```
