# 定位子标签

```py
# 定位父标签
p_node = driver.find_element(By.ID, 'form1')
# 根据父标签定位子标签(会递归查找所有下级)
div_list = p_node.find_elements(By.TAG_NAME, 'div')
```
