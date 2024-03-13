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

X_train = X_train.reshape((len(X_train), 3, 32, 32))
X_test = X_test.reshape((len(X_test), 3, 32, 32))

train_set = TensorDataset(X_train, Y_train)
test_set = TensorDataset(X_test, Y_test)

train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
test_loader = DataLoader(test_set, batch_size=64, shuffle=False)


# # 定义模型结构
class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(12)
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(12)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv4 = nn.Conv2d(in_channels=12, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(24)
        self.conv5 = nn.Conv2d(in_channels=24, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn5 = nn.BatchNorm2d(24)
        self.fc1 = nn.Linear(24 * 10 * 10, 10)

    def forward(self, input):
        output = F.relu(self.bn1(self.conv1(input)))
        output = F.relu(self.bn2(self.conv2(output)))
        output = self.pool(output)
        output = F.relu(self.bn4(self.conv4(output)))
        output = F.relu(self.bn5(self.conv5(output)))
        output = output.view(-1, 24 * 10 * 10)
        output = self.fc1(output)

        return output


# Instantiate a neural network model
model = Network()
# 定义模型结构
# class LeNet(nn.Module):
#     def __init__(self):
#         super(LeNet, self).__init__()
#         # 定义卷积层和全连接层
#         self.conv1 = nn.Conv2d(3, 6, kernel_size=5, stride=1)
#         self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
#         self.conv2 = nn.Conv2d(6, 16, kernel_size=5, stride=1)
#         self.conv3 = nn.Conv2d(16, 120, kernel_size=5, stride=1)
#         self.fc1 = nn.Linear(120, 84)
#         self.fc2 = nn.Linear(84, 10)
#
#     def forward(self, x):
#         x = self.pool(torch.relu(self.conv1(x)))
#         x = self.pool(torch.relu(self.conv2(x)))
#         x = torch.relu(self.conv3(x))
#         x = x.view(-1, 120)
#         x = torch.relu(self.fc1(x))
#         x = self.fc2(x)
#         return x
#
#
# model = LeNet()
criterion = nn.CrossEntropyLoss()  # 交叉熵损失函数
# optimizer = optim.SGD(model.parameters(), lr=0.001)
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
# 将SGD优化器替换为Adam优化器
# optimizer = optim.Adam(model.parameters(), lr=0.001)


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