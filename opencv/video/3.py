import cv2

# 打开摄像头
cap = cv2.VideoCapture(0)

# 创建背景减除器（MOG2算法）
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, detectShadows=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 应用背景减除
    fgmask = fgbg.apply(frame)

    # 显示原图和前景掩码
    cv2.imshow("Frame", frame)
    cv2.imshow("Foreground Mask", fgmask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()