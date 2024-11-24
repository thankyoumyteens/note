# useState 声明类型

```tsx
import { useState } from "react";

interface UserInfo {
  name?: string;
}

function App() {
  // 指定state的类型是 null 或者 UserInfo
  const [user, setUser] = useState<UserInfo | null>(null);
  return (
    <div>
      <div>
        {/* ? 表示 user 可能为 null */}
        {/* user为null时不会继续获取name属性的值 */}
        {/* user不为null时才会去获取name属性的值 */}
        <h1>name: {user?.name}</h1>
        <button onClick={() => setUser({ name: "Jack" })}>set user</button>
      </div>
    </div>
  );
}

export default App;
```
