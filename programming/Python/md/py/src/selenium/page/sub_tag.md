# 定位子标签

```py
# 定位父标签
p_node = driver.find_element(By.ID, 'form1')
# 根据父标签定位子标签
e = p_node.find_element(By.ID, 'btn1')
```
