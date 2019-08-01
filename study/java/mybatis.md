# MyBatis中${ }与\#{ }有什么区别

\#{}是预编译处理，MyBatis在处理#{}时, 它会将sql中的#{}替换为?, 
然后调用PreparedStatement的set方法来赋值

${}是字符串替换, MyBatis在处理${}时, 它会将sql中的${}替换为变量的值

使用${}会导致sql注入

