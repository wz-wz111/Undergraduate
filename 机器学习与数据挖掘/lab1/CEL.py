import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import StandardScaler

# 定义交叉熵损失函数
def cross_entropy_loss(y, y_pred):
    epsilon = 1e-15  # 用于避免对数函数中的除零错误
    loss = - (y * np.log(y_pred + epsilon) + (1 - y) * np.log(1 - y_pred + epsilon))
    return np.mean(loss)


# 训练模型
def train(X, y, learning_rate, num_epochs):
    num_features = X.shape[1]
    w = np.zeros(num_features)
    b = 0
    for epoch in range(num_epochs):
        y_pred = predict(X, w, b)
        loss = cross_entropy_loss(y, y_pred)

        # 计算梯度
        dw = np.dot(X.T, (y_pred - y)) / len(y)
        db = np.mean(y_pred - y)

        # 更新参数
        w -= learning_rate * dw
        b -= learning_rate * db

        if epoch % 100 == 0:
            print(f'Epoch {epoch}, Loss: {loss}')
    return w, b

# 定义预测函数
def predict(X, w, b):
    z = np.dot(X, w) + b
    y_pred = 1 / (1 + np.exp(-z))  # 使用sigmoid函数进行二分类预测
    return y_pred

if __name__ == "__main__":
    # 读取训练集和测试集数据
    train_data = pd.read_csv("mnist_01_train.csv")
    X_train = train_data.iloc[:, 1:].values
    y_train = train_data.iloc[:, 0].values
    # y_train[y_train == 0] = -1

    test_data = pd.read_csv("mnist_01_test.csv")
    X_test = test_data.iloc[:, 1:].values
    y_test = test_data.iloc[:, 0].values
    # y_test[y_test == 0] = -1

    # 数据预处理 - 标准化
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 设置学习率和训练轮数
    learning_rate = 0.01
    num_epochs = 800

    # 训练模型
    start_time = time.time()
    W, b = train(X_train, y_train, learning_rate, num_epochs)
    end_time = time.time()

    # 进行预测
    correct_predictions = 0
    x_predict = predict(X_train, W, b)
    for i in range(len(X_train)):
        label = x_predict[i]
        if label > 0.5:
            label = 1
        else:
            label = 0
        if label == y_train[i]:
            correct_predictions = correct_predictions + 1
    accuracy = correct_predictions / len(X_train)
    print(f"Linear (cross-entropy) 训练集准确度: {accuracy * 100:.5f}%")

    correct_predictions = 0
    total_samples = len(X_test)
    x_predict = predict(X_test, W, b)
    for i in range(total_samples):
        label = x_predict[i]
        if label > 0.5:
            label = 1
        else:
            label = 0
        if label == y_test[i]:
            correct_predictions = correct_predictions + 1

    accuracy = correct_predictions / total_samples
    print(f"Linear (cross-entropy) 测试集准确度: {accuracy * 100:.5f}%")
    print("It takes", end_time - start_time, "s")
# 不做预处理
# Accuracy on the test set: 99.95272%
# 做预处理
# Accuracy on the test set: 99.95272%