# insightface 人脸识别

一站式人脸识别开源库，集成了当前 SOTA（State-of-the-Art）的模型（如 ArcFace、MobileFaceNet、RetinaFace 检测），支持人脸检测、关键点、特征提取、匹配全流程。

核心优势：

- 精度极高（在 LFW、CFP-FP 等公开数据集上排名前列）
- 支持轻量级模型（如 MobileFaceNet），可部署在移动端/边缘设备
- 提供 Python/Java/C++ API，工程化落地成本低

适用场景：

- 工业级项目（如考勤系统、人脸门禁、视频监控），追求高精度和稳定性

## 安装依赖

注意：Windows 系统可能需要先安装 Visual C++ 运行库

```sh
# 如果使用 CPU 运行:
pip install insightface opencv-python numpy onnxruntime
# 如果使用 GPU 运行:
pip install insightface opencv-python numpy onnxruntime-gpu
```

## 使用

```py
import cv2
import numpy as np
from insightface.app import FaceAnalysis


# 初始化 InsightFace 应用（自动下载预训练模型）
def init_insightface() -> FaceAnalysis:
    # 使用 CPU 运行
    # 如果电脑支持 GPU, 则可以换成: 'CUDAExecutionProvider'
    app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    # det_size：检测图像尺寸（越大检测精度越高）
    app.prepare(ctx_id=0, det_size=(640, 640))
    return app


# 准备已知人脸特征库
def init_faces(app: FaceAnalysis, known_face_path: str) -> tuple[list, list]:
    # 人脸特征编码列表
    known_face_encodings = []
    # 人脸姓名列表
    known_face_names = []

    # 加载已知人脸并提取特征
    known_img = cv2.imread(known_face_path)
    known_faces = app.get(known_img)  # 检测并提取人脸特征

    if len(known_faces) > 0:
        # embedding 为 512 维特征
        known_face_encodings.append(known_faces[0].embedding)
        known_face_names.append("Zhang San")
        print("已知人脸特征加载完成！")
    return known_face_encodings, known_face_names


# 实时摄像头人脸识别
def insightface_recognition(app: FaceAnalysis, known_face_encodings: list, known_face_names: list):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # 检测当前帧人脸并提取特征
        faces = app.get(frame)

        # 绘制人脸框和匹配结果
        for face in faces:
            # 人脸框坐标
            bbox = face.bbox.astype(int)
            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]

            # 特征匹配（余弦相似度）
            if known_face_encodings:
                similarity = np.dot(face.embedding, known_face_encodings[0]) / (
                        np.linalg.norm(face.embedding) * np.linalg.norm(known_face_encodings[0])
                )

                if similarity > 0.5:  # InsightFace 阈值通常设为 0.5
                    name = known_face_names[0]
                    text = f"{name} (sim: {similarity:.2f})"
                    color = (0, 255, 0)
                else:
                    text = f"Unknown (sim: {similarity:.2f})"
                    color = (0, 0, 255)
            else:
                text = "No Known Faces"
                color = (255, 0, 0)

            # 绘制
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("InsightFace Recognition", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 1. 初始化 InsightFace 应用（自动下载预训练模型）
    app = init_insightface()
    # 2. 准备已知人脸特征库
    known_face_encodings, known_face_names = init_faces(app, "zhang_san.jpg")
    # 3. 实时摄像头人脸识别
    insightface_recognition(app, known_face_encodings, known_face_names)
```
