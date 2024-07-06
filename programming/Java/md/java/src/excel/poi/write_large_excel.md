# 超大 excel 写入

使用 SXSSFWorkbook 替代 XSSFWorkbook 即可。

```java
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.streaming.SXSSFWorkbook;

import java.io.FileOutputStream;
import java.io.IOException;

public class ExcelWriter {

    public static void main(String[] args) {
        String fileName = "demo.xlsx";

        // 使用 SXSSFWorkbook 替代 XSSFWorkbook
        try (SXSSFWorkbook wb = new SXSSFWorkbook(); FileOutputStream os = new FileOutputStream(fileName)) {
            Sheet sheet = wb.createSheet("sheet1");
            // 每个sheet最大支持1048576行
            for (int r = 0; r < 1048576; r++) {
                Row row = sheet.createRow(r);
                Cell cell = row.createCell(0);
                cell.setCellValue("第" + (r + 1) + "行");
            }
            wb.write(os);
        } catch (IOException ignored) {
        }
    }
}
```
