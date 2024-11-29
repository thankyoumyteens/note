# 使用下标访问子节点

```py
# <?xml version="1.0" encoding="utf-8"?>
# <demo_root name="demo">
#    <name type="string">
#        <value>zhangsan</value>
#    </name>
#    <age type="int">
#        <value>10</value>
#    </age>
# </demo_root>

from xml.etree import ElementTree as ET

tree = ET.parse('demo.xml')
root = tree.getroot()

# 获取age的子节点value
value = root[1][0]

print(value.text)
```
