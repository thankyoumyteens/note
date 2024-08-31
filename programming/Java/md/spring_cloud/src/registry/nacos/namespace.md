# 命名空间

namespace 用来来实现环境隔离功能。

- Nacos 中可以有多个 namespace，默认为 public，每个 namespace 都有唯一的 id
- 不同 namespace 之间相互隔离，不同 namespace 之间的服务互相不可见
- namespace 下可以有分组(group), 分组下有服务(service)。不同的分组之间微服务也不能互相不可见。服务的默认分组都是 DEFAULT_GROUP

可以命名空间菜单页新增 namespace。

## 配置服务的 namespace

```yaml
spring:
  cloud:
    nacos:
      server-addr: http://localhost:8848
      discovery:
        # 配置集群名称
        cluster-name: BJ
        # 命名空间的id
        namespace: 46c7e6e0-5c8e-41dd-bbff-8f44b58d1570
```
