# 底部导航栏

### 1. pages 右键 -> 新建页面 -> 勾选 "在 pages.json 中注册"(可以直接在下方修改 navigationBarTitleText 的值)

### 2. pages.json

```json
{
  // 新建页面时自动添加
  "pages": [
    //pages数组中第一项表示应用启动页
    {
      "path": "pages/index/index",
      "style": {
        // 导航栏标题文字内容
        "navigationBarTitleText": "首页"
      }
    },
    {
      "path": "pages/my/my",
      "style": {
        "navigationBarTitleText": "我的"
      }
    }
  ],
  // 全局窗口样式
  "globalStyle": {
    // 导航栏标题颜色，仅支持 black/white
    "navigationBarTextStyle": "white",
    "navigationBarTitleText": "uni-app",
    // 顶部导航栏颜色
    "navigationBarBackgroundColor": "#27BA98",
    "backgroundColor": "#F8F8F8"
  },
  // 底部导航栏
  "tabBar": {
    // 未选中时文字的颜色
    "color": "#7A7E83",
    // 选中时文字的颜色
    "selectedColor": "#3cc51f",
    // list中至少两项
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        // 未选中时图标
        "iconPath": "/static/logo.png",
        // 选中时的图标
        "selectedIconPath": "/static/logo.png"
      },
      {
        "pagePath": "pages/my/my",
        "text": "我的"
      }
    ]
  },
  "uniIdRouter": {}
}
```
