# 使用结构体

1. 创建结构体

```go
package demo

type DemoParam struct {
	Name string
}
type DemoResult struct {
	Message string
}

type DemoCommunicate struct {
}

func NewDemoCommunicate() *DemoCommunicate {
	return &DemoCommunicate{}
}

// 必须要大写才能在js中调用
// 参数和返回值都使用结构体
func (d *DemoCommunicate) SayHello(param DemoParam) DemoResult {
	return DemoResult{Message: "Hello " + param.Name}
}
```

2. 在 main.go 中绑定

```go
package main

import (
	"embed"
	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
    // 导入
	"myproject/demo"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	app := NewApp()
	err := wails.Run(&options.App{
		Title:  "myproject",
		Width:  1024,
		Height: 768,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		BackgroundColour: &options.RGBA{R: 27, G: 38, B: 54, A: 1},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
            // 在这里绑定
			demo.NewDemoCommunicate(),
		},
	})

}
```

3. 运行 `wails dev`, 会自动在 `wailsjs/go` 目录中创建 `demo/DemoCommunicate.d.ts` 和 `demo/DemoCommunicate.js` 两个文件, 结构体 DemoCommunicate 中的所有公开方法都会自动添加。同时也会在 `wailsjs/go` 目录中自动创建 `models.ts` 文件, 其中会定义 go 中的结构体

4. 在 vue 中使用

```js
// 导入参数和返回值的对象声明
import { demo } from "../../wailsjs/go/models.ts";

function greet() {
  // 参数使用结构体
  let p = new demo.DemoParam();
  p.Name = data.name;
  SayHello(p).then((result) => {
    // 返回值也是结构体
    data.resultText = result.Message;
  });
}
```
