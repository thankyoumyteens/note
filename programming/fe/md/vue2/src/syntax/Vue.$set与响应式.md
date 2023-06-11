# Object类型响应式

当把一个object对象放到Vue的data里面时，Vue会使用Object.defineproperty将该对象的所有属性都设置上getter和setter。

使用Object.defineproperty能监听对象上的某个属性的修改与获取，但是无法监听到对象属性的增和删。所以Vue无法监听到data的某个属性增加与删除。

```js
export default {
    data() {
        return {
            user: {
                name: ''
            }
        }
    },
    methods: {
        changeUser() {
            // 响应式的
            this.user.name = '张';
            // 非响应式的
            this.user.age = 10;
            // 响应式的
            this.$set(this.user, 'age', 10);
            //使用Object.assign实现响应式修改
            this.user = Object.assign({}, this.user, {
                name: '张', // 覆盖user中的name
                age: 10 // 新字段
            })
        }
    }
}
```

在ES6中提供了Proxy可以实现元编程，Vue3也使用Proxy来重写了响应式系统，在Vue3中可以监听到data的某个属性增加与删除。

# Array类型响应式

Vue不能检测数组的以下变动

- 使用索引直接设置一个数组项，如this.arr\[0] = 10
- 修改数组的长度，如this.arr.length = 100

```js
export default {
    data() {
        return {
            items: [1, 2, 3]
        }
    },
    methods: {
        changeItems() {
            // 非响应式的
            this.items[0] = 10;
            // 非响应式的
            this.items.length = 2;
            // 响应式的
            this.items.splice(0, 1, 10);
            // 响应式的
            this.$set(this.items, 0, 10);
        }
    }
}
```
