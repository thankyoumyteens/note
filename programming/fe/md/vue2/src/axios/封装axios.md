# 封装axios

创建一个新的文件, 例如`api.js`。

```javascript
// 导入axios
import axios from 'axios';
// 创建一个axios实例, 并添加自定义的配置: 
const api = axios.create({
  baseURL: 'https://api.example.com', // 设置基础URL
  timeout: 5000, // 设置请求超时时间
  headers: {
    'Content-Type': 'application/json' // 设置请求头
  }
});
// 在axios实例上添加自定义的方法: 
export const get = (url, params) => {
    return api.get(url, {
        params: params
    });
};

export const post = (url, params) => {
    return api.post(url, params);
};
// 添加请求拦截器
api.interceptors.request.use(
    config => {
        // 在请求发送之前做些什么
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        // 对请求错误做些什么
        return Promise.reject(error);
    }
);
// 添加响应拦截器
api.interceptors.response.use(
    response => {
        // 对响应数据做些处理
        return response;
    },
    error => {
        // 对响应错误做些处理
        return Promise.reject(error);
    }
);
// 导出axios实例
export default api; // 导出整个axios实例
```

在其他文件中导入和使用封装好的axios实例或方法: 

```javascript
import api from './api'; // 导入整个axios实例
```
