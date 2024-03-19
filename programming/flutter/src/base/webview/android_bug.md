# android 网页不展示

## 报错 net::ERR_CLEARTEXT_NOT_PERMITTED

创建 xml 文件: project/android/app/src/main/res/xml/network_security_config.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </base-config>
</network-security-config>
```

修改 manifest 文件: project/android/app/src/main/AndroidManifest.xml

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- 增加networkSecurityConfig -->
    <application
        android:label="untitled"
        android:name="${applicationName}"
        android:networkSecurityConfig="@xml/network_security_config"
        android:icon="@mipmap/ic_launcher">
        <!-- ... -->
    </application>
</manifest>
```
