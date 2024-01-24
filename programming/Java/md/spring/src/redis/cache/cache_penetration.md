# 缓存穿透

查询数据时, 会先从缓存中查询, 如果缓存中没有, 才取数据库中查询。

查询一个不存在的数据, 数据库中没有数据也不会写入缓存, 导致每次请求都会查询数据库。如果有大量这种请求, 就会导致王俊凯崩溃。

## 解决方案

1. 缓存空结果: 如果查询的数据不存在, 就把这个空结果也缓存下来
   - 优点: 实现简单
   - 缺点:
     1. 内存消耗过大
     2. 数据不一致: 如果后来这个请求有数据了, 就会导致缓存和数据库中的数据不一致
2. 布隆过滤器: 请求先经过布隆过滤器, 再到达缓存, 如果查询的数据不存在布隆过滤器会直接返回
   - 优点:
     1. 内存占用少
     2. 查询效率高：布隆过滤器可以在非常快的时间内判断一个元素是否存在于集合中, 而不需要像传统数据结构那样进行线性扫描
   - 缺点:
     1. 实现复杂
     2. 存在误判: 布隆过滤器中的存储的 key 越多, 误判率越高
     3. 需要预热: 使用前要先将数据库中所有需要缓存的数据加载到布隆过滤器中, 如果数据库中的数据会变动, 还需要定期维护布隆过滤器
     4. 不能删除布隆过滤器中已存在的 key

## 布隆过滤器

布隆过滤器(Bloom Filter) 是由 Howard Bloom 在 1970 年提出的。它用来检测一个元素在不在集合中。

布隆过滤器会维护一个位图(byte 数组), 当一个元素被加入集合时, 通过 k 个哈希函数将这个元素映射成位图中的 k 个位置,把它们置为 1。查询时, 同样需要调用这 k 个哈希函数算出这个元素对应位图中的 k 个位置, 如果这 k 个位置的值都为 1, 则该元素在集合中, 只要有一个为 0, 则该元素不在集合中。由于位图初始全为 0, 所以使用布隆过滤器前需要先将集合中的所有元素都添加到布隆过滤器中, 以初始化位图。

比如下图, 集合中有三个元素: 100, 101, 102, 经过 3 个 hash 函数后分别落在黄色位置。元素 10 经过 3 个 hash 函数后落在蓝色位置, 所以 10 不在集合中:

![](../../img/BloomFilter.png)

布隆过滤器存在误判问题, 比如下图, 元素 aabc, 10 经过 3 个 hash 函数后同样落在黄色位置, 但它并不在集合中:

![](../../img/BloomFilter2.png)

如果集合的长度为 n, 期望的误差为 p, 则可以根据下面的公式求出位图的长度 m 和 hash 函数的数量 k:

![](../../img/BloomFilter3.png)

## Guava 实现的布隆过滤器

依赖

```xml
<!-- https://mvnrepository.com/artifact/com.google.guava/guava -->
<dependency>
  <groupId>com.google.guava</groupId>
  <artifactId>guava</artifactId>
  <version>33.0.0-jre</version>
</dependency>
```

使用布隆过滤器

```java
// 集合
List<Integer> collection = new ArrayList<>();
collection.add(1);
collection.add(2);
collection.add(3);

// 创建布隆过滤器, 集合的长度: collection.size(), 期望的误差: 0.001
BloomFilter<Integer> bloomFilter = BloomFilter.create(Funnels.integerFunnel(),
        collection.size(), 0.001);

// 布隆过滤器预热
for (Integer item : collection) {
    bloomFilter.put(item);
}

// 判断数据是否在集合中
System.out.println(bloomFilter.mightContain(1));
System.out.println(bloomFilter.mightContain(10));
```

## Redisson 实现的布隆过滤器

依赖

```xml
<!-- https://mvnrepository.com/artifact/org.redisson/redisson -->
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson</artifactId>
    <version>3.26.0</version>
</dependency>
```

使用布隆过滤器

```java
// 集合
List<Integer> collection = new ArrayList<>();
collection.add(1);
collection.add(2);
collection.add(3);

Config config = new Config();
config.useSingleServer().setAddress("redis://localhost:6379");
RedissonClient redissonClient = Redisson.create(config);

// 创建布隆过滤器, 集合的长度: collection.size(), 期望的误差: 0.001
RBloomFilter<Integer> bloomFilter = redissonClient.getBloomFilter("intBloomFilter");
bloomFilter.tryInit(collection.size(), 0.001);

// 布隆过滤器预热
for (Integer item : collection) {
    bloomFilter.add(item);
}

// 判断数据是否在集合中
System.out.println(bloomFilter.contains(1));
System.out.println(bloomFilter.contains(10));
```
