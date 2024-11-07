# 使用 TypeScript

实现一个 todo list:

1. 定义类型 type.ts:

```ts
export interface TodoItem {
  id: number;
  text: string;
  completed: boolean;
}
// TodoList组件接收的props类型
export interface TodoListProps {
  todoList: TodoItem[];
  changeCompleted: (id: number) => void;
  removeTodo: (id: number) => void;
  addTodo: (text: string) => void;
}
// TodoItem组件接收的props类型
export interface TodoItemProps {
  todoItem: TodoItem;
  changeCompleted: (id: number) => void;
  removeTodo: (id: number) => void;
}
```

2. TodoItem.tsx:

```tsx
import { TodoItemProps } from "../types";

export default function TodoItem(props: TodoItemProps) {
  const { todoItem, changeCompleted, removeTodo } = props;
  return (
    <>
      <div>
        <input
          type="checkbox"
          checked={todoItem.completed}
          onChange={() => changeCompleted(todoItem.id)}
        />
        <span
          style={{
            textDecoration: todoItem.completed ? "line-through" : "none",
          }}
        >
          {todoItem.text}
        </span>
        <button onClick={() => removeTodo(todoItem.id)}>Remove</button>
      </div>
    </>
  );
}
```

3. TodoList.tsx:

```tsx
import { useState } from "react";
import { TodoListProps } from "../types";
import TodoItem from "./TodoItem";

export default function TodoList(props: TodoListProps) {
  const { todoList, changeCompleted, removeTodo, addTodo } = props;
  const [todoText, setTodoText] = useState<string>("");
  return (
    <>
      <h1>Todo List</h1>
      <input
        type="text"
        value={todoText}
        onChange={(e) => setTodoText(e.target.value)}
      />
      <button onClick={() => addTodo(todoText)}>Add Todo</button>
      <ul>
        {todoList.map((item) => (
          <li key={item.id}>
            <TodoItem
              todoItem={item}
              changeCompleted={changeCompleted}
              removeTodo={removeTodo}
            />
          </li>
        ))}
      </ul>
    </>
  );
}
```

4. App.tsx:

```tsx
import { useState } from "react";
import { TodoItem } from "./types";
import TodoList from "./components/TodoList";

function App() {
  const [todoList, setTodoList] = useState<TodoItem[]>([]);
  const changeCompleted = (id: number) => {
    const newTodoList = todoList.map((item) => {
      if (item.id === id) {
        return { ...item, completed: !item.completed };
      }
      return item;
    });
    setTodoList(newTodoList);
  };
  const removeTodo = (id: number) => {
    const newTodoList = todoList.filter((item) => item.id !== id);
    setTodoList(newTodoList);
  };
  const addTodo = (text: string) => {
    const newTodo: TodoItem = {
      id: Math.floor(Math.random() * 1000),
      text,
      completed: false,
    };
    setTodoList([...(todoList || []), newTodo]);
  };
  return (
    <>
      <TodoList
        todoList={todoList}
        changeCompleted={changeCompleted}
        removeTodo={removeTodo}
        addTodo={addTodo}
      />
    </>
  );
}

export default App;
```
