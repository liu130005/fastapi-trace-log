import torch

x = torch.randn(2, 2, requires_grad=True)
print(x)

y = x + 2


print(y)
z = y * y * 3

print(z)

out = z.mean()
print(out)

out.backward()
print(x.grad)


# 手动计算验证
manual_grad = 1.5 * (x.data + 2)
print("手动计算的梯度 =", manual_grad)
print("是否一致 =", torch.allclose(x.grad, manual_grad))