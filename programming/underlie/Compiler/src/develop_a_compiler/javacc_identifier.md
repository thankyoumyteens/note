# 扫描标识符和关键字

```java
// 关键字
TOKEN: {
    <VOID       : "void">
    | <CHAR     : "char">
    | <SHORT    : "short">
    | <INT      : "int">
    | <LONG     : "long">
    | <STRUCT   : "struct">
    | <UNION    : "union">
    | <ENUM     : "enum">
    | <STATIC   : "static">
    | <EXTERN   : "extern">
    | <CONST    : "const">
    | <SIGNED   : "signed">
    | <UNSIGNED : "unsigned">
    | <IF       : "if">
    | <ELSE     : "else">
    | <SWITCH   : "switch">
    | <CASE     : "case">
    | <DEFAULT_ : "default">
    | <WHILE    : "while">
    | <DO       : "do">
    | <FOR      : "for">
    | <RETURN   : "return">
    | <BREAK    : "break">
    | <CONTINUE : "continue">
    | <GOTO     : "goto">
    | <TYPEDEF  : "typedef">
    | <IMPORT   : "import">
    | <SIZEOF   : "sizeof">
}

// 标识符
// 以大/小写字母或下划线开头, 后接字母/数字或下划线
TOKEN: {
    <IDENTIFIER: ["a"-"z", "A"-"Z", "_"] (["a"-"z", "A"-"Z", "_", "0"-"9"])*>
}
```

关键字需要定义在标识符前面, 这样扫描到`void func() {}`这种代码时, 会把 void 当作关键字。
