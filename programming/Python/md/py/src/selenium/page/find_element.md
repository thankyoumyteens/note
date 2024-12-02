# 定位 HTML 标签

```py
# 根据id定位
e = driver.find_element(By.ID, 'btnId')
# 根据name定位
e = driver.find_element(By.NAME, 'btnName')
# 根据class定位
e = driver.find_element(By.CLASS_NAME, 'btnClass')
# 根据标签定位
e = driver.find_element(By.TAG, 'div')
# xpath定位
e = driver.find_element(By.XPATH, 'xPath')
# css定位
e = driver.find_element(By.CSS_SELECTOR, '#btnId')

# 根据class定位多个标签
e_list = driver.find_elements(By.CLASS_NAME, 'btnClass')
```
