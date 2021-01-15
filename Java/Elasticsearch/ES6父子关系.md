# 父-子关系文档

假设现在有这样的需求场景：一个博客有多篇文章，文章有标题、内容、作者、日期等信息，同时一篇文章中会有评论，评论有评论的内容、作者、日期等信息，通过ES来存储博客的文章及评论信息。

此时文章本身就是"父"，而评论就是"子"，这类问题也可以通过```nested```嵌套对象实现，大部分情况下```netsted```嵌套对象和```parent-child```父子对象能够互相替代，但他们仍然不同的优缺点。下面将介绍这两种数据结构。

## nested嵌套对象

一篇文章的数据结构如下：

```json
{
    "title":"ElasticSearch6.x实战教程",
    "author":"OKevin",
    "content":"这是一篇水文",
    "created":1562141626000,
    "comments":[{
        "name":"张三",
        "content":"写的真菜",
        "created":1562141689000
    },{
        "name":"李四",
        "content":"辣鸡",
        "created":1562141745000
    }]
}
```

通过RESTful API创建索引及定义映射结构：

```json
PUT http://localhost:9200/blog
{
	"mappings":{
		"article":{
			"properties":{
				"title":{
					"type":"text",
					"analyzer":"ik_smart",
					"fields":{
						"keyword":{
							"type":"keyword",
							"ignore_above":256
						}
					}
				},
				"author":{
					"type":"text",
					"analyzer":"ik_smart",
					"fields":{
						"keyword":{
							"type":"keyword",
							"ignore_above":256
						}
					}
				},
				"content":{
					"type":"text",
					"analyzer":"ik_smart"
				},
				"created":{
					"type":"date"
				},
				"comments":{
					"type":"nested",
					"properties":{
						"name":{
							"type":"text",
							"analyzer":"ik_smart",
							"fields":{
								"keyword":{
									"type":"keyword",
									"ignore_above":256
								}
							}
						},
						"content":{
							"type":"text",
							"analyzer":"ik_smart",
							"fields":{
								"keyword":{
									"type":"keyword",
									"ignore_above":256
								}
							}
						},
						"created":{
							"type":"date"
						}
					}
				}
			}
		}
	}
}
```

插入数据：

```json
POST http://localhost:9200/blog/article
{
    "title":"ElasticSearch6.x实战教程",
    "author":"OKevin",
    "content":"这是一篇水文",
    "created":1562141626000,
    "comments":[{
        "name":"张三",
        "content":"写的真菜",
        "created":1562141689000
    },{
        "name":"李四",
        "content":"辣鸡",
        "created":1562141745000
    }]
}
```

### 查询作者为“OKevin”文章的所有评论（父查子）

```json
GET http://localhost:9200/blog/article/_search
{
	"query":{
		"bool":{
			"must":[{
				"match":{
					"author.keyword":"OKevin"
				}
			}]
		}
	}
}
```

ES结果返回2条作者为"OKevin"的全部数据(文章+评论)。

### 查询评论中含有“辣鸡”的文章（子查父）

```json
GET http://localhost:9200/blog/article/_search
{
	"query":{
		"bool":{
			"must":[{
				"match":{
					"author.keyword":"OKevin"
				}
			},{
				"nested":{
					"path":"comments",
					"query":{
						"bool":{
							"must":[{
								"match":{
									"comments.content":"辣鸡"
								}
							}]
						}
					}
				}
			}]
		}
	}
}
```

ES确实只返回了包含"辣鸡"的数据(文章+评论)。

## parent-child父子文档

文章数据结构

```json
{
    "title":"ElasticSearch6.x实战教程",
    "author":"OKevin",
    "content":"这是一篇实战教程",
    "created":1562141626000,
    "comments":[]
}
```

评论数据结构

```json
{
    "name":"张三",
    "content":"写的真菜",
    "created":1562141689000
}
```

ES6.x以前是将这两个结构分别存储在两个类型Type中关联(这看起来更接近关系型数据库表与表的关联查询)，但在ES6.x开始一个索引Index只能创建一个类型Type，要再想实现表关联查询，就意味着需要把上述两张表揉在一起，ES6.x由此定义了一个新的数据类型——```join```。

通过RESTful API创建索引及定义映射结构：

```json
{
	"mappings":{
		"article":{
			"properties":{
				"title":{
					"type":"text",
					"analyzer":"ik_smart",
					"fields":{
						"keyword":{
							"type":"keyword",
							"ignore_above":256
						}
					}
				},
				"author":{
					"type":"text",
					"analyzer":"ik_smart",
					"fields":{
						"keyword":{
							"type":"keyword",
							"ignore_above":256
						}
					}
				},
				"content":{
					"type":"text",
					"analyzer":"ik_smart"
				},
				"created":{
					"type":"date"
				},
				"comments":{
					"type":"join",
					"relations":{
						"article":"comment"
					}
				}
			}
		}
	}
}
```

重点关注其中的"comments"字段，可以看到类型定义为```join```，relations定义了谁是父谁是子，"article":"comment"表示article是父comment是子。

父子文档的插入是父与子分别插入(因为可以理解为把多个表塞到了一张表里)。

插入父文档：

```json
POST http://localhost:9200/blog/article/1
{
    "title":"ElasticSearch6.x实战教程",
    "author":"OKevin",
    "content":"这是一篇水文",
    "created":1562141626000,
    "comments":"article"
}
```

插入子文档：

```json
POST http://localhost:9200/blog/article/4?routing=1
{
    "name":"张三",
    "content":"写的真菜",
    "created":1562141689000,
    "comments":{
    	"name":"comment",
    	"parent":1
    }
}
```

如果查询索引数据会发现一共有9条数据，并不是```nested```那样将"评论"嵌套"文章"中的。

### 查询作者为“OKevin”文章的所有评论（父查子）

```json
GET http://localhost:9200/blog/article/_search
{
	"query":{
		"has_parent":{
			"parent_type":"article",
			"query":{
				"match":{
					"author.keyword":"OKevin"
				}
			}
		}
	}
}
```

ES只返回了comment评论结构中的数据，而不是全部包括文章数据也返回。这是嵌套对象查询与父子文档查询的区别之一——**子文档可以单独返回**。

### 查询评论中含有“辣鸡”的文章（子查父）

```json
GET http://localhost:9200/blog/artice/_search
{
	"query":{
		"has_child":{
			"type":"comment",
			"query":{
				"match":{
					"content":"辣鸡"
				}
			}
		}
	}
}
```

ES同样也只返回了父文档的数据，而没有子文档(评论)的数据。

```nested```嵌套对象和```parent-child```父子文档之间最大的区别，嵌套对象中的"父子"是一个文档数据，而父子文档的中的"父子"是两个文档数据。这意味着嵌套对象中如果涉及对嵌套文档的操作会对整个文档造成影响（重新索引，但查询快），包括修改、删除、查询。而父子文档子文档或者父文档本身就是**独立**的文档，对子文档或者父文档的操作并不会相互影响（不会重新索引，查询相对慢）。
