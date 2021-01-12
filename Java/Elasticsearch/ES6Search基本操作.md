# 数据准备

数据格式
```json
{
    "account_number": 0,
    "balance": 16623,
    "firstname": "Bradshaw",
    "lastname": "Mckenzie",
    "age": 29,
    "gender": "F",
    "address": "244 Columbus Place",
    "employer": "Euron",
    "email": "bradshawmckenzie@euron.com",
    "city": "Hobucken",
    "state": "CO"
}
```

导入本地数据
```
curl -H "Content-Type: application/json" -X POST "localhost:9200/bank/_doc/_bulk?pretty&refresh" --data-binary "@./accounts.json"
```
