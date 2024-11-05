# 数组类型的 state

```jsx
import { useState } from "react";

function App() {
  const [persons, setPersons] = useState([
    {
      name: "张三",
      age: 18,
    },
    {
      name: "王五",
      age: 20,
    },
  ]);

  const addPerson = () => {
    // 添加新元素
    setPersons([
      ...persons,
      {
        name: "李四",
        age: 19,
      },
    ]);
  };

  const changePerson = () => {
    // 修改元素
    persons[0].name = "张三丰";
    setPersons([...persons]);
  };
  const removePerson = () => {
    // 删除元素
    const newArray = persons.filter((item, index) => {
      return index !== 0;
    });
    setPersons([...newArray]);
  };
  return (
    <div>
      <div>
        {persons.map((item, index) => {
          return (
            <div key={index}>
              <span>{item.name}</span>
              <span>{item.age}</span>
            </div>
          );
        })}
      </div>
      <button onClick={addPerson}>新增</button>
      <button onClick={changePerson}>修改</button>
      <button onClick={removePerson}>删除</button>
    </div>
  );
}

export default App;
```
