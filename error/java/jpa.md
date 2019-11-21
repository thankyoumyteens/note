# java.sql.SQLSyntaxErrorException: Table 'sell.hibernate_sequence' doesn't exist

id为自增属性，直接添加@GeneratedValue报了如下错误
```
    @Id
    @GeneratedValue
    private Integer Id;
```

解决方法 ：
在 @GeneratedValue后加上strategy = GenerationType.IDENTITY
```
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer Id;
```
