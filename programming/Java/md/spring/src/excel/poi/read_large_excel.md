# 超大 excel 读取

继承 `DefaultHandler` 类，重写 `startElement()`, `characters()`, `endElement()` 方法。

- `startElement()` 获取单元格的类型（如日期、数字、字符串等）
- `characters()` 获取该单元格对应的索引值或是内容值。如果单元格类型是字符串则获取的是字符串池的索引值, 其它类型则获取的就是内容
- `endElement()` 根据 `startElement()` 的单元格类型和 `characters()` 的索引值或内容值，最终得出单元格的内容

```java
import org.apache.poi.openxml4j.exceptions.OpenXML4JException;
import org.apache.poi.openxml4j.opc.OPCPackage;
import org.apache.poi.xssf.eventusermodel.XSSFReader;
import org.apache.poi.xssf.model.SharedStringsTable;
import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import java.io.IOException;
import java.io.InputStream;
import java.util.Iterator;

public class ExcelReader {

    public static class SheetHandler extends DefaultHandler {
        // 字符串池
        private final SharedStringsTable stringPool;
        // 单元格的值或索引
        private String valueOrIndex;
        // 单元格类型是字符串
        private boolean isString;
        // 单元格类型是内联字符串
        private boolean isInlineStr;

        public SheetHandler(SharedStringsTable sst) {
            this.stringPool = sst;
        }

        /**
         * 该方法自动被调用，每读一行调用n次, n是这一行有多少列
         * 调用顺序:
         *     第1行第1列,
         *     第1行第2列,
         *     第1行第3列,
         *     ...
         *     第2行第1列,
         *     第2行第2列,
         *     第2行第3列,
         *     ...
         */
        @Override
        public void startElement(String uri, String localName, String name, Attributes attributes) {
            // c => cell 代表单元格
            if (name.equals("c")) {
                // 获取单元格的位置, 如: A1 B1
                System.out.print(attributes.getValue("r") + " - ");
                // 获取单元格类型
                String cellType = attributes.getValue("t");

                // 字符串类型
                if (cellType != null && cellType.equals("s")) {
                    // 标识为true 交给后续endElement处理
                    isString = true;
                } else {
                    isString = false;
                }
                // 内联字符串类型
                if (cellType != null && cellType.equals("inlineStr")) {
                    // 标识为true 交给后续endElement处理
                    isInlineStr = true;
                } else {
                    isInlineStr = false;
                }
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
         * 根据startElement()的单元格数字类型和characters()的索引值或内容值，最终得出单元格的内容值
         */
        @Override
        public void endElement(String uri, String localName, String name) {
            if (isString) {
                // valueOrIndex是索引，直接取出对应的值
                int idx = Integer.parseInt(valueOrIndex);
                valueOrIndex = stringPool.getItemAt(idx).toString();
                isString = false;
            }

            // v => 单元格内容
            if (name.equals("v")) {
                System.out.println(valueOrIndex);
            }
            // is => 内联字符串内容
            if (isInlineStr && name.equals("is")) {
                isInlineStr = false;
                System.out.println(valueOrIndex);
            }
        }
    }

    public static void main(String[] args) {
        String fileName = "demo.xlsx";

        try (OPCPackage pkg = OPCPackage.open(fileName)) {
            XSSFReader r = new XSSFReader(pkg);
            // 获取excel的字符串池
            SharedStringsTable sst = r.getSharedStringsTable();
            // 用于解析xml
            SAXParserFactory parserFactory = SAXParserFactory.newInstance();
            SAXParser parser = parserFactory.newSAXParser();
            XMLReader reader = parser.getXMLReader();
            // 注册自定义的sheet处理类
            ContentHandler handler = new SheetHandler(sst);
            reader.setContentHandler(handler);

            // 遍历读取所有sheet
            Iterator<InputStream> sheets = r.getSheetsData();
            while (sheets.hasNext()) {
                try (InputStream sheet = sheets.next()) {
                    InputSource sheetSource = new InputSource(sheet);
                    reader.parse(sheetSource);
                }
            }
        } catch (IOException | OpenXML4JException | ParserConfigurationException | SAXException ignored) {
        }
    }
}
```
