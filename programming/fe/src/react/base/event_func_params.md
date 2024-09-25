# onClick 传参

```jsx
export default function UrlEncodeHelper() {
  function doConvert(e, a, b) {
    console.log(a, b);
  }

  return (
    <div>
      <button
        onClick={(e) => {
          doConvert(e, "123", "321");
        }}
      >
        转换
      </button>
    </div>
  );
}
```
