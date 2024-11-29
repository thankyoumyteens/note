# 查找子节点

```py
from xml.etree import ElementTree as ET

tree = ET.parse('demo.xml')
root = tree.getroot()

# 查找tag为demo_tag的所有子节点
for target in root.iter('demo_tag'):
    print(target.tag)

# 使用tag或xpath查找所有匹配的子节点
for target in root.findall('name/value'):
    print(target.tag)

# 返回第一个匹配的子节点
target = root.find('name/value')
print(target.tag)
```
