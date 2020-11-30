# 自定义 Template

打开 File -> Settings -> Editor -> Live Templates

新增自定义模板，首先需要填写快捷键（即 Abbreviation），描述是可选的，然后定义模板的上下文，点击define选择Java，这样在编辑 Java 的时候就会触发当前模板。

比如在Abbreviation填`sout`, Template text填`System.out.println($END$)`。点击ok就可以在java代码中输入sout生成代码了。

# Live Templates实现方法注释

打开 File -> Settings -> Editor -> Live Templates

新建一个group，命名为“self”，表明这个组里面的模板是自定义的，可能仅适用于自己的工作场景。

在组里新建一个模板，快捷键定义为*，确认方式选择Enter，即在应用模板的地方，输入`/*+回车`，即可生成模板内容。

Template text 模板定义如下:
```
*
* @MethodName: $methodName$
* @Description: $END$
$params$
* @return $return$
* @throws ServiceException
* @author xxx
* @email xxx@123.cn
* @date $date$ $time$
*/
```

\$param\$表示一个自定义的变量，用于枚举方法中的参数，即@param的内容。但是这里有个问题，就是如何循环生成方法的多个参数并且换行显示呢？虽然Live Templates中提供了一个功能函数-methodParameters()，但这个函数可以理解为只是“一串”参数，怎么拆分显示呢？这里用到了Groovy脚本语言，将\$param\$这个变量对应的表达式写为执行Groovy脚本，即拆分methodParameters()返回的“一串”参数，并在每个参数前面添加@param并换行。

点击Edit variables编辑变量, 添加脚本:

param的Groovy脚本:
```Groovy
groovyScript("def result=''; def params=\"${_1}\".replaceAll('[\\\\[|\\\\]|\\\\s]', '').split(',').toList(); for(i = 0; i < params.size(); i++) {result+='* @param ' + params[i] + ((i < params.size() - 1) ? '\\n' : '')}; return result", methodParameters())
```

\$return\$同理, 将methodReturnType()返回的全类名改成简写类名:

return的Groovy脚本:
```Groovy
groovyScript("def result=''; def params=\"${_1}\"; result=params.substring(params.lastIndexOf('.')+1); return result", methodReturnType())
```

\$date\$也是一个自定义变量，对应的表达式使用内置的date()函数，表示输出当前的日期。
\$END\$是内置的一个变量，表示模板内容生成后，光标停留的位置。生成方法注释后，可能需要填写方法的描述内容，自定义光标停留的位置可以方便后续操作。
生成的自定义模板内容后，光标默认会依次停留在自定义变量的位置，需要用户手动回车确定，直至无自定义变量为止。这个默认行为有时可能是不需要的，所以编辑自定义变量时，选中“skip if defined”即可。

# Live Templates实现Logger定义语句生成

Template text
```
private static final Logger logger = LoggerFactory.getLogger($CLASS_NAME$.class);
```

Edit variables:
```
$CLASS_NAME$ -> className()
```
