# @Scheduled

@Scheduled注解是Spring Boot提供的用于定时任务控制的注解, 主要用于控制任务在某个指定时间执行, 或者每隔一段时间执行。需要配合@EnableScheduling使用

```java
@Configuration
@EnableScheduling
public class ScheduledDemo {
    // 每五秒钟执行一次
    @Scheduled(cron = "*/5 * * * * ?")
    public void scheduledDemo() {
        System.out.println("test"+new Date());
    }
}
```

Scheduled在集群环境下部署时会遇到同一时间同时触发定时任务的情况

# ShedLock

ShedLock是个分布式锁, 定时任务执行时先去redis申请分布式锁, 当某一个进程申请成功后, 会执行对应的任务逻辑, 其他进程无法获取定时任务, 不能执行任务, 只能等待下一轮再去竞争

@SchedulerLock注解一共支持五个参数, 分别是

- name: 用来标注一个定时服务的名字, 被用于写入数据库作为区分不同服务的标识, 如果有多个同名定时任务则同一时间点只有一个执行成功
- lockAtMostFor: 成功执行任务的节点所能拥有独占锁的最长时间, 单位是毫秒ms
- lockAtMostForString: 成功执行任务的节点所能拥有的独占锁的最长时间的字符串表达, 例如"PT14M"表示为14分钟, 单位可以是S,M,H
- lockAtLeastFor: 成功执行任务的节点所能拥有独占所的最短时间, 单位是毫秒ms
- lockAtLeastForString: 成功执行任务的节点所能拥有的独占锁的最短时间的字符串表达, 例如"PT14M"表示为14分钟,单位可以是S,M,H

maven
```xml
<dependency>
    <groupId>net.javacrumbs.shedlock</groupId>
    <artifactId>shedlock-spring</artifactId>
    <version>2.3.0</version>
</dependency>
<dependency>
    <groupId>net.javacrumbs.shedlock</groupId>
    <artifactId>shedlock-provider-redis-spring</artifactId>
    <version>2.3.0</version>
</dependency>

<!--spring2.0集成redis所需common-pool2 -->
<!-- jedis依赖此 若项目中已经引入jedis 请忽略此步骤-->
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
</dependency>
```

配置数据源
```java
@Configuration
@EnableScheduling
// defaultLockAtMostFor  默认锁定时间
@EnableSchedulerLock(defaultLockAtMostFor = "PT55S")
public class ShedLockRedisConfig{
    @Bean
    public LockProvider lockProvider(RedisConnectionFactory connectionFactory) {
        return new RedisLockProvider(connectionFactory);
    }
}
```

配合Scheduled
```java
@Scheduled(cron = "0/3 * * * * ? ")
@SchedulerLock(name = "testMisc",lockAtLeastFor = 4*1000, lockAtMostFor = 6*1000)
public void testMisc(){
    log.info ( "定时任务测试" );
    eleOrderlyChargingFeign.runMisc();
}
```
