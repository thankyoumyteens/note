# 封装请求

```ts
export interface DataType<T> {
  code: number;
  message: string;
  data: T;
}

export const get = <T>(
  url: string,
  params: Object | Array<string | Object>
) => {
  return new Promise<DataType<T>>((resolve, reject) => {
    uni.request({
      url: url,
      method: "GET",
      data: params,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          const r = res.data as DataType<T>;
          console.log(r);
          if (r.code === 0) {
            resolve(r);
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
