# sqfite

Sqflite 是一个同时支持 Android 跟 iOS 平台的数据库。

## 依赖

pubspec.yaml

```yaml
dependencies:
  flutter:
    sdk: flutter
  sqflite: ^2.3.2
```

## 创建数据库

```dart
// 数据库存在就直接打开
//  不存在就创建
Database database = await openDatabase("demo.db");
```

## 删除数据库

```dart
await deleteDatabase("demo.db");
```

## 建表

```dart
Database database = await openDatabase(
  "demo.db",
  version: 1,
  onCreate: (Database db, int version) async {
    // 执行建表语句
    await db.execute(sql);
  },
);
```

## insert

```dart
void insertDemo(String val1, String val2) async {
  Database database = await openDatabase("demo.db");
  await database.rawInsert(
      'insert into my_talbe (col1, col2) values (?, ?)', [val1, val2]);
}
```

## update

```dart
void updateDemo(String val1, String val2) async {
  Database database = await openDatabase("demo.db");
  await database.rawInsert(
      'update my_talbe set col1 = ? where col2 = ?', [val1, val2]);
}
```

## delete

```dart
void deleteDemo(String val1) async {
  Database database = await openDatabase("demo.db");
  await database.rawDelete(
      'delete from my_talbe where col1 = ?', [val1]);
}
```

## select

```dart
Future<List<Map>> getList(String val1) async {
  Database database = await openDatabase("demo.db");
  List<Map> list = await database
      .rawQuery('select * from my_talbe where col1 = ?', [val1]);
  return list;
}
```
