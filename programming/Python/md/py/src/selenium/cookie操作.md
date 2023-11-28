# cookie操作

| 方法                            | 说明                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| get_cookies()                     | 获得所有cookie信息                                                                                      |
| get_cookie(name)                  | 返回字典的key为“name”的cookie信息                                                                |
| add_cookie(cookie_dict)           | 添加cookie。“cookie_dict”指字典对象, 必须有name 和value 值                                  |
| delete_cookie(name,optionsString) | 删除cookie信息。“name”是要删除的cookie的名称, “optionsString”是该cookie的选项, 目前支持的选项包括“路径”, “域” |
| delete_all_cookies()              | 删除所有cookie信息                                                                                      |
