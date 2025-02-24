# 拦截器

```ts
// request表示拦截uni.request()方法
uni.addInterceptor("request", {
  // 请求发出前触发
  invoke(options: UniApp.RequestOptions) {
    // 修改请求地址
    options.url = "http://localhost:8080" + options.url;
    // 修改请求超时时间(单位: 毫秒)
    options.timeout = 10000;
    // 修改请求头
    options.header = {
      ...options.header,
      Authorization: "Bearer 123123123123123123123",
    };
  },
  success(result: UniApp.RequestSuccessCallbackResult) {
    // 请求成功后，打印响应信息
    console.log("interceptor-success", result);
  },
  fail(err: UniApp.GeneralCallbackResult) {
    // 请求失败后，打印错误信息
    console.log("interceptor-fail", err);
  },
});

// 测试拦截器
export function test(username: string, password: string) {
  uni.request({
    url: "/user/login",
    method: "POST",
    data: {
      username: username,
      password: password,
    },
    success: (res) => {
      console.log(res);
    },
    fail: (err) => {
      console.log(err);
    },
  });
}
```
