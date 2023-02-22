# Element-UI 在table组件el-table-column中使用v-if的问题

```html
<el-table-column
  v-if="isHolidayLive"
  prop="regionNamePath"
  label="申请床位"
  width="300"
/>
```

明明数据项有值，但是在页面上没有显示出来

# 分析

vue在渲染元素时，出于效率考虑，会尽量地复用已有的元素而非重新渲染，导致元素间相互影响，不能正常渲染

# 解决

```html
<el-table-column
  v-if="isHolidayLive"
  prop="regionNamePath"
  label="申请床位"
  width="300"
  key="regionNamePath"
/>
```
