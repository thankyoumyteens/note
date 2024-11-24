# 设置单元格样式

```java
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.ss.util.RegionUtil;
import org.apache.poi.xssf.streaming.SXSSFWorkbook;

import java.io.FileOutputStream;

public class Demo {
    public static void main(String[] args) throws Exception {
        String fileName = "demo.xlsx";

        // 使用 SXSSFWorkbook 替代 XSSFWorkbook
        try (SXSSFWorkbook wb = new SXSSFWorkbook(); FileOutputStream os = new FileOutputStream(fileName)) {
            Sheet sheet = wb.createSheet("sheet1");
            Row row = sheet.createRow(2);
            Cell cell = row.createCell(1);
            cell.setCellValue("B3");

            CellStyle cellStyle = wb.createCellStyle();
            // 设置单元格颜色
            cellStyle.setFillForegroundColor(IndexedColors.YELLOW.getIndex());
            cellStyle.setFillPattern(FillPatternType.SOLID_FOREGROUND);
            // 设置单元格边框
            cellStyle.setBorderTop(BorderStyle.THIN);
            cellStyle.setBorderBottom(BorderStyle.THIN);
            cellStyle.setBorderLeft(BorderStyle.THIN);
            cellStyle.setBorderRight(BorderStyle.THIN);
            // 设置单元格对齐方式
            cellStyle.setAlignment(HorizontalAlignment.CENTER);
            cellStyle.setVerticalAlignment(VerticalAlignment.CENTER);
            // 设置字体
            Font font = wb.createFont();
            font.setFontName("宋体");
            font.setFontHeightInPoints((short) 12);
            font.setColor(IndexedColors.RED.getIndex());
            cellStyle.setFont(font);
            cell.setCellStyle(cellStyle);

            wb.write(os);
        }
    }
}
```
