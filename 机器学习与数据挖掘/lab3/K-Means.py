import numpy as np
from scipy.spatial.distance import cdist
import pandas as pd
import time
import matplotlib.pyplot as plt

def load_data(file_path):
    data = pd.read_csv(file_path)
    labels = data.iloc[:, 0].values
    features = data.iloc[:, 1:].values / 255.0  # 对特征值进行归一化
    return labels, features

def kmeans(X, Y, k, max_iterations=100):
    # 随机选择k个中心点
    # centers = X[np.random.choice(range(len(X)), k, replace=False)]

    # 初始化方法2
    centers = kmeans_pp_init(X,k)

    for t in range(max_iterations):
        # 计算样本到每个中心点的距离
        distances = cdist(X, centers, 'euclidean')

        # 找到每个样本对应的最近的中心点
        labels = np.argmin(distances, axis=1)

        # 更新中心点的位置
        new_centers = np.array([X[labels == i].mean(axis=0) for i in range(k)])

        # 判断中心点是否变化不大，如果不变化则停止迭代
        if np.all(centers == new_centers):
            break

        centers = new_centers
        if t % 10 == 0:
            matrix = np.zeros((k, 10))
            distances = cdist(X, centers, 'euclidean')
            y_pred = np.argmin(distances, axis=1)
            for i in range(len(X)):
                matrix[y_pred[i]][Y[i]] += 1
            dict = np.argmax(matrix, axis=1)

            distances = cdist(X_test, centers, 'euclidean')
            y_pred = np.argmin(distances, axis=1)
            accuracy = clustering_accuracy(y_test, y_pred, dict)
            accuracy_list.append(accuracy * 100)
            print("Epoch:", t)
            print("Clustering Accuracy:", accuracy * 100, "%")

    # 给中心点分配标签
    matrix = np.zeros((k, 10))
    distances = cdist(X, centers, 'euclidean')
    y_pred = np.argmin(distances, axis=1)
    for i in range(len(X)):
        matrix[y_pred[i]][Y[i]] += 1
    dict = np.argmax(matrix, axis=1)
    # t是迭代次数
    return centers, t, dict



# 初始化方法：使用k-means++算法进行初始化
def kmeans_pp_init(X, k):
    centers = [X[np.random.randint(0, len(X))]]

    for _ in range(1, k):
        distances = cdist(X, centers, 'euclidean')
        min_distances = np.min(distances, axis=1)
        weights = min_distances / np.sum(min_distances)
        next_center = X[np.random.choice(range(len(X)), p=weights)]
        centers.append(next_center)

    return np.array(centers)


# 聚类性能评价函数：聚类精度(Clustering Accuracy)
def clustering_accuracy(y_true, y_pred, dict):
    n = len(y_true)
    correct = 0

    for i in range(n):
        if y_true[i] == dict[y_pred[i]]:
            correct += 1

    return correct / n


if __name__ == "__main__":

    y_train, X_train = load_data("E:\学习资料\大三上\机器学习与数据挖掘\lab3\data\mnist_train.csv")
    y_test, X_test = load_data("E:\学习资料\大三上\机器学习与数据挖掘\lab3\data\mnist_test.csv")
    k = 50 # 簇类数
    n_runs = 200 # 运行次数
    accuracy_list = []
    strat_time = time.time()
    # 训练模型
    centers, epoch, dict = kmeans(X_train, y_train, k, n_runs)

    # kmeans = KMeans(n_clusters=10, random_state=0)
    # kmeans.fit(X_train)
    # centers = kmeans.cluster_centers_

    # 在测试集上进行预测
    distances = cdist(X_test, centers, 'euclidean')
    y_pred = np.argmin(distances, axis=1)
    end_time = time.time()
    # 计算聚类精度
    accuracy = clustering_accuracy(y_test, y_pred, dict)
    print("Max Clustering Accuracy:", max(accuracy_list), "%")
    print("It takes", end_time - strat_time,"s")

    # 绘制accuracy_values的图像
    plt.plot(range(1, epoch + 1,10), accuracy_list, label='Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Test Accuracy over Epochs')
    plt.legend()
    plt.show()