# 基本使用

1. 安装

```sh
npm install zustand
```

2. 定义 store

```ts
import { create } from "zustand";

interface User {
  userId?: string;
  username?: string;
}
interface UserStore {
  user: User;
}

const useCouterStore = create<UserStore>(() => {
  return {
    // 在组件之间共享的状态
    user: {
      userId: "cust",
      username: "cust",
    }, // 初始化状态
  };
});

// 用来修改状态的方法
const setUser = (user: User) => {
  useCouterStore.setState((state) => {
    return { user: { ...state.user, ...user } };
  });
};
const clearUser = () => {
  useCouterStore.setState({ user: {} });
};

export { useCouterStore, setUser, clearUser };
```

3. 使用

```tsx
import { useCouterStore, setUser, clearUser } from "./user";

function App() {
  // 获取状态
  const user = useCouterStore((state) => state.user);

  return (
    <>
      <h1>{user.username}</h1>
      <button onClick={() => setUser({ userId: "1", username: "jane" })}>
        设置用户
      </button>
      <button onClick={clearUser}>清除用户</button>
    </>
  );
}

export default App;
```
