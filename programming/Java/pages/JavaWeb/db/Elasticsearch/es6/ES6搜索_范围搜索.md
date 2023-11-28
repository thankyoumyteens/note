# 范围查询

范围查询关键字```range```, 它包括大于```gt```、大于等于```gte```、小于```lt```、小于等于```lte```。

## 查询age>25的学生。

```json
POST http://localhost:9200/user/student/_search?pretty
{
  "query":{
    "range":{
      "age":{
        "gt":25
      }
    }
  }
}
```

## 查询age >= 21 且 age < 26且name="kevin"的学生

```json
POST http://localhost:9200/user/search/_search?pretty
{
  "query":{
    "bool":{
      "must":[{
        "term":{
          "name":"kevin"
        }
      },{
        "range":{
          "age":{
            "gte":21,
            "lt":25
          }
        }
      }]
    }
  }
}
```
