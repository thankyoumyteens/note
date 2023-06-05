```html
<el-table
    :data="tableData"
    style="width: 100%">
    <el-table-column prop="totalNum" label="总数"></el-table-column>
    <el-table-column prop="aNum" label="a数量"></el-table-column>
    <el-table-column prop="bNum" label="b数量"></el-table-column>
</el-table>
```

要求: 数量不是0的列字体为绿色，并可以点击

```html
<template>
    <el-table
        :data="tableData"
        style="width: 100%"
        :cell-class-name="cellClassName">
        <el-table-column prop="totalNum" label="总数"></el-table-column>
        <el-table-column prop="aNum" label="a数量"></el-table-column>
        <el-table-column prop="bNum" label="b数量"></el-table-column>
    </el-table>
</template>

<script>
    export default {
        data() {
            return {
                cellClassName: (row, column, rowIndex, columnIndex) => {
                    // 当前列
                    let col = row[column["property"]];
                    // 是数字
                    if (!isNaN(col)) {
                        // 非0可点击
                        if (col !== 0) {
                            return "clickable";
                        } else {
                            return "plaintext";
                        }
                    }
                },
            }
        }
    }
</script>

<style lang="scss" scoped>
    /deep/ .plaintext span {
        cursor: inherit;
        color: black;
    }
    /deep/ .clickable span {
        cursor: pointer;
        color: green;
    }
</style>
```
