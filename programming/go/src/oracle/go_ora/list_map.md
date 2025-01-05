# 查询结果转成 map

```go
package main

import (
	"database/sql"
	"fmt"
	goOra "github.com/sijms/go-ora/v2"
)

func main() {
	urlOptions := map[string]string{
		"SID": "orcl",
	}
	dsn := goOra.BuildUrl("127.0.0.1", 11521, "", "DEMO", "123456", urlOptions)

	// 打开一个新的数据库连接
	db, err := sql.Open("oracle", dsn)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	// 实际进行连接
	err = db.Ping()
	if err != nil {
		panic(err)
	}
	fmt.Println("连接成功")

	// 执行SQL语句
	query := "select * from MY_TABLE_1"
	rows, err := db.Query(query)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	// 获取所有列名
	columns, err := rows.Columns()
	if err != nil {
		panic(err)
	}
	columnLength := len(columns)

	// 创建一个buffer, 用于存储每一行的数据
	buffer := make([]interface{}, columnLength)
	for index, _ := range buffer {
		var a interface{}
		buffer[index] = &a
	}

	var resultList []map[string]interface{}
	for rows.Next() {
		// 将每一行的数据读取到buffer中
		if err := rows.Scan(buffer...); err != nil {
			panic(err)
		}

		// 将buffer中的数据存入到rowData中
		rowData := make(map[string]interface{})
		for i, data := range buffer {
			p := data.(*interface{})
			rowData[columns[i]] = *p
		}
		resultList = append(resultList, rowData)
	}

	// 检查行遍历时发生的错误
	if err := rows.Err(); err != nil {
		panic(err)
	}

	fmt.Println(resultList)
}
```
