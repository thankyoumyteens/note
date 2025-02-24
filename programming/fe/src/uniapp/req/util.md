# 封装请求

```ts
interface DataType<T> {
  code: number;
  message: string;
  data: T;
}

export const get = <T>(url: string, params: any) => {
  return new Promise<T>((resolve, reject) => {
    uni.request({
      url: url,
      method: "GET",
      data: params,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          const r = res.data as DataType<T>;
          if (r.code === 0) {
            resolve(r.data);
          } else {
            reject(r);
          }
        } else {
          uni.showToast({
            title: "数据获取失败",
          });
        }
      },
      fail: (err) => {
        uni.showModal({
          title: "请求失败",
          content: err.errMsg,
          showCancel: false,
          confirmText: "确定",
        });
      },
    });
  });
};
```

## 使用

```ts
import { get } from "../../utils/request";

const getData = async () => {
  const name = await get<string>("/getUserName", { uid: "123" });
  console.log(name);
};
```
