# 查

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

	var (
        id int64
        name sql.NullString
    )
    for rows.Next() {
        err = rows.Scan(&id, &name)
        if err != nil {
            panic(err)
        }
	    fmt.Println(id, name)
    }
}
```
