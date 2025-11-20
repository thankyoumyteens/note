# 摄像头视频捕获

```py
import cv2


def capture_camera_basic():
    # 初始化摄像头（0=默认摄像头，1=外接摄像头，依此类推）
    cap = cv2.VideoCapture(0)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("错误：无法打开摄像头！")
        return

    # 可选：设置摄像头参数（分辨率、帧率，需摄像头支持）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 高度
    cap.set(cv2.CAP_PROP_FPS, 30)  # 帧率

    # 循环读取视频帧
    while True:
        # 读取一帧（ret=是否成功读取，frame=帧数据）
        ret, frame = cap.read()

        # 若读取失败（如摄像头断开），退出循环
        if not ret:
            print("警告：无法读取视频帧，退出！")
            break

        # 实时显示帧（窗口名："Camera Capture"）
        cv2.imshow("Camera Capture", frame)

        # 按键控制（按 ESC 退出，按 S 保存当前帧）
        key = cv2.waitKey(1) & 0xFF  # 等待1ms，获取按键
        if key == 27:  # ESC 键（ASCII码27）
            print("用户按下ESC，退出程序！")
            break
        elif key == ord('s'):  # S 键保存帧
            cv2.imwrite("captured_frame.jpg", frame)
            print("已保存当前帧为 captured_frame.jpg")

    # 释放资源（必须执行，否则摄像头会被占用）
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_camera_basic()
```
