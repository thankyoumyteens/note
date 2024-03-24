# SuppressWarnings

@SuppressWarning 是一个注解, 它的作用是关闭编译时的警告, 可以用于标记整个类、某个方法、某个属性或者某个参数, 用于告诉编译器这个代码是安全的, 不必警告。

参数:

- all : 关闭所有警告
- boxing : 关闭装箱、拆箱相关的警告
- cast : 关闭强转相关的警告
- dep-ann : 关闭过时注解相关的警告
- fallthrough : 关闭没有 break 的 switch 语句的警告
- finally : 关闭 finally 块没有 return 的警告
- hiding : 关闭关于隐藏的本地变量的警告
- incomplete-switch : 关闭 switch 语句中 case 不完整的警告(当 case 是枚举时)
- nls : 关闭创建无法翻译的字符串的警告 (nls : National Language Support)
- null : 关闭关于可能为空的警告
- rawtypes : 关闭使用泛型作为类参数时没有指明参数类型的警告
- restriction : 关闭使用不建议或者禁止的引用的警告
- serial : 关闭一个可序列化类中没有 serialVersionUID 的警告
- static-access : 关闭一个不正确的静态访问相关的警告
- synthetic-access : 关闭未优化的内部类访问相关的警告
- unchecked : 关闭未经检查的操作(比如强转)的警告
- unqualified-field-access : 关闭不合格的属性访问的警告
- unused : 关闭未使用代码相关的警告
- FieldCanBeLocal : 关闭全局变量只使用一次, 可以被当做局部变量的警告
