import cv2
import numpy as np

# 读取两张同尺寸图像
img1 = cv2.imread(r"/opencv/image/images/1.jpg")
img2 = cv2.imread(r"/opencv/image/images/2.png")

# 使用cv2.resize()函数调整其中一个图像的大小以匹配另一个图像
if img1.shape[:2] != img2.shape[:2]:
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

if img1 is not None and img2 is not None:
    # 1. 加法（像素值超过255会截断）
    add1 = cv2.add(img1, img2)  # OpenCV加法（饱和运算）
    add2 = img1 + img2  # numpy加法（模运算，不推荐）

    # 2. 加权加法（图像融合）
    # 公式：dst = α×img1 + β×img2 + γ
    blended = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)  # 70% img1 + 30% img2

    # 3. 按位运算（常用于遮罩）
    # 创建两张200x200的图像
    img_a = np.zeros((200, 200, 3), np.uint8)
    img_b = np.zeros((200, 200, 3), np.uint8)
    cv2.rectangle(img_a, (50, 50), (150, 150), (0, 255, 0), -1)  # 绿色矩形
    cv2.circle(img_b, (100, 100), 50, (0, 0, 255), -1)  # 红色圆形

    bitwise_and = cv2.bitwise_and(img_a, img_b)  # 与（交集）
    bitwise_or = cv2.bitwise_or(img_a, img_b)  # 或（并集）
    bitwise_not = cv2.bitwise_not(img_a)  # 非（反转）

    # 显示结果
    cv2.imshow("Blended", blended)
    cv2.imshow("AND", bitwise_and)
    cv2.imshow("OR", bitwise_or)
    cv2.waitKey(0)
    cv2.destroyAllWindows()