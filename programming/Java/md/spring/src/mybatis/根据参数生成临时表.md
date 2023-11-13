# 根据参数生成临时表

```xml
select t1.NAME, t1.VALUE from (
<foreach collection="codeList" item="code" separator="union">
    select
        #{code.val,jdbcType=VARCHAR} as VALUE,
        #{code.name,jdbcType=VARCHAR} as NAME
    from dual
</foreach>
) t1
```
