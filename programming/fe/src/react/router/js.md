# 编程式跳转

```tsx
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate("/");
  };

  const handleAboutClick = () => {
    navigate("/about");
  };

  return (
    <ul>
      <li onClick={handleHomeClick}>首页</li>
      <li onClick={handleAboutClick}>关于我们</li>
    </ul>
  );
}

export default Navbar;
```
