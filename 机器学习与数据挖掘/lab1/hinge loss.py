import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import StandardScaler

# 步骤 2: 定义模型
def linear_svm(features, labels, learning_rate, C, num_epochs):
    # 初始化权重向量W和偏置项b
    W = np.zeros(features.shape[1])
    b = 0
    # 训练模型
    for epoch in range(num_epochs):
        for i, x in enumerate(features):
            # 计算预测值
            y_pred = np.dot(W, x) + b

            # 计算Hinge Loss
            loss = max(0, 1 - labels[i] * y_pred)

            # 计算梯度
            if loss > 0:
                dW = -C * labels[i] * x
                db = -C * labels[i]
            else:
                dW = 0
                db = 0

            # 更新权重
            W -= learning_rate * dW
            b -= learning_rate * db

    return W,b


# 步骤 4: 预测
def predict(x, W, b):
    y_pred = np.dot(W, x) + b
    if y_pred > 0:
        return 1
    else:
        return -1


# 使用示例
if __name__ == "__main__":
    # 读取训练集和测试集数据
    train_data = pd.read_csv("mnist_01_train.csv")
    X_train = train_data.iloc[:, 1:].values
    y_train = train_data.iloc[:, 0].values
    y_train[y_train == 0] = -1

    test_data = pd.read_csv("mnist_01_test.csv")
    X_test = test_data.iloc[:, 1:].values
    y_test = test_data.iloc[:, 0].values
    y_test[y_test == 0] = -1

    # 数据预处理 - 标准化
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 设置学习率、正则化参数C和迭代次数
    learning_rate = 0.0001
    for C in (0.001, 0.01, 0.1, 1, 10):
        num_epochs = 100

        # 训练模型
        start_time = time.time()
        W, b = linear_svm(X_train, y_train, learning_rate, C, num_epochs)
        end_time = time.time()

        correct_predictions = 0
        for i in range(len(X_train)):
            if predict(X_train[i], W, b) == y_train[i]:
                correct_predictions += 1

        accuracy = correct_predictions / len(X_train)
        print("C =", C)
        print(f"Linear (Hinge Loss) 训练集准确度: {accuracy * 100:.5f}%")

        correct_predictions = 0
        total_samples = len(X_test)
        for i in range(total_samples):
            if predict(X_test[i], W, b) == y_test[i]:
                correct_predictions += 1

        accuracy = correct_predictions / total_samples
        print(f"Linear (Hinge Loss) 测试集准确度: {accuracy * 100:.5f}%")
        print("It takes",end_time- start_time,"s")
# 不做预处理
# Accuracy on the test set: 99.85816%
# 做预处理
# Accuracy on the test set: 99.95272%