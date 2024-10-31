# 增删改

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
	queryString := "update MY_TABLE_1 set T_NAME = :1 where T_ID = :2"
	r, err := db.Exec(queryString, "new name", 1)
	if err != nil {
		panic(err)
	}
	// 获取受影响的行数
	rowsAffected, err := r.RowsAffected()
	if err != nil {
		panic(err)
	}
	fmt.Println(rowsAffected)
}
```
