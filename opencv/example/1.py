import cv2
import numpy as np

# 读取两张重叠的图像（左右视角）
# 注：需要保证两张图像有足够的重叠区域才能成功拼接
img_left = cv2.imread("left.jpg")  # 左侧图像
img_right = cv2.imread("right.jpg")  # 右侧图像

# 转换为灰度图，减少计算量
gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)  # 左侧灰度图
gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)  # 右侧灰度图

# 初始化ORB特征检测器（Oriented FAST and Rotated BRIEF）
# ORB是一种高效的局部特征描述符，适合实时应用
orb = cv2.ORB_create()

# 检测特征点并计算描述符
# kp: 关键点（图像中具有独特性的点，如角点、边缘等）
# des: 描述符（对关键点周围区域的特征进行量化的向量）
kp_left, des_left = orb.detectAndCompute(gray_left, None)  # 左侧图像的关键点和描述符
kp_right, des_right = orb.detectAndCompute(gray_right, None)  # 右侧图像的关键点和描述符

# 初始化暴力匹配器（BFMatcher）
# 匹配规则：cv2.NORM_HAMMING适合ORB描述符（二进制特征）
# crossCheck=True：只有当A在B中的最佳匹配同时也是B在A中的最佳匹配时，才认为是有效匹配
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# 对左右图像的描述符进行匹配
matches = bf.match(des_left, des_right)

# 按匹配距离排序（距离越小，匹配质量越高）
# 匹配距离表示两个描述符的差异程度，值越小说明特征越相似
matches = sorted(matches, key=lambda x: x.distance)

# 提取匹配点对的坐标
# queryIdx：左侧图像中关键点的索引
# trainIdx：右侧图像中关键点的索引
# reshape(-1, 1, 2)：将坐标转换为OpenCV需要的形状（N×1×2）
src_pts = np.float32([kp_left[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)  # 左侧匹配点坐标
dst_pts = np.float32([kp_right[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)  # 右侧匹配点坐标

# 计算单应性矩阵（Homography Matrix）
# 单应性矩阵描述了两个平面之间的映射关系，可用于将左侧图像投影到右侧图像的视角
# cv2.RANSAC：随机采样一致性算法，用于剔除错误匹配（外点）
# 5.0：判断内点的阈值（像素距离）
M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# 拼接图像
# 获取右侧图像的高度和宽度
h, w = img_right.shape[:2]

# 对左侧图像进行透视变换，将其投影到右侧图像的坐标系
# 输出图像大小设置为：左侧宽度+右侧宽度，高度为右侧高度（确保能容纳拼接结果）
result = cv2.warpPerspective(img_left, M, (img_left.shape[1] + w, h))

# 将右侧图像拼接到结果的左侧（因为左侧图像已被变换到右侧视角）
result[:h, :w] = img_right  # 覆盖结果图像的对应区域

# 显示拼接后的全景图
cv2.imshow("Panorama", result)
cv2.waitKey(0)  # 等待用户按键
cv2.destroyAllWindows()  # 关闭所有窗口