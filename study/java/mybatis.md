# MyBatis中${ }与\#{ }有什么区别

\#{}是预编译处理，MyBatis在处理#{}时, 它会将sql中的#{}替换为?, 
然后调用PreparedStatement的set方法来赋值

${}是字符串替换, MyBatis在处理${}时, 它会将sql中的${}替换为变量的值

使用${}会导致sql注入

# mybatis常用标签

## select标签　

属性介绍:

- id :唯一的标识符.
- parameterType:传给此语句的参数的全路径名或别名 例:com.test.poso.User
- resultType :语句返回值类型或别名。注意，如果是集合，那么这里填写的是集合的泛型，而不是集合本身（resultType 与resultMap 不能并用）

```
<select id="selectByPrimaryKey" resultMap="BaseResultMap" parameterType="com.test.poso.User">
    select * from student where id=#{id}
</select>
```

## insert标签

属性介绍:

- id :唯一的标识符
- parameterType:传给此语句的参数的全路径名或别名 例:com.test.poso.User

```
<insert id="insert" parameterType="com.test.poso.User">
    insert into student(name, age) values(#{name}, #{age})
</insert>
```

## delete标签

属性介绍:

- id :唯一的标识符
- parameterType:传给此语句的参数的全路径名或别名 例:com.test.poso.User

```
<delete id="deleteByPrimaryKey" parameterType="com.test.poso.User">
    delete from student where id=#{id}
</delete>
```

## update标签

属性介绍:

- id :唯一的标识符
- parameterType:传给此语句的参数的全路径名或别名 例:com.test.poso.User

```
<update id="updateByPrimaryKey" parameterType="com.test.poso.User">
    update student set name = #{name} where id = #{id}
</update>
```

## resultMap标签

基本作用：

- 建立SQL查询结果字段与实体属性的映射关系信息
- 查询的结果集转换为java对象，方便进一步操作。
- 将结果集中的列与java对象中的属性对应起来并将值填充进去

注意：与java对象对应的列不是数据库中表的列名，而是查询后结果集的列名

标签说明：

主标签：

- id:该resultMap的标志
- type：返回值的类名，此例中返回Studnet类

子标签：

- id:用于设置主键字段与领域模型属性的映射关系，此处主键为ID，对应id。
- result：用于设置普通字段与领域模型属性的映射关系

```
<resultMap id="BaseResultMap" type="com.online.model.Student">
        <id property="id" column="id" />
        <result column="NAME" property="name" />
        <result column="HOBBY" property="hobby" />
        <result column="MAJOR" property="major" />
        <result column="BIRTHDAY" property="birthday" />
        <result column="AGE" property="age" />
</resultMap>
  <!--查询时resultMap引用该resultMap -->  
<select id="selectByPrimaryKey" resultMap="BaseResultMap" parameterType="Object">
        select id,name,hobby,major,birthday,age from student where id=#{id}
</select> 
```

## if 标签
   
if标签通常用于WHERE语句、UPDATE语句、INSERT语句中，
通过判断参数值来决定是否使用某个查询条件、判断是否更新某一个字段、
判断是否插入某个字段的值。

```
<if test="name != null and name != ''">
         and NAME = #{name}
</if>
```

## foreach 标签

foreach标签主要用于构建in条件，可在sql中对集合进行迭代。
也常用到批量删除、添加等操作中。

属性介绍：

- collection：collection属性的值有三个分别是list、array、map三种，分别对应的参数类型为：List、数组、map集合。
- item ：表示在迭代过程中每一个元素的别名
- index ：表示在迭代过程中每次迭代到的位置（下标）
- open ：前缀
- close ：后缀
- separator ：分隔符，表示迭代时每个元素之间以什么分隔

```
<!-- in查询所有，不分页 -->
<select id="selectIn" resultMap="BaseResultMap">
    select name,hobby from student where id in
    <foreach item="item" index="index" collection="list" open="(" separator="," close=")">
        #{item}
    </foreach>
</select>
```

## where标签

where标签会知道如果它包含的标签中有返回值的话，它就插入一个‘where’。
此外，如果标签返回的内容是以AND 或OR 开头的，则它会剔除掉。

```
<select id="getStudentListWhere" parameterType="Object" resultMap="BaseResultMap">     
    SELECT * from STUDENT      
       <where>   
         <if test="name!=null and name!='' ">     
            NAME LIKE CONCAT(CONCAT('%', #{name}),'%')      
         </if>     
         <if test="hobby!= null and hobby!= '' ">     
            AND hobby = #{hobby}      
         </if>  
       </where>        
</select>    
```

## set标签

当在update语句中使用if标签时，如果最后的if没有执行，则或导致逗号多余错误。
使用set标签可以将动态的配置set关键字，和剔除追加到条件末尾的任何不相关的逗号。

```
<update id="updateStudent" parameterType="Object">     
    UPDATE STUDENT      
    <set>     
        <if test="name!=null and name!='' ">     
            NAME = #{name},      
        </if>     
        <if test="hobby!=null and hobby!='' ">     
            MAJOR = #{major},      
        </if> 
        <if test="hobby!=null and hobby!='' ">     
            HOBBY = #{hobby},  
        </if>     
    </set>     
    WHERE ID = #{id};      
</update>  
```

## trim标签

一般用于去除sql语句中多余的and关键字，逗号，或者给sql语句前拼接
“where“、“set“以及“values(“ 等前缀，或者添加“)“等后缀，
可用于选择性插入、更新、删除或者条件查询等操作。

trim属性主要有以下四个

- prefix：给sql语句拼接的前缀
- suffix：给sql语句拼接的后缀
- prefixOverrides：去除sql语句前面的关键字或者字符，该关键字或者字符由prefixOverrides属性指定，假设该属性指定为"AND"，当sql语句的开头为"AND"，trim标签将会去除该"AND"
- suffixOverrides：去除sql语句后面的关键字或者字符，该关键字或者字符由suffixOverrides属性指定

```
<insert id="insert" parameterType="Object">
    insert into student    
    <trim prefix="(" suffix=")" suffixOverrides=",">
        <if test="name != null">
            NAME,
        </if>
        <if test="hobby != null">
            HOBBY,
        </if>    
    </trim>    
    <trim prefix="values(" suffix=")" suffixOverrides=",">  
        <if test="name != null">
            #{name},
        </if>
        <if test="hobby != null">
            #{hobby},
        </if>
    </trim>
</insert>
```

## sql标签

定义常量

```
<sql id="Base_Column_List">
    ID,MAJOR,BIRTHDAY,AGE,NAME,HOBBY
</sql>
```

## include标签

用于引用定义的常量

```
<select id="selectAll" resultMap="BaseResultMap">
    SELECT
    <include refid="Base_Column_List" />
    FROM student
</select>
```

