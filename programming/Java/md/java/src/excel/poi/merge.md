# 合并单元格

```java
package com.example.work;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.xssf.streaming.SXSSFWorkbook;

import java.io.FileOutputStream;

public class Demo {
    public static void main(String[] args) throws Exception {
        String fileName = "demo.xlsx";

        try (SXSSFWorkbook wb = new SXSSFWorkbook(); FileOutputStream os = new FileOutputStream(fileName)) {
            Sheet sheet = wb.createSheet("sheet1");
            Row row = sheet.createRow(2);
            Cell cell0 = row.createCell(1);
            cell0.setCellValue("B3");
            Cell cell1 = row.createCell(2);
            cell1.setCellValue("C3");

            // 合并单元格
            // 起始行, 终止行, 起始列, 终止列
            // 第一行和第二行合并
            // 第一列和第二列合并
            CellRangeAddress cellAddresses = new CellRangeAddress(1, 2, 1, 2);
            sheet.addMergedRegion(cellAddresses);

            // 为合并后的单元格添加边框
            RegionUtil.setBorderTop(BorderStyle.THIN, cellAddresses, sheet);
            RegionUtil.setBorderRight(BorderStyle.THIN, cellAddresses, sheet);
            RegionUtil.setBorderBottom(BorderStyle.THIN, cellAddresses, sheet);
            RegionUtil.setBorderLeft(BorderStyle.THIN, cellAddresses, sheet);

            wb.write(os);
        }
    }
}
```
