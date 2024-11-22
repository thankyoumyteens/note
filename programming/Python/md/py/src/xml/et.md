# 解析 xml

使用 Python 内置的 ElementTree 解析。

## 常用属性

- tag: 字符串, xml 的标签
- attrib: dict, xml 的属性
- text: 字符串, xml 的标签体

```xml
<!-- tag: 'demo_tag' -->
<!-- attrib: {'demo_attr': 'abc'} -->
<!-- text: 'content' -->
<demo_tag demo_attr="abc">content</demo_tag>
```

## 示例 xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<demo_root name="demo">
   <name type="string">
       <value>zhangsan</value>
   </name>
   <age type="int">
       <value>10</value>
   </age>
</demo_root>
```

## 获取根节点

```py
from xml.etree import ElementTree as ET

# 解析xml
tree = ET.parse('demo.xml')

# 根节点
root = tree.getroot()

print(root.tag)
print(root.attrib)
```

## 使用索引访问子节点

```py
root = tree.getroot()

# 获取age的子节点value
age_value = root[1][0]

print(age_value.tag)
print(age_value.text)
```

## 遍历子节点

```py
root = tree.getroot()

# 遍历直接子节点
for child in root:
    print(child.tag, child.attrib)

# 递归遍历所有子节点
for child in root.iter():
    print(child.tag, child.attrib)
```

## 查找

```py
root = tree.getroot()

# 查找子节点中tag为demo_tag的标签
for target in root.iter('demo_tag'):
    print(target.tag)

# 使用tag或xpath查找
for target in root.findall('name/value'):
    print(target.tag)

# 返回第一个匹配的子节点
target = root.find('name/value')
print(target.tag)
```
