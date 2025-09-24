import cv2

img = cv2.imread(r"/opencv/image/images/1.jpg")  # 替换为你的图像路径

if img is not None:
    # 图像属性
    print("形状（高, 宽, 通道）：", img.shape)  # (500, 800, 3) 表示高500px，宽800px，3通道
    print("像素总数：", img.size)  # 500×800×3 = 1,200,000
    print("数据类型：", img.dtype)  # 通常为uint8（0-255）

    # 像素操作
    pixel = img[100, 200]  # 获取(100行, 200列)的像素值（BGR）
    print("像素值(B, G, R)：", pixel)  # 例如 [128, 64, 32]

    img[100, 200] = [0, 255, 0]  # 修改为绿色（B=0, G=255, R=0）
    cv2.imshow("Modified Pixel", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()