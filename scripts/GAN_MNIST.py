import subprocess
import os

# 获取当前进程的 PID
pid = os.getpid()

# 使用 perf 记录内存和缓存的访问事件
# perf_command = ["perf", "record", "-e", "mem_inst_retired.all_loads,mem_inst_retired.all_stores,L1-dcache-loads,L1-dcache-stores,L1-dcache-misses,user_time,system_time",
#                 "-c", "50000",
#                 "-p", str(pid), 
#                 "-o", "perf_output.data"
#                 ]
# perf_process = subprocess.Popen(perf_command)


import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# 设置随机种子，确保结果可重复
torch.manual_seed(42)

# 设备配置
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")

# MNIST数据集
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))  # 将像素值范围从[0, 1]转到[-1, 1]
])

# 加载数据集
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

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
            nn.Tanh()  # 输出到[-1, 1]区间
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
            nn.Sigmoid()  # 输出[0, 1]表示真假
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
criterion = nn.BCELoss()  # 二元交叉熵损失
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

        # 真实图像
        real_labels = torch.full((batch_size,), real_label, device=device).float()  # 转换为 float 类型
        output = discriminator(imgs)
        err_d_real = criterion(output.view(-1), real_labels)
        err_d_real.backward()

        # 假图像
        noise = torch.randn(batch_size, latent_dim, device=device)
        fake_imgs = generator(noise)
        fake_labels = torch.full((batch_size,), fake_label, device=device).float()  # 转换为 float 类型
        output = discriminator(fake_imgs.detach())  # 不计算梯度
        err_d_fake = criterion(output.view(-1), fake_labels)
        err_d_fake.backward()

        optimizer_d.step()

        # 训练生成器
        generator.zero_grad()

        output = discriminator(fake_imgs)
        err_g = criterion(output.view(-1), real_labels)  # 生成器希望判别器认为假图像为真
        err_g.backward()

        optimizer_g.step()

        # 输出日志
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

# 训练完成后停止 perf
perf_process.terminate()