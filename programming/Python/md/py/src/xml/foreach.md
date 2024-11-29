# 遍历子节点

```py
from xml.etree import ElementTree as ET

tree = ET.parse('demo.xml')
root = tree.getroot()

# 遍历直接子节点
for child in root:
    print(child.tag)

# 递归遍历所有子节点
for child in root.iter():
    print(child.tag)
```
