# 保存摄像头视频到本地

```py
import cv2


def capture_camera_save_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("错误：无法打开摄像头！")
        return

    # 设置视频参数
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 帧宽度（自动获取摄像头支持的宽度）
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 帧高度
    fps = 30  # 帧率（需与摄像头一致）
    # 视频编码器（mp4格式）
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # 保存视频（文件名、编码器、帧率、分辨率）
    out = cv2.VideoWriter("captured_video.mp4", fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 实时写入视频帧
        out.write(frame)

        # 显示实时画面
        cv2.imshow("Camera (Saving to video)", frame)

        # 按ESC退出
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    # 释放资源（注意：先释放VideoWriter，再释放摄像头）
    out.release()
    cap.release()
    cv2.destroyAllWindows()
    print("视频已保存为 captured_video.mp4")


if __name__ == "__main__":
    capture_camera_save_video()
```
