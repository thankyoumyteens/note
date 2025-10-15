# 显示图像

```py
# 创建指定名称的窗口
cv2.namedWindow(winname='window1')
# 把img显示在名为window1的窗口上
cv2.imshow(winname='window1', mat=img)

# 等待用户按键, 避免窗口立即关闭
key = cv2.waitKey(delay=0)
# 销毁所有窗口
cv2.destroyAllWindows()
```

也可以不创建窗口, 直接使用 imshow 显示图片, 这样 imshow 会自动创建一个窗口。
