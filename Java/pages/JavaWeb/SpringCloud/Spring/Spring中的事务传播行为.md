# Spring中七种事务传播行为

事务的传播行为, 默认值为 Propagation.REQUIRED。可以手动指定其他的事务传播行为

- Propagation.REQUIRED: 如果当前存在事务, 则加入该事务, 如果当前不存在事务, 则创建一个新的事务。
- Propagation.SUPPORTS: 如果当前存在事务, 则加入该事务；如果当前不存在事务, 则以非事务的方式继续运行。
- Propagation.MANDATORY: 如果当前存在事务, 则加入该事务；如果当前不存在事务, 则抛出异常。
- Propagation.REQUIRES_NEW: 重新创建一个新的事务, 如果当前存在事务, 挂起当前的事务。外层事务不会影响内部事务的提交/回滚, 内部事务的异常, 会影响外部事务的回滚
- Propagation.NOT_SUPPORTED: 以非事务的方式运行, 如果当前存在事务, 暂停当前的事务。
- Propagation.NEVER: 以非事务的方式运行, 如果当前存在事务, 则抛出异常。
- Propagation.NESTED: 如果没有, 就新建一个事务；如果有, 就在当前事务中嵌套其他事务。
