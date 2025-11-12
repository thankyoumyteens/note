# 定位直接子标签

```py
# 定位父标签
p_node = driver.find_element(By.ID, 'form1')
# 根据父标签定位直接子级
li_list = p_node.find_elements(By.XPATH, './li')
```
