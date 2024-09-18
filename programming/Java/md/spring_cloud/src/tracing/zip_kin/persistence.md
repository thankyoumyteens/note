# 持久化

zipkin 支持的存储方式：

- 内存：服务重启将会失效，不推荐。默认
- MySQL：数据量越大性能越低
- Elasticsearch：主流的解决方案
- Cassandra：官方推荐

## 使用 MySQL 持久化
