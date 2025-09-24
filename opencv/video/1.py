import cv2

# 打开视频文件（参数0为摄像头）
cap = cv2.VideoCapture("test_video.mp4")

if not cap.isOpened():
    print("无法打开视频")
    exit()

# 循环读取帧
while True:
    ret, frame = cap.read()  # ret：是否成功，frame：当前帧
    if not ret:
        break  # 视频结束

    # 显示帧
    cv2.imshow("Video", frame)

    # 按q退出
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()