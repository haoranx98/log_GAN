
import subprocess
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset
import matplotlib.pyplot as plt
# import psutil

# 限制 PyTorch 只使用 8 个线程
# torch.set_num_threads(8)

# 绑定到 8 个 P-Core 线程
# big_cores = [0, 2, 4, 6, 8, 10, 12, 14]
# psutil.Process().cpu_affinity(big_cores)
# print(f"PyTorch 运行时绑定的 CPU 核心: {big_cores}")

# 获取当前进程的 PID
# pid = os.getpid()

# 设置随机种子，确保结果可重复
torch.manual_seed(42)

# 设备配置
device = torch.device("cpu")
print("使用 CPU 运行代码...")
# MNIST数据集转换
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # 归一化到[-1, 1]
])

print("正在加载 MNIST 数据集...")

# 加载完整数据集
full_train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
full_test_dataset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)

print("MNIST 数据集加载完成！")

print("正在创建 DataLoader...")
# 只使用前 30 张训练图片和前 10 张测试图片
train_dataset = Subset(full_train_dataset, range(30))
test_dataset = Subset(full_test_dataset, range(10))

# 创建 DataLoader
train_loader = DataLoader(train_dataset, batch_size=10, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=10, shuffle=False)

print("DataLoader 创建完成！")
print(f"训练集大小: {len(train_dataset)} 张图片")
print(f"测试集大小: {len(test_dataset)} 张图片")

# Generator网络
class Generator(nn.Module):
    def __init__(self, latent_dim):
        super(Generator, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(True),
            nn.Linear(256, 512),
            nn.ReLU(True),
            nn.Linear(512, 1024),
            nn.ReLU(True),
            nn.Linear(1024, 28*28),
            nn.Tanh()
        )

    def forward(self, z):
        return self.fc(z).view(-1, 1, 28, 28)

# Discriminator网络
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(28*28, 1024),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(1024, 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.fc(x.view(-1, 28*28))

# 超参数
latent_dim = 100
lr = 0.0002
beta1 = 0.5

# 创建生成器和判别器
generator = Generator(latent_dim).to(device)
discriminator = Discriminator().to(device)

# 损失函数和优化器
criterion = nn.BCELoss()
optimizer_g = optim.Adam(generator.parameters(), lr=lr, betas=(beta1, 0.999))
optimizer_d = optim.Adam(discriminator.parameters(), lr=lr, betas=(beta1, 0.999))

# 训练GAN
num_epochs = 10
real_label = 1
fake_label = 0

for epoch in range(num_epochs):
    for i, (imgs, _) in enumerate(train_loader):
        batch_size = imgs.size(0)
        imgs = imgs.to(device)

        # 训练判别器
        discriminator.zero_grad()
        real_labels = torch.full((batch_size,), real_label, device=device).float()
        output = discriminator(imgs)
        err_d_real = criterion(output.view(-1), real_labels)
        err_d_real.backward()

        # 生成假图像
        noise = torch.randn(batch_size, latent_dim, device=device)
        fake_imgs = generator(noise)
        fake_labels = torch.full((batch_size,), fake_label, device=device).float()
        output = discriminator(fake_imgs.detach())
        err_d_fake = criterion(output.view(-1), fake_labels)
        err_d_fake.backward()
        optimizer_d.step()

        # 训练生成器
        generator.zero_grad()
        output = discriminator(fake_imgs)
        err_g = criterion(output.view(-1), real_labels)
        err_g.backward()
        optimizer_g.step()

        if i % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i}/{len(train_loader)}], '
                  f'D Loss: {err_d_real.item() + err_d_fake.item():.4f}, G Loss: {err_g.item():.4f}')

    # 保存生成的图片
    if (epoch+1) % 10 == 0:
        with torch.no_grad():
            fake_imgs = generator(torch.randn(64, latent_dim, device=device))
            fake_imgs = fake_imgs.detach().cpu()
            grid = torchvision.utils.make_grid(fake_imgs, nrow=8, normalize=True)
            plt.imshow(grid.permute(1, 2, 0))
            plt.axis('off')
            plt.savefig(f'gan_generated_epoch_{epoch+1}.png')
            plt.close()

print("Training Finished!")
