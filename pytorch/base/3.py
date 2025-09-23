import torch
from torch import nn


# 定义一个简单的全连接神经网络
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # 输入层到隐藏层
        self.fc1 = nn.Linear(2, 2)
        # 隐藏层到输出层
        self.fc2 = nn.Linear(2, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))

        print("隐藏层输出:", x)

        x = self.fc2(x)
        return x

# 创建网络实例
model = SimpleNN()


# 创建示例输入
input = torch.randn(2, 2)  # 3个样本，每个样本2个特征
print("输入:", input)

# 前向传播
output = model(input)
print("输出:", output)

1.16899344
1.81360089


# 定义损失函数（例如均方误差MSE）
criterion = nn.MSELoss()

target = torch.randn(2, 1)
print("目标输出: ", target)

# 计算损失
loss = criterion(output, target)
print("损失: ", loss)

# 定义优化器（使用Adam优化器）
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练步骤
optimizer.zero_grad() # 清空梯度
loss.backward() # 反向传播
optimizer.step() # 更新参数
