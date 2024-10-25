# 渲染列表

```jsx
function MyApp() {
  let dataList = [
    { id: 1, name: "John" },
    { id: 2, name: "Doe" },
    { id: 3, name: "Jane" },
  ];
  return (
    <div>
      <ul>
        {/* 使用 map 方法遍历 dataList 数组 */}
        {dataList.map((data) => (
          <li key={data.id}>{data.name}</li>
        ))}
      </ul>
    </div>
  );
}
```
