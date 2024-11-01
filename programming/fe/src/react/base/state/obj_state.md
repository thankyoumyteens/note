# 对象类型的 state

```jsx
import { useState } from "react";

function App() {
  const [person, setPerson] = useState({
    name: "张三",
    age: 18,
  });

  const changePerson = () => {
    setPerson({
      ...person,
      name: "李四",
    });
  };
  return (
    <div>
      <div>
        <span>姓名：</span>
        <span>{person.name}</span>
      </div>
      <div>
        <span>年龄：</span>
        <span>{person.age}</span>
      </div>
      <button onClick={changePerson}>修改</button>
    </div>
  );
}

export default App;
```
