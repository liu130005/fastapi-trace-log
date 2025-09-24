import cv2
print("OpenCV版本：", cv2.__version__)  # 输出类似 4.12.0 即成功
print("扩展模块路径：", cv2.data.haarcascades)  # 预训练模型路径（基础模块之一）

# 读取图像
img = cv2.imread(r"/opencv/image/images/1.jpg")  # 替换为你的图像路径

# 检查读取成功
if img is None:
    print("图像读取失败，请检查路径")
else:
    # 显示图像
    cv2.namedWindow("First OpenCV Demo", cv2.WINDOW_NORMAL)
    cv2.imshow("First OpenCV Demo", img)

    # 等待按键并关闭窗口
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 保存图像
    cv2.imwrite("first_demo_saved.jpg", img)
    print("图像保存成功")