import cv2

img = cv2.imread("test.jpg")
if img is not None:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)  # 降噪

    # Canny边缘检测
    canny = cv2.Canny(blurred, 50, 150)  # 低阈值50，高阈值150

    # Sobel边缘检测（x方向）
    sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobel_x = cv2.convertScaleAbs(sobel_x)  # 转为绝对值

    # Laplacian边缘检测
    laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
    laplacian = cv2.convertScaleAbs(laplacian)

    cv2.imshow("Canny", canny)
    cv2.imshow("Sobel X", sobel_x)
    cv2.imshow("Laplacian", laplacian)
    cv2.waitKey(0)
    cv2.destroyAllWindows()