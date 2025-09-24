import cv2

gray = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)
if gray is not None:
    # 简单阈值
    ret, thresh_bin = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # 二值化
    ret, thresh_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)  # 反二值化
    ret, thresh_trunc = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)  # 截断

    # 自适应阈值
    adaptive_gauss = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    cv2.imshow("Binary", thresh_bin)
    cv2.imshow("Adaptive Gaussian", adaptive_gauss)
    cv2.waitKey(0)
    cv2.destroyAllWindows()