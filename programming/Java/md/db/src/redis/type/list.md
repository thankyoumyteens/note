# list

```sh
# 从列表右端插入值(可以是多个)
rpush students "Tom" "Jerry"

# 从列表左端插入值(可以是多个)
lpush students "Tom" "Jerry"

# 在Jerry左边插入John
linsert students before "Jerry" "John"

# 在Jerry右边插入John
linsert students after "Jerry" "John"

# 从列表左端弹出一个元素
lpop students

# 从列表右端弹出一个元素
rpop students

# 删除所有的Tom
lrem students 0 "Tom"

# 从左到右, 删除3个Tom
lrem students 3 "Tom"

# 从右到左, 删除3个Tom
lrem students -3 "Tom"

# 相当于 students = students.subList(1, 3)
ltrim students 1 2
```

## 查询

```sh
# 获取从左到右索引范围是[1, 2]的所有元素
lrange students 1 2

# 获取索引是1的元素
lindex students 1

# 获取列表的长度
llen students
```

## 修改

```sh
# 把索引是1的元素值改为Tom
lset students 1 "Tom"
```
