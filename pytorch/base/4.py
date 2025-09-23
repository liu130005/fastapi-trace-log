import torch
from torch import nn

# 1. 定义一个简单的神经网络模型
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(2, 2) # 输入层和隐藏层的维度
        self.fc2 = nn.Linear(2, 1) # 隐藏层和输出层的维度

    def forward(self, x):
        x = torch.relu(self.fc1(x)) # 使用 ReLU 激活函数
        x = self.fc2(x)
        return x

# 2. 创建模型实例
model = SimpleNN()

# 3. 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 4. 假设我们有训练数据X和Y
X = torch.randn(10, 2) # 假设有 10 个样本，每个样本有两个特征
Y = torch.randn(10, 1) # 10个目标值

# 5. 训练循环
for epoch in range(1000): # 训练 100 个周期
    # 前向传播
    optimizer.zero_grad() # 清空梯度
    outputs = model(X) # 前向传播
    loss = criterion(outputs, Y) # 计算损失
    loss.backward() # 反向传播
    optimizer.step() # 更新参数

    # 每10轮输出一次损失
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/1000], Loss: {loss.item():.4f}')
















