# 视频文件播放

注意：OpenCV 本身不支持音频处理（仅处理视频帧），所以播放视频时默认没有声音。

```py
import cv2


def play_video_advanced(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"错误：无法打开视频文件 {video_path}！")
        return

    # 获取视频基本信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps

    print(f"视频信息：{width}x{height} | {fps:.1f} FPS | 时长：{duration:.1f} 秒")
    print("操作说明：")
    print("  ESC：退出 | 空格：暂停/继续 | S：保存帧 | +：加速 | -：减速 | 拖拽进度条：调整进度")

    # 播放控制变量
    paused = False
    speed_multiplier = 1.0  # 倍速（默认1.0x）
    min_speed = 0.25  # 最小倍速
    max_speed = 4.0  # 最大倍速
    frame_interval = int(1000 / (fps * speed_multiplier))  # 动态调整帧间隔

    # 创建窗口并添加进度条（用于调整播放进度）
    cv2.namedWindow("Advanced Video Player", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Progress", "Advanced Video Player", 0, total_frames - 1, lambda x: None)

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("视频播放结束！")
                break

            # 更新进度条（同步当前播放位置）
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            cv2.setTrackbarPos("Progress", "Advanced Video Player", current_frame)

            # 在帧上显示倍速信息
            cv2.putText(
                frame, f"Speed: {speed_multiplier:.2f}x",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )

            cv2.imshow("Advanced Video Player", frame)

        # 按键控制
        key = cv2.waitKey(frame_interval) & 0xFF

        if key == 27:  # ESC：退出
            break
        elif key == ord(' '):  # 空格：暂停/继续
            paused = not paused
        elif key == ord('s'):  # S：保存帧
            if 'frame' in locals():
                cv2.imwrite(f"saved_frame_{current_frame}.jpg", frame)
                print(f"已保存帧 {current_frame} 为 saved_frame_{current_frame}.jpg")
        elif key == ord('+'):  # + 键：加速
            speed_multiplier = min(speed_multiplier + 0.25, max_speed)
            frame_interval = int(1000 / (fps * speed_multiplier))
            print(f"当前倍速：{speed_multiplier:.2f}x")
        elif key == ord('-'):  # - 键：减速
            speed_multiplier = max(speed_multiplier - 0.25, min_speed)
            frame_interval = int(1000 / (fps * speed_multiplier))
            print(f"当前倍速：{speed_multiplier:.2f}x")

        # 处理进度条拖拽（用户手动调整播放位置）
        if not paused:
            trackbar_pos = cv2.getTrackbarPos("Progress", "Advanced Video Player")
            # 若进度条位置与当前帧不一致，跳转到指定帧
            if abs(trackbar_pos - current_frame) > 1:
                cap.set(cv2.CAP_PROP_POS_FRAMES, trackbar_pos)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    VIDEO_PATH = "a.mp4"
    play_video_advanced(VIDEO_PATH)
```
