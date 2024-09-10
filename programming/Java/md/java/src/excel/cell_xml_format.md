# Excel 的 XML 格式

Office 2007 以后, 微软使用 Office Open XML(也称为 OpenXML 或 OOXML)作为 office 文件的技术规范。

Office Open XML 是一种基于 XML 的文件格式, 用于办公文档, 包括文字处理文档、电子表格、演示文稿以及图表、图形、形状等其他图形材料。该规范由微软开发, 并在 2006 年被 ECMA International 采纳为标准 ECMA-376。

ECMA-376 包括三种主要办公文档类型的不同规范: WordprocessingML(用于文字处理文档)、SpreadsheetML(用于电子表格文档)和 PresentationML(用于演示文档)。此外, 它还包括一些支持性标记语言, 最重要的是 DrawingML(用于绘图、形状和图表)。

Open XML 格式由 ECMA(欧洲计算机制造商协会)定义, 而另一个全球标准组织, 国际标准化组织(ISO), 也提供了一项 Open XML 标准, 称为 ISO/IEC 29500。

总的来说, ECMA-376 是一个定义了 Office Open XML 格式的国际标准, 它使得办公文档能够在不同的软件和平台之间进行有效的保存、交换和互操作。

## xlsx 目录结构

```
.
├── [Content_Types].xml
├── _rels
├── docProps
│   ├── app.xml
│   └── core.xml
└── xl
    ├── _rels
    │   └── workbook.xml.rels
    ├── sharedStrings.xml
    ├── styles.xml
    ├── theme
    │   └── theme1.xml
    ├── workbook.xml
    └── worksheets
        └── sheet1.xml
```

其中 `sharedStrings.xml` 文件存储了工作簿中使用的所有共享字符串, 以减少文件大小。

## 单元格的类型

Excel 单元格在 `.xlsx` 文件中的 XML 格式遵循 Office Open XML 标准。每个单元格在对应的 sheet 的 xml 文件中被定义:

```xml
<worksheet
    xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

    <sheetData>
        <!-- 每个row表示一行 -->
        <row r="1" spans="1:3">
            <c r="A1" t="s">
                <v>1</v>
            </c>
            <c r="B1" t="s">
                <v>2</v>
            </c>
            <c r="C1" t="s">
                <v>3</v>
            </c>
            <!-- More cells -->
        </row>
        <!-- More rows -->
    </sheetData>
    <!-- Other worksheet elements -->
</worksheet>
```

在这个示例中: 

- `<worksheet>` 是工作表的根元素。
- `<sheetData>` 包含了工作表中的所有行和单元格数据。
- `<row r="1" spans="1:3">` 表示这是第一行, 并且这一行至少包含从 A 列到 C 列的单元格。
- `<c r="A1" t="s">` 表示一个单元格, 其中 `r="A1"` 定义了单元格的位置(第 1 行第 1 列), `t="s"` 表示单元格的类型是字符串("s" 表示字符串类型, 其他类型还包括数字 "n"、公式 "f" 等)。
- `<v>` 元素包含了单元格的值, 这里 `v="1"`、`v="2"` 和 `v="3"` 分别表示 A1、B1 和 C1 单元格的值。

### 布尔类型

类型值为 `b`,  true 映射成数字 1。

```xml
<c r="A1" t="b">
    <v>1</v>
</c>
```

### 日期类型

类型值为 `d`, 日期类型的值是个浮点数。

```xml
<c r="A1" s="1">
    <v>44927.416678240741</v>
</c>
```

### 错误类型

类型值为 `e`, 表示这个单元格包含一个错误。

```xml
<c r="A1" t="e"/>
```

### 内联字符串类型

类型值为 `inlineStr`, 表示这个单元格的字符串并没有用共享字符串池子的值。

```xml
<c r="A1" t="inlineStr">
    <is>
        <t>Hello World</t>
    </is>
</c>
```

### 数字类型

类型值为 `n` 或为空。

```xml
<c r="A1">
    <v>100</v>
</c>
```

### 共享字符串类型

类型值为 `s`, v 节点的值可以看做一个指针, 指向共享字符串池(对应文件 sharedStrings.xml )中的字符串索引。

```xml
<c r="A1" t="s">
    <!-- sharedStrings.xml中索引为0的字符串 -->
    <v>0</v>
</c>
```

### 公式类型

类型值为 `f` 或为空, `<f>` 标签包含公式 `SUM(A1:C1)`, `<v>` 标签包含公式的计算结果。

```xml
<c r="A1" t="f">
  <f>SUM(A1:C1)</f>
  <v>6</v>
</c>
```
