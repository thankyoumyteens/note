# Context 声明类型

```ts
import { createContext } from "react";

interface TitleType {
  value: string;
}

const TitleContext = createContext<TitleType>({ value: "title1" });
export default TitleContext;
```
