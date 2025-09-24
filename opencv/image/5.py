import cv2

img = cv2.imread(r"/opencv/image/images/1.jpg")
if img is not None:
    # 缩放
    resized = cv2.resize(img, (400, 300), interpolation=cv2.INTER_AREA)  # 缩小时推荐
    scaled = cv2.resize(img, None, fx=0.5, fy=0.5)  # 按50%缩放

    # 裁剪（[y1:y2, x1:x2]）
    cropped = img[100:300, 200:400]  # 裁剪区域

    # 旋转
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)  # 旋转90度
    rotated = cv2.warpAffine(img, M, (cols, rows))

    cv2.imshow("Resized", resized)
    cv2.imshow("Cropped", cropped)
    cv2.imshow("Rotated", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()