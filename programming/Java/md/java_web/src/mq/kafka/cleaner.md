# 数据清理机制

1. 根据消息的保留时间, 当消息在 kafka 中保存的时间超过阈值(log.retention.hours=168, 默认 7 天), 就会触发清理
2. 根据 topic 存储的数据大小, 当 topic 所占的空间超过阈值(log.retention.bytes=1073741824, 默认关闭), 则开始删除最久的消息
