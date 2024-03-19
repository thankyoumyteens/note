# ios 网页不展示

修改项目的 ios/Runner/Info.plist 文件:

```xml
<!-- ... -->
<plist version="1.0">
<dict>
    <!-- ... -->
    <!-- 添加下面的内容 -->
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
        <key>NSAllowsArbitraryLoadsInWebContent</key>
        <true/>
    </dict>
</dict>
</plist>
```
