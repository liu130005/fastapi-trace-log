import cv2

img = cv2.imread("test.jpg")
if img is not None:
    img_copy = img.copy()
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 查找轮廓
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓
    cv2.drawContours(img_copy, contours, -1, (0, 255, 0), 2)

    # 计算轮廓面积和周长
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)  # closed=True表示闭合轮廓
        print(f"轮廓{i + 1}：面积={area}, 周长={perimeter}")

    cv2.imshow("Contours", img_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()