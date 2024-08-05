# rabbitmq

```sh
sudo apt update
sudo apt install rabbitmq-server
sudo systemctl status rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmqctl add_user 用户名 密码
sudo rabbitmqctl set_user_tags 用户名 administrator
sudo rabbitmqctl set_permissions -p / 用户名 ".*" ".*" ".*"
```

访问 http://your_server_ip:15672/ 来使用 Web 管理界面，使用之前创建的用户登录。
