import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

# 1. 数据加载与预处理
transform = transforms.Compose([
    transforms.ToTensor(),  # 转为张量
    transforms.Normalize((0.5,), (0.5,))  # 归一化到 [-1, 1]
])

# 加载MNIST数据集
train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=True, download=False, transform=transform)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

# 2. 定义CNN模型
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 定义卷积层
        # 输入通道数：1，输出通道数：32，卷积核大小：3，步长：1，填充：1
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1) #
        # 输入通道数：32，输出通道数：64，卷积核大小：3，步长：1，填充：1
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)

        # 定义全连接层
        # 输入维度：7*7*64，输出维度：128 展平后输入到全连接层
        self.fc1 = nn.Linear(7*7*64, 128)
        # 输入维度：128，输出维度：10 分类
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x)) # 第一层卷积层 + 激活函数
        x = F.max_pool2d(x, 2) # 最大池化层
        x = F.relu(self.conv2(x)) # 第二层卷积层 + 激活函数
        x = F.max_pool2d(x, 2) # 最大池化层
        x = x.view(-1, 7*7*64) # 展平
        x = F.relu(self.fc1(x)) # 第一层全连接层 + 激活函数
        x = self.fc2(x) # 第二层全连接层
        return x

# 创建模型实例
model = SimpleCNN()

# 3. 定义损失函数和优化器
criterion = nn.CrossEntropyLoss() # 多分类交叉熵损失
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# 4. 模型训练
num_epochs = 5
model.train() # 设置模型为训练模式

for epoch in range(num_epochs):

    total_loss = 0

    for images, labels in train_loader:
        outputs = model(images) # 前向传播
        loss = criterion(outputs, labels) # 计算损失

        optimizer.zero_grad() # 清空梯度
        loss.backward() # 反向传播
        optimizer.step() # 更新参数

        total_loss += loss.item()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss / len(train_loader):.4f}")


# 5. 模型陈岑是
model.eval() # 设置模型为评估模式
total_correct = 0
total_samples = 0

with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total_correct += (predicted == labels).sum().item()
        total_samples += labels.size(0)

accuracy = 100 * total_correct / total_samples
print(f"Test Accuracy: {accuracy:.4f}")

# 6.可视化测试结果
dataiter = iter(test_loader)
images, labels = next(dataiter)
outputs = model(images)
_, predictions = torch.max(outputs, 1)

fig, axes = plt.subplots(1, 6, figsize=(12, 4))
for i in range(6):
    axes[i].imshow(images[i][0], cmap='gray')
    axes[i].set_title(f"Label: {labels[i]}\nPred: {predictions[i]}")
    axes[i].axis('off')
plt.show()











