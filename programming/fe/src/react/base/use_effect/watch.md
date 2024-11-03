# 监听 state

```jsx
import { useEffect, useState } from "react";

function App() {
  const [person, setPerson] = useState({
    name: "张三",
    age: 18,
  });
  useEffect(() => {
    console.log("person被修改");
  }, [person]);
  return (
    <div>
      <h1>{person.name}</h1>
      <h2>{person.age}</h2>
      <button onClick={() => setPerson({ name: "李四", age: 20 })}>修改</button>
    </div>
  );
}

export default App;
```
