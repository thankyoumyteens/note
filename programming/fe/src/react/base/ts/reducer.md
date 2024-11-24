# useReducer 声明类型

```tsx
import { useReducer } from "react";

// state 的类型
interface UserInfo {
  name?: string;
}

// action type 的可选值
const enum ActionType {
  SET_NAME,
  CLEAR_NAME,
}

interface Action {
  type: ActionType;
  name?: string;
}

function reducer(state: UserInfo, action: Action): UserInfo {
  switch (action.type) {
    case ActionType.SET_NAME:
      return { name: action.name };
    case ActionType.CLEAR_NAME:
      return {};
    default:
      return state;
  }
}

function App() {
  const [user, dispatch] = useReducer(reducer, {});
  return (
    <div>
      <div>
        <h1>name: {user.name}</h1>
        <button
          onClick={() => dispatch({ type: ActionType.SET_NAME, name: "Jack" })}
        >
          set user
        </button>
      </div>
    </div>
  );
}

export default App;
```
