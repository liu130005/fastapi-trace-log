import torch
import torch.nn as nn

# 创建模型
model = nn.Linear(3, 1)
print("权重形状:", model.weight.shape)  # torch.Size([1, 3])
print("偏置形状:", model.bias.shape)    # torch.Size([1])

# 查看初始权重和偏置
print("权重值:", model.weight.data)
print("偏置值:", model.bias.data)

# 创建输入
input = torch.randn(5, 3)
print("输入形状:", input.shape)  # torch.Size([5, 3])

# 手动计算验证
manual_output = input @ model.weight.t() + model.bias
print("手动计算结果:", manual_output)

# 模型计算结果
output = model(input)
print("模型计算结果:", output)

# 验证结果是否一致
print("结果是否一致:", torch.allclose(manual_output, output))
