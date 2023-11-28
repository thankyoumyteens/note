# .vue文件中的style的scoped属性

在vue组件中, 为了使样式私有化, 不对全局造成污染, 在style标签上添加scoped属性, 以表示它只属于当下的模块。

创建公共组件button
```html
<button class="button">text</button>
<style scoped>
  .button{
    padding: 5px 10px;
    font-size: 12px;
    border-radus: 2px;
  }
</style>
```
浏览器渲染后的button组件
```html
<button data-v-2311c06a class="button">text</button>
<style>
.button[data-v-2311c06a]{
  padding: 5px 10px;
  font-size: 12px;
  border-radus: 2px;
}
</style>
```

可以看出, 添加了scoped属性的组件, 做了如下操作: 

1. 给HTML的DOM节点增加一个不重复的data属性(data-v-2311c06a)
2. 在编译后生成的css语句的末尾加一个当前组件的data属性选择器(data-v-2311c06a)来私有化样式

# 问题

在需要改子组件的样式, 但是又不影响其他页面使用这个子组件的样式的时候, scoped会导致修改不生效

在父组件内使用scoped时, 想要改变子组件的样式, 会不生效

```html
<style scoped>
    .father-div .child-div {
        color:red;
    }
</style>
```
会解析成
```html
<!-- 父组件的hash值: b45036b2 -->
<!-- 子组件的hash值: 384b136e -->
<style>
    .father-div .child-div[data-v-b45036b2] {
        color:red;
    }
</style>
```

原因是: 父组件内css选择器后添加的是父组件的hash值, 而子组件的html标签上的是子组件的hash值, 对应不上当然没效果

# 解决: 使用深度作用选择器

深度作用选择器有>>>和别名/deep/, >>>基本在纯css中使用, Sass, less一般都用/deep/或::v-deep


```html
<style scoped>
    .father-div /deep/ .child-div {
        color:red;
    }
</style>
```
当遇到deep的时候会将deep替换成当前组件的hash值, 并且不会再为后面的选择器增加hash值

```html
<!-- 父组件的hash值: b45036b2 -->
<!-- 子组件的hash值: 384b136e -->
<style>
    .father-div[data-v-b45036b2] .child-div {
        color:red;
    }
</style>
```
