# 通用命令

- `keys *` 列出所有 key
- `keys he*` 列出所有以 he 开头的 key
- `dbsize` key 的总数
- `exists 键` key 是否存在, 存在返回 1, 否则返回 0
- `del 键` 删除指定的 key, 删除成功返回 1, key 不存在返回 0
- `expire 键 秒` 设置 key 在指定秒数后过期
- `ttl 键` 查看 key 还有多久过期
- `persist 键` 去掉 key 的过期时间
- `type 键` 返回 key 的数据类型
