# org.apache.poi.util.RecordFormatException: Tried to allocate an array of length 4276190, but 1000000 is the maximum for this record type

```java
// 原来的写法
try (XSSFWorkbook wb = new XSSFWorkbook(file.getInputStream())) {
    XSSFSheet sheet = wb.getSheetAt(0);
    int rowCount = sheet.getLastRowNum() + 1;
    for (int i = 1; i < rowCount; i++) {
        XSSFRow row = sheet.getRow(i);
        String val0 = getCellData(row, 0);
        String val1 = getCellData(row, 1);
        String val2 = getCellData(row, 2);
        if (StrUtil.isNotBlank(val2) && val2.length() > 100) {
            throw new Exception("输出过长, 第" + (i + 1) + "行");
        }
        if (StringUtils.isBlank(val0)
                && StringUtils.isBlank(val1)
                && StringUtils.isBlank(val2)
        ) {
            // 空行
            continue;
        }
        ResultDTO.ResultDTOBuilder builder = ResultDTO.builder()
                .val0(val0).remark(val1);
        if (StringUtils.isBlank(val0)
                || (StringUtils.isBlank(val1)
                && StringUtils.isBlank(val2))
        ) {
            ResultDTO build = builder.build();
            log.error("缺少必填项" + build);
            errorDataList.add(build);
            continue;
        }
        // ...
        dataList.add(builder.build());
    }
    // 入库
    for (ResultDTO ResultDTO : dataList) {
        // ...
    }
} catch (IOException e) {
    throw new RuntimeException("");
}
```

## 原因

POI有一些缺陷, 操作都是在内存中完成的, 内存消耗很大。poi在处理之前使用IOUtils里面的方法校验了下数据的字节长度, 当超过常量配置的长度后会抛出上面的异常, 如果不做限制就会导致内存不足。

## 解决

使用EasyExcel

```java
// 新写法
EasyExcel.read(
    file.getInputStream(),
    ResultDTO.class,
    new ReadListener<ResultDTO>() {
        @Override
        public void invoke(ResultDTO o, AnalysisContext analysisContext) {
            String val0 = o.getVal0();
            String val1 = o.getVal1();
            String val2 = o.getVal2();
            if (StrUtil.isNotBlank(val2) && val2.length() > 200) {
                errorMsg[0] = "输出过长, 第" + analysisContext.getCurrentRowNum() + "行";
            }
            if (StringUtils.isBlank(val0)
                    && StringUtils.isBlank(val1)
                    && StringUtils.isBlank(val2)
            ) {
                // 空行
                return;
            }
            ResultDTO.ResultDTOBuilder builder = ResultDTO.builder()
                    .val0(val0).remark(val1);
            if (StringUtils.isBlank(val0)
                    || (StringUtils.isBlank(val1)
                    && StringUtils.isBlank(val2))
            ) {
                ResultDTO build = builder.build();
                log.error("缺少必填项" + build);
                errorDataList.add(build);
                return;
            }
            // ...
            dataList.add(builder.build());
        }

        @Override
        public void doAfterAllAnalysed(AnalysisContext analysisContext) {

        }
    }
).sheet().doRead();

if (StringUtils.isNotBlank(errorMsg[0])) {
    throw new Exception(errorMsg[0]);
}
// 入库
for (ResultDTO ResultDTO : dataList) {
    // ...
}
```
