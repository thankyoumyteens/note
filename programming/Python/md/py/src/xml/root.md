# 获取根节点

```py
from xml.etree import ElementTree as ET

tree = ET.parse('demo.xml')

# 根节点
root = tree.getroot()

print(root.tag)
```
