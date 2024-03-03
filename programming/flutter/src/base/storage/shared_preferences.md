# shared_preferences

## 依赖

pubspec.yaml

```yaml
dependencies:
  flutter:
    sdk: flutter
  shared_preferences: ^2.2.2
```

## 存

```dart
void saveString(key, value) async {
  SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
  sharedPreferences.setString(key, value);
}
```

## 取

```dart
Future<String> getString(key) async {
  String val = "";
  SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
  if (sharedPreferences.getString(key) != null) {
    val = sharedPreferences.getString(key)!;
  }
  return val;
}
```
