# el-table-column 中使用 v-if 导致不能正常渲染

## 错误代码

```html
<el-table :data="tableData" style="width: 100%">
  <el-table-column v-if="isShow" prop="date" label="日期" />
  <el-table-column v-if="isShow" prop="name" label="姓名" />
  <el-table-column v-if="isShow" prop="address" label="地址" />
</el-table>
```

明明数据项有值, 但是在页面上没有显示出来

## 原因

vue 在渲染元素时, 出于效率考虑, 会尽量地复用已有的元素而非重新渲染, 导致元素间相互影响, 不能正常渲染。总而言之就是 v-if 不能多次作用在同一组件上。

## 解决

添加一个具有唯一值的 key attribute，表明该元素是完全独立的，不要复用它。

```html
<el-table-column v-if="isShow" prop="myVal" label="xxx" :key="data['myVal']" />
<el-table :data="tableData" style="width: 100%">
  <el-table-column
    v-if="isShow"
    prop="date"
    label="日期"
    :key="tableData['date']"
  />
  <el-table-column
    v-if="isShow"
    prop="name"
    label="姓名"
    :key="tableData['name']"
  />
  <el-table-column
    v-if="isShow"
    prop="address"
    label="地址"
    :key="tableData['address']"
  />
</el-table>
```
