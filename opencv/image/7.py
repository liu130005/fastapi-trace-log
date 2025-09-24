import cv2

img = cv2.imread("noise.png")
if img is not None:
    # 1. 均值滤波
    mean_blur = cv2.blur(img, (5, 5))

    # 2. 高斯滤波
    gauss_blur = cv2.GaussianBlur(img, (5, 5), 0)

    # 3. 中值滤波（去椒盐噪声）
    median_blur = cv2.medianBlur(img, 5)

    # 4. 双边滤波（保边缘平滑）
    bilateral = cv2.bilateralFilter(img, 9, 75, 75)

    cv2.imshow("Original", img)
    cv2.imshow("Median Blur", median_blur)
    cv2.imshow("Bilateral", bilateral)
    cv2.imshow("Gaussian Blur", gauss_blur)
    cv2.waitKey(0)
    cv2.destroyAllWindows()