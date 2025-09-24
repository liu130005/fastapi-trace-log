import cv2

# 打开视频或摄像头
cap = cv2.VideoCapture(0)  # 0为摄像头

# 读取第一帧并选择跟踪区域
ret, frame = cap.read()
if not ret:
    exit()

# 手动框选目标（鼠标拖动选择）
bbox = cv2.selectROI("Select Target", frame, False)

# 初始化跟踪器（CSRT算法）
tracker = cv2.TrackerCSRT_create()
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 更新跟踪
    success, bbox = tracker.update(frame)

    # 绘制跟踪框
    if success:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Tracking failed", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()