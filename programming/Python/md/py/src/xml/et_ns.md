# 解析命名空间

ElementTree 中带命名空间的标签格式:

```py
{命名空间}标签
```

示例 xml:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<my_ns:document xmlns:my_ns="http://xxxxxxx">
    <my_ns:body>
        <!-- ... -->
    </my_ns:body>
</my_ns:document>
```

解析:

```py
from xml.etree import ElementTree as ET
# 命名空间
my_ns = '{http://xxxxxxx}'
# 解析xml
tree = ET.parse('demo.xml')
# 根节点 my_ns:document
root = tree.getroot()
# 查找子节点中tag为demo_tag的标签
for target in root.iter(f'{my_ns}body'):
    print(target.tag)
```
