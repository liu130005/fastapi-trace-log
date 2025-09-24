import cv2

img = cv2.imread(r"/opencv/image/images/1.jpg")
if img is not None:
    # BGR转灰度（常用）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # BGR转RGB（用于Matplotlib显示）
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # BGR转HSV（适合颜色检测）
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # BGR转Lab（光照不变性）
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    cv2.imshow("Gray", gray)
    cv2.imshow("RGB", rgb)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Lab", lab)
    cv2.waitKey(0)
    cv2.destroyAllWindows()