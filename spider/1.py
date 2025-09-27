# 导入uiautomator2库
import time

import uiautomator2 as u2
from uiautomator2 import Device


# USB连接手机

def open_app():
    device = u2.connect('8XGEF6YX6D7TNRJF')
    # app启动
    device.app_start('com.hrfax.zjbocshare')

    return device


# 填入用户名和密码（请根据实际的元素标识符调整）
# device(text="请输入用户名").set_text("1234567")
# device(resourceId="com.hrfax.zjbocshare:id/phoneEditText").wait(5)
# device(resourceId="com.hrfax.zjbocshare:id/phoneEditText").set_text("1234568")
# device(resourceId="com.hrfax.zjbocshare:id/pwdEditText").set_text("111111")
# device.press("back")
# # 点击登录按钮
# device(resourceId="com.hrfax.zjbocshare:id/tv_login_login").click()

# 列举正在运行的 app
# device.app_list_running()


# time.sleep(10)
#
# device(text="历史").click()
#
# device(resourceId="com.hrfax.zjbocshare:id/btnHistory").wait(3)
# device(resourceId="com.hrfax.zjbocshare:id/btnHistory").click()
#
# device(resourceId="com.hrfax.zjbocshare:id/iv_sex").wait(3)
# device(resourceId="com.hrfax.zjbocshare:id/iv_sex").click()
#
# time.sleep(20)

# device(resourceId="com.hrfax.zjbocshare:id/title_tv").click()
# device(text="订单日志").click()
#
# time.sleep(3)

def get_latest_audit_info(device: Device):
    try:
        # 获取 RecyclerView
        recycler_view = device(className="androidx.recyclerview.widget.RecyclerView")

        if recycler_view.exists and len(recycler_view) > 0:
            # 获取 RecyclerView 中的第一个 LinearLayout 子元素
            first_linear_layout = recycler_view.child(className="android.widget.LinearLayout")[0]

            if first_linear_layout.exists:
                # 获取第一个 LinearLayout 中的第二个 LinearLayout 子元素
                second_linear_layout = first_linear_layout.child(className="android.widget.LinearLayout")[1]

                if second_linear_layout.exists:
                    # 遍历第二个 LinearLayout 中的前两个 LinearLayout 子元素
                    latest_audit_info = ""
                    for index in range(2):
                        if len(second_linear_layout.child(className="android.widget.LinearLayout")) > index:
                            # 获取第二个 LinearLayout 中的第 index+1 个 LinearLayout 子元素
                            target_linear_layout = second_linear_layout.child(className="android.widget.LinearLayout")[index]

                            if target_linear_layout.exists:
                                # 获取目标 LinearLayout 内的所有 TextView
                                text_views = target_linear_layout.child(className="android.widget.TextView")
                                # 获取每个 TextView 的文本值
                                for i, text_view in enumerate(text_views):
                                    if text_view.exists:
                                        text_value = text_view.get_text()
                                        latest_audit_info += text_value
                            else:
                                print(f"未找到第 {index + 1} 个 LinearLayout")
                        else:
                            print(f"第二个 LinearLayout 中少于 {index + 1} 个 LinearLayout 子元素")

                        latest_audit_info += "\n"
                else:
                    print("未找到第二个 LinearLayout")
            else:
                print("未找到第一个 LinearLayout")
        else:
            print("未找到 `androidx.recyclerview.widget.RecyclerView` 或为空")

    except Exception as e:
        print(f"获取元素信息时出错: {e}")

    print(latest_audit_info)
    return latest_audit_info


if __name__ == '__main__':
    device = open_app()
    # get_latest_audit_info(device)

    # device.press("back")
    # time.sleep(5)
    # 滑动到指定的 item 位置
    # 滚动到下一个页面
    # 直接滚动到指定索引的item
    # 逐步向前滚动到指定位置
    # 直接滚动到指定索引的item
    # 滚动到下一个页面
    count = 4
    fy = 180 + 453 * 7
    duration =  4.0
    for i in range(count):
        device.swipe(0, 1086, 0, 180, 1.0)  # 从(0,1)滑动到(0,180)



