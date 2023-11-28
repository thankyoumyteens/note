# 分词

ES6中, 只对```text```类型进行分词

可以指定让搜索的字段不进行分词, 例如设置为```keyword```字段。

ES的默认分词器是```standard```, 可直接通过API指定分词器以及字符串查看分词结果。

使用```standard```进行英文分词: 

```json
POST http://localhost:9200/_analyze
{
	"analyzer":"standard",
	"text":"hello world" 
}
```

ES响应: 

```json
{
    "tokens": [
        {
            "token": "hello",
            "start_offset": 0,
            "end_offset": 5,
            "type": "<ALPHANUM>",
            "position": 0
        },
        {
            "token": "world",
            "start_offset": 6,
            "end_offset": 11,
            "type": "<ALPHANUM>",
            "position": 1
        }
    ]
}
```

如果对“helloword”进行分词, 结果将只有“helloword”一个词, ```standsard```对英文按照空格进行分词。

# 中文分词ik插件

ik下载地址（直接下载编译好了的zip文件, 需要和ES版本一致）: [https://github.com/medcl/elasticsearch-analysis-ik/releases](https://github.com/medcl/elasticsearch-analysis-ik/releases)。

下载完成后解压```elasticsearch-analysis-ik-6.3.2.zip```将解压后的文件夹直接放入ES安装目录下的```plugins```文件夹中, 重启ES。

使用ik插件的```ik_smart```分词器: 

```json
POST http://localhost:9200/_analyze
{
  "analyzer":"ik_smart",
  "text":"学生"
}
```

ES响应: 

```json
{
    "tokens": [
        {
            "token": "学生",
            "start_offset": 0,
            "end_offset": 2,
            "type": "CN_WORD",
            "position": 0
        }
    ]
}
```

```ik_smart```会按照关键字的**最粗粒度进行分词**, 比如搜索“北京大学”时, “北京大学”是一个特定的词汇, 它并不是指“北京的大学”, 此时“北京大学”不会被分词。

```ik_max_word```则会按照**最细粒度进行分词**, 同样搜索“北京大学”时, 它将会被分词为“北京大学”, “北京大”, “北京”, “大学”。

有时候一个词并不在ik插件的词库中, 例如很多网络用语等, 此时我们可以将其添加到ik插件的自定义词库中。

“小米手机”使用```ik_smart```的分词结果: 

```json
{
    "tokens": [
        {
            "token": "小米",
            "start_offset": 0,
            "end_offset": 2,
            "type": "CN_WORD",
            "position": 0
        },
        {
            "token": "手机",
            "start_offset": 2,
            "end_offset": 4,
            "type": "CN_WORD",
            "position": 1
        }
    ]
}
```

进入ik插件安装目录```elasticsearch-5.6.0/plugins/elasticsearch/config```, 创建名为```custom.dic```的自定义词库, 向文件中添加“小米手机”并保存。仍然是此目录, 修改```IKAnalyzer.cfg.xml```文件, 如下所示: 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
        <comment>IK Analyzer 扩展配置</comment>
        <!--用户可以在这里配置自己的扩展字典 -->
        <entry key="ext_dict">custom.dic</entry>
         <!--用户可以在这里配置自己的扩展停止词字典-->
        <entry key="ext_stopwords"></entry>
        <!--用户可以在这里配置远程扩展字典 -->
        <!-- <entry key="remote_ext_dict">words_location</entry> -->
        <!--用户可以在这里配置远程扩展停止词字典-->
        <!-- <entry key="remote_ext_stopwords">words_location</entry> -->
</properties>
```

重启ES后, 再次通过```ik_smart```对“小米手机”进行分词, 发现“小米手机”不再被分词。

# 创建映射指定分词器

在创建映射时, 可以指定字段采用哪种分词器, 避免我们在每次搜索时都指定。

创建word索引	```PUT http://localhost:9200/word```

创建analyzer_demo类型并定义映射

```json
PUT http://localhost:9200/word/analyzer_demo/_mapping
{
  "properties":{
    "name":{
      "type":"text",
        "analyzer":"ik_smart"
    }
  }
}
```

查看word索引结构  ```GET http://localhost:9200/word ```

ES响应: 

```json
{
  "word": {
    "aliases": {},
    "mappings": {
      "analyzer_demo": {
        "properties": {
          "name": {
            "type": "text",
            "analyzer": "ik_smart"
          }
        }
      }
    },
    "settings": {
      "index": {
        "creation_date": "1561304920088",
        "number_of_shards": "5",
        "number_of_replicas": "1",
        "uuid": "A2YO9GpzRrGAIm2Q6rCoWA",
        "version": {
          "created": "5060099"
        },
        "provided_name": "word"
      }
    }
  }
}
```

可以看到ES在对name字段进行分词时会采用```ik_smart```分词器。
