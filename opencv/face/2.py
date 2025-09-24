import cv2
import numpy as np

# 读取目标物体和场景图像
object_img = cv2.imread("object.jpg", 0)  # 要识别的物体
scene_img = cv2.imread("scene.jpg", 0)  # 包含物体的场景

# 初始化ORB检测器
orb = cv2.ORB_create()

# 检测特征点和描述符
kp1, des1 = orb.detectAndCompute(object_img, None)
kp2, des2 = orb.detectAndCompute(scene_img, None)

# 匹配特征点
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)  # 按距离排序

# 绘制匹配结果
result = cv2.drawMatches(object_img, kp1, scene_img, kp2,
                         matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv2.imshow("Object Recognition", result)
cv2.waitKey(0)
cv2.destroyAllWindows()