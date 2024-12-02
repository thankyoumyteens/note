# 等待标签出现

```py
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 每0.5秒尝试一次定位, 等待时间超过100秒则报错
# 定位到标签后返回该标签
e = WebDriverWait(driver, 100, 0.5).until(
    EC.presence_of_element_located(('id', 'btn1'))
)

print(e)
```

expected_conditions 中常用的函数:

- `presence_of_element_located`: 标签是否存在于页面的 DOM 树中, 如果是, 返回该标签(单个标签), 否则报错
- `presence_of_all_elements_located`: 定位的标签范围内, 是否至少有一个标签存在于页面 DOM 树中, 如果是, 返回满足条件的所有标签组成的 List, 否则返回空 List
- `visibility_of_element_located`: 特定标签是否存在于页面 DOM 树中并且可见, 如果是, 返回该标签(单个标签), 否则报错
- `visibility_of_any_elements_located`: 定位的标签范围内, 是否至少有一个标签存在于页面 DOM 树中并且可见, 如果是, 返回满足条件的所有标签组成的 List, 否则返回空 List
- `visibility_of_all_elements_located`: 定位的标签范围内, 是否所有标签都存在于页面 DOM 树中并且可见, 如果是, 返回满足条件的所有标签组成的 List, 否则返回空 List
