# 枚举

```ts
const enum Type {
  A,
  B,
  C,
}

function getTypeName(type: Type) {
  switch (type) {
    case Type.A:
      return "A";
    case Type.B:
      return "B";
    case Type.C:
      return "C";
  }
}
```
