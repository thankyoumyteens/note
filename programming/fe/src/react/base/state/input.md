# input 标签双向绑定

```jsx
import { useState } from "react";

function App() {
  const [inputText, setInputText] = useState("");
  return (
    <div>
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <br />
      <p>{inputText}</p>
    </div>
  );
}

export default App;
```
