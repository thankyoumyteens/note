# 自定义 Hook

自定义 Hook 主要是为了逻辑复用。

```jsx
import { useEffect, useState } from "react";

// 自定义Hook
function usePersonInfo() {
  const [person, setPerson] = useState({});

  useEffect(() => {
    setPerson({
      name: "unknown",
      age: -1,
    });
  }, []);

  const setPersonInfo = (p) => {
    setPerson({ ...p });
  };

  return [person, setPersonInfo];
}

function App() {
  // 多次执行同一个Hook, 它们的数据各自独立
  const [person1, setPerson1] = usePersonInfo();
  const [person2, setPerson2] = usePersonInfo();

  return (
    <div>
      <h1>{person1.name}</h1>
      <h1>{person2.name}</h1>
      <button
        onClick={() =>
          setPerson1({
            name: "Tom",
            age: 10,
          })
        }
      >
        切换1
      </button>
      <button
        onClick={() =>
          setPerson2({
            name: "Jack",
            age: 10,
          })
        }
      >
        切换2
      </button>
    </div>
  );
}

export default App;
```
