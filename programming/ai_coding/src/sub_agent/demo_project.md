# 项目准备

```sh
git clone https://github.com/spring-petclinic/spring-petclinic-rest.git
cd spring-petclinic-rest
./mvnw test
./mvnw spring-boot:run
```

它默认使用 H2 内存数据库，启动后可以访问：

```
http://localhost:9966/petclinic/
http://localhost:9966/petclinic/swagger-ui.html
http://localhost:9966/petclinic/v3/api-docs
```

README 里列出的 API 包括 owners、pets、vets、pet types、specialties、visits、users 等资源，足够做很多小步功能练习。

它不是玩具项目，因为有真实实体关系；但也不是大型企业项目，不会一上来被认证、微服务、消息队列、复杂部署拖死。
