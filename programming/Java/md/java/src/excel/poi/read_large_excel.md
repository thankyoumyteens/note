# excel 读取

按 xml 方式解析 excel。

继承 `DefaultHandler` 类, 重写 `startElement()`, `characters()`, `endElement()` 方法。

- `startElement()` 获取单元格的类型(如日期、数字、字符串等)
- `characters()` 获取该单元格对应的索引值或是内容值。如果单元格类型是字符串则获取的是字符串池的索引值, 其它类型则获取的就是内容
- `endElement()` 根据 `startElement()` 的单元格类型和 `characters()` 的索引值或内容值, 最终得出单元格的内容

### 1. 用来保存单元格数据

```java
public class CellInfo {

    public int row;
    public int col;
    public String value;

    public CellInfo(int row, int col, String value) {
        this.row = row;
        this.col = col;
        this.value = value;
    }
}
```

### 2. 自定义 sheet 处理类 SheetHandler

```java
import org.apache.poi.ss.util.CellReference;
import org.apache.poi.xssf.model.SharedStrings;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

import java.util.ArrayList;
import java.util.List;

public class SheetHandler extends DefaultHandler {
    public List<CellInfo> cellInfoList;

    // 字符串池
    private final SharedStrings stringPool;
    // 单元格的值或索引
    // 如果单元格类型是字符串, 则valueOrIndex保存的是字符串池索引
    // 如果单元格类型是其它类型, 则valueOrIndex保存的是单元格的值
    private String valueOrIndex;
    // 单元格类型是字符串
    private boolean isString;
    // 单元格类型是内联字符串
    private boolean isInlineStr;
    // 当前单元格的行列
    private int row;
    private int col;

    public SheetHandler(SharedStrings sp) {
        this.stringPool = sp;
        this.cellInfoList = new ArrayList<>();
    }

    /**
     * 该方法自动被调用, 每读一行调用n次, n是这一行有多少列
     * 调用顺序:
     * 第1行第1列,
     * 第1行第2列,
     * 第1行第3列,
     * ...
     * 第2行第1列,
     * 第2行第2列,
     * 第2行第3列,
     * ...
     */
    @Override
    public void startElement(String uri, String localName, String name, Attributes attributes) {
        // c 代表单元格
        if (name.equals("c")) {
            // 获取单元格的位置, 如: A1 B1
            String cellPos = attributes.getValue("r");
            CellReference cellReference = new CellReference(cellPos);
            row = cellReference.getRow();
            col = cellReference.getCol();
            // 获取单元格类型
            String cellType = attributes.getValue("t");

            // 字符串类型, 交给后续的endElement方法处理
            isString = cellType != null && cellType.equals("s");
            // 内联字符串类型, 交给后续endElement处理
            isInlineStr = cellType != null && cellType.equals("inlineStr");
        }
        valueOrIndex = "";
    }

    /**
     * 用于获取该单元格对应的索引值或是内容值
     * 如果单元格类型是字符串则获取的是索引值
     * 其它类型获取的是内容值
     */
    public void characters(char[] ch, int start, int length) {
        valueOrIndex += new String(ch, start, length);
    }

    /**
     * 根据startElement()的单元格数字类型和characters()的索引值或内容值, 最终得出单元格的内容值
     */
    @Override
    public void endElement(String uri, String localName, String name) {
        String cellValue = valueOrIndex;
        if (isString) {
            // valueOrIndex是索引, 从字符串池中取出对应的值
            int idx = Integer.parseInt(valueOrIndex);
            cellValue = stringPool.getItemAt(idx).toString();
            isString = false;
        }

        // v: 单元格内容
        if (name.equals("v")) {
            cellInfoList.add(new CellInfo(row, col, cellValue));
        }
        // is: 内联字符串内容
        if (isInlineStr && name.equals("is")) {
            isInlineStr = false;
            cellInfoList.add(new CellInfo(row, col, cellValue));
        }
    }
}
```

### 3. 通过 SheetHandler 读取

```java
public static Map<String, List<CellInfo>> readAllSheets(String filePath) throws Exception {
    Map<String, List<CellInfo>> resultMap = new HashMap<>();
    try (OPCPackage pkg = OPCPackage.open(filePath)) {
        XSSFReader r = new XSSFReader(pkg);
        // 获取excel的字符串池
        SharedStrings sp = r.getSharedStringsTable();
        // 用于解析xml
        SAXParserFactory parserFactory = SAXParserFactory.newInstance();
        SAXParser parser = parserFactory.newSAXParser();
        XMLReader reader = parser.getXMLReader();
        // 注册自定义的sheet处理类
        SheetHandler handler = new SheetHandler(sp);
        reader.setContentHandler(handler);

        // 遍历读取所有sheet
        XSSFReader.SheetIterator sheets = (XSSFReader.SheetIterator) r.getSheetsData();
        while (sheets.hasNext()) {
            try (InputStream sheet = sheets.next()) {
                // sheet名
                String sheetName = sheets.getSheetName();
                InputSource sheetSource = new InputSource(sheet);
                reader.parse(sheetSource);

                // 获取结果
                List<CellInfo> cellInfoList = handler.cellInfoList;
                resultMap.put(sheetName, cellInfoList);
                handler.cellInfoList = new ArrayList<>();
            }
        }
    }
    return resultMap;
}
```
