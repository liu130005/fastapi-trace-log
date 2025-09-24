import cv2
import numpy as np

img = cv2.imread("test.jpg")
if img is not None:
    # 1. 灰度滤镜
    gray_filter = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_filter = cv2.cvtColor(gray_filter, cv2.COLOR_GRAY2BGR)  # 转回3通道

    # 2. 反色滤镜
    invert_filter = 255 - img

    # 3. 复古滤镜（蓝通道降低，红通道提高）
    vintage = img.copy()
    vintage[:, :, 0] = cv2.add(vintage[:, :, 0], -50)  # B通道降低
    vintage[:, :, 2] = cv2.add(vintage[:, :, 2], 50)  # R通道提高

    # 4. 锐化滤镜
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpen_filter = cv2.filter2D(img, -1, kernel)

    # 显示效果
    cv2.imshow("Original", img)
    cv2.imshow("Vintage", vintage)
    cv2.imshow("Sharpen", sharpen_filter)
    cv2.waitKey(0)
    cv2.destroyAllWindows()