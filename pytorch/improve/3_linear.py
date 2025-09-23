import torch
import numpy as np
import matplotlib.pyplot as plt
from torch import nn

# 随机种子，确保每次运行结果一致
torch.manual_seed(42)

# 生成训练数据
X = torch.randn(100, 2)  # 100 个样本，每个样本 2 个特征
true_w = torch.tensor([2.0, 3.0])  # 假设真实权重
true_b = 4.0  # 偏置项
Y = X @ true_w + true_b + torch.randn(100) * 0.1  # 加入一些噪声

# 打印部分数据
print(X[:5])
print(Y[:5])

# 定义线性回归模型
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__() # 继承父类
        self.linear = nn.Linear(2, 1)  # 输入维度为 2，输出维度为 1

    def forward(self, x):
        return self.linear(x)

# 创建模型实例
model = LinearRegressionModel()

# 定义损失函数
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练模型
for epoch in range(1000):
    model.train()

    # 前向传播
    predictions = model(X) # 模型预测结果
    loss = criterion(predictions.squeeze(), Y) # # 计算损失

    # 反向传播
    optimizer.zero_grad() # 清空梯度
    loss.backward() # 计算梯度
    optimizer.step() # 更新参数

    # 打印损失
    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/1000], Loss: {loss.item():.4f}')


# 测试模型
# 查看训练后的权重和偏置
print(f'Predicted weight: {model.linear.weight.data.numpy()}')
print(f'Predicted bias: {model.linear.bias.data.numpy()}')

# 在新数据上做预测
with torch.no_grad(): # 禁用梯度计算
    predictions = model(X)


# 可视化预测与实际值
plt.scatter(X[:, 0], Y, color='blue', label='True values')
plt.scatter(X[:, 0], predictions, color='red', label='Predictions')
plt.legend()
plt.show()

# 在训练过程中，随着损失逐渐减小，，我们希望最终的模型能够拟合我们生成的数据。通过查看训练后的权重和偏置，我们可以看到它们与真实权重和偏置非常接近。
# 理论上，模型的输出权重应该接近true_w和true_b
# 在可视化的散点图中，蓝色点表示真实值，红色点表示预测值。我们可以看到，预测值与真实值非常接近。




















