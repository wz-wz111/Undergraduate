import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import time
import matplotlib.pyplot as plt

# 加载数据
def load_data(dir):
    import pickle
    import numpy as np
    X_train = []
    Y_train = []
    for i in range(1, 6):
        with open(dir + r'/data_batch_' + str(i), 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        X_train.append(dict[b'data'])
        Y_train += dict[b'labels']
    X_train = np.concatenate(X_train, axis=0)
    with open(dir + r'/test_batch', 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    X_test = dict[b'data']
    Y_test = dict[b'labels']
    return X_train, Y_train, X_test, Y_test

def predict():
    # 在测试集上评估模型性能
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy_values.append((100 * correct / total))
    print(f'Accuracy of the network on the test images: {100 * correct / total}%')

X_train, Y_train, X_test, Y_test = load_data(r'E:\学习资料\机器学习与数据挖掘\lab2\data')

X_train = torch.tensor(X_train / 255.0, dtype=torch.float32)  # 将数据类型转换为float32
X_test = torch.tensor(X_test / 255.0, dtype=torch.float32)  # 将数据类型转换为float32
Y_train = torch.tensor(Y_train)
Y_test = torch.tensor(Y_test)

X_train = X_train.reshape((len(X_train), 32, 32, 3)).permute(0, 3, 1, 2)
X_test = X_test.reshape((len(X_test), 32, 32, 3)).permute(0, 3, 1, 2)

train_set = TensorDataset(X_train, Y_train)
test_set = TensorDataset(X_test, Y_test)

train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
test_loader = DataLoader(test_set, batch_size=64, shuffle=False)

# 构建多层感知机（MLP）模型
# class MLP(nn.Module):
#     def __init__(self):
#         super(MLP, self).__init__()
#         self.fc1 = nn.Linear(32*32*3, 128)  # 输入层到第一个隐藏层
#         self.fc2 = nn.Linear(128, 64)  # 第一个隐藏层到第二个隐藏层
#         self.fc3 = nn.Linear(64, 10)  # 第二个隐藏层到输出层
#
#     def forward(self, x):
#         x = x.view(-1, 32*32*3)  # 将输入数据展开成一维向量
#         x = F.relu(self.fc1(x))  # 第一个隐藏层（使用ReLU激活函数）
#         x = F.relu(self.fc2(x))  # 第二个隐藏层（使用ReLU激活函数）
#         x = self.fc3(x)  # 输出层
#         return x
class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(32*32*3, 128)  # 输入层到第一个隐藏层
        self.fc2 = nn.Linear(128, 10)  # 第一个隐藏层到第二个隐藏层
        # self.fc3 = nn.Linear(64, 10)  # 第二个隐藏层到输出层

    def forward(self, x):
        x = x.view(-1, 32*32*3)  # 将输入数据展开成一维向量
        x = F.relu(self.fc1(x))  # 第一个隐藏层（使用ReLU激活函数）
        # x = F.relu(self.fc2(x))  # 第二个隐藏层（使用ReLU激活函数）
        x = self.fc2(x)  # 输出层
        return x
# class MLP(nn.Module):
#     def __init__(self):
#         super(MLP, self).__init__()
#         self.fc1 = nn.Linear(32*32*3, 128)  # 输入层到第一个隐藏层
#         self.fc2 = nn.Linear(128, 64)  # 第一个隐藏层到第二个隐藏层
#         self.fc3 = nn.Linear(64, 10)  # 第二个隐藏层到输出层
#
#     def forward(self, x):
#         x = x.view(-1, 32*32*3)  # 将输入数据展开成一维向量
#         x = F.relu(self.fc1(x))  # 第一个隐藏层（使用ReLU激活函数）
#         x = F.relu(self.fc2(x))  # 第二个隐藏层（使用ReLU激活函数）
#         x = self.fc3(x)  # 输出层
#         return x

# 初始化模型、损失函数和优化器
model = MLP()
criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数
# optimizer = optim.SGD(model.parameters(), lr=0.001)
# optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
# 将SGD优化器替换为Adam优化器
optimizer = optim.Adam(model.parameters(), lr=0.001)


# 训练模型
loss_values = []
accuracy_values = []
start_time = time.time()
num_epochs = 50
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)
    epoch_loss = running_loss / len(train_loader.dataset)
    loss_values.append(epoch_loss)
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {epoch_loss:.4f}')
    predict()

end_time = time.time()
print(f'The max accuracy of the network on the test images: {max(accuracy_values)}%')
print("It takes", end_time - start_time, 's')

# 绘制epoch_loss的图像
plt.plot(range(1, num_epochs+1), loss_values, label='Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss over Epochs')
plt.legend()
plt.show()

# 绘制accuracy_values的图像
plt.plot(range(1, num_epochs+1), accuracy_values, label='Test Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.title('Test Accuracy over Epochs')
plt.legend()
plt.show()