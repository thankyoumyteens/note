# LiveTemplates

## 自定义 Template

打开 File -> Settings -> Editor -> Live Templates

新增自定义模板，首先需要填写快捷键（即 Abbreviation），描述是可选的，然后定义模板的上下文，点击define选择Java，这样在编辑 Java 的时候就会触发当前模板。

比如在Abbreviation填`sout`, Template text填`System.out.println($END$)`。点击ok就可以在java代码中输入sout生成代码了。

## Live Templates实现方法注释

打开 File -> Settings -> Editor -> Live Templates

新建一个group，命名为“self”，表明这个组里面的模板是自定义的，可能仅适用于自己的工作场景。

在组里新建一个模板，快捷键定义为`*`，确认方式选择`Enter`，即在应用模板的地方，输入`/*+回车`，即可生成模板内容。

Template text 模板定义如下:
```
*
 * @Description $END$
 * @Author xxx
 * @Create $date$ $time$
 $params$
 */
```

`$params$`是一个自定义的变量，用于枚举方法中的参数，即@param的内容。将`$params$`这个变量对应的表达式写为执行Groovy脚本，即拆分methodParameters()返回的“一串”参数，并在每个参数前面添加@param并换行。

点击Edit variables编辑变量, 添加脚本:

param的Groovy脚本:
```Groovy
groovyScript("def result=''; def params=\"${_1}\".replaceAll('[\\\\[|\\\\]|\\\\s]', '').split(',').toList(); def rs=\"${_2}\"; for(i = 0; i < params.size(); i++) { if (i == 0) { result += '* @param ' + params[i] + ((i < params.size() - 1) ? '\\n' : ''); } else { result += ' * @param ' + params[i] + ((i < params.size() - 1) ? '\\n' : ''); } }; result+=rs == 'void' ? '' : '\\n * @return ';return result", methodParameters(), methodReturnType())
```

`$date$`也是一个自定义变量，对应的表达式使用内置的date()函数，表示输出当前的日期。
`$time$`也是一个自定义变量，对应的表达式使用内置的time()函数，表示输出当前的时间。
