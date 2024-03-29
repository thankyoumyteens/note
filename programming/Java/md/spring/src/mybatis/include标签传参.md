# include 标签传参

mybatis 的 include 标签主要是用于 sql 语句的可重用，并且可以接收参数来生成动态 sql。

```xml
<sql id="demo">
    <if test="strParam != null">
        #{strParam}
    </if>
    <if test="demoParam != null">
        #{demoParam}
    </if>
    <if test="demoParam == null">
        'none'
    </if>
</sql>

<select id="test2" resultType="java.lang.String">
    select
    <include refid="demo"/>
    ,
    <include refid="demo">
        <property name="strParam" value="123"/>
    </include>
    from dual
</select>
```

```java
List<Object> queryDemo(@Param("demoParam") String demoParam);
```
