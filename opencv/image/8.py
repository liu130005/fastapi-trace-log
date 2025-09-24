import cv2
import numpy as np

# 读取二值图
img = cv2.imread("binary.png", 0)
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# 结构元素（卷积核）
kernel = np.ones((5, 5), np.uint8)

# 腐蚀
erosion = cv2.erode(thresh, kernel, iterations=1)

# 膨胀
dilation = cv2.dilate(thresh, kernel, iterations=1)

# 开运算（腐蚀+膨胀）
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# 闭运算（膨胀+腐蚀）
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# 形态学梯度（膨胀-腐蚀）
gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)

cv2.imshow("Original", thresh)
cv2.imshow("Opening", opening)
cv2.imshow("Gradient", gradient)
cv2.imshow("Closing", closing)
cv2.waitKey(0)
cv2.destroyAllWindows()