# 设置某些单元格不可编辑

```java
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.streaming.SXSSFWorkbook;

import java.io.FileOutputStream;
import java.io.IOException;

public class DemoMain {

    /**
     * 锁定整个sheet, 把可编辑的单元格解锁
     */
    public static void main(String[] args) {
        String fileName = "export.xlsx";
        // 使用SXSSFWorkbook避免内存溢出
        try (SXSSFWorkbook wb = new SXSSFWorkbook(); FileOutputStream os = new FileOutputStream(fileName)) {
            Sheet sheet = wb.createSheet("sheet1");

            // 不可编辑的单元格
            CellStyle lock = wb.createCellStyle();
            lock.setLocked(true);

            // 可编辑的单元格
            CellStyle unlock = wb.createCellStyle();
            unlock.setLocked(false);

            // 写入数据
            for (int r = 0; r < 10; r++) {
                Row row = sheet.createRow(r);
                for (int c = 0; c < 10; c++) {
                    Cell cell = row.createCell(c);
                    // 第2列上锁
                    if (c == 1) {
                        cell.setCellStyle(lock);
                        cell.setCellValue("不可编辑");
                    } else {
                        cell.setCellStyle(unlock);
                        cell.setCellValue("可以编辑");
                    }
                }
            }
            // sheet添加保护，这个一定要否则光锁定还是可以编辑的
            sheet.protectSheet("password");
            wb.write(os);
        } catch (IOException ignored) {
        }
    }
}
```
