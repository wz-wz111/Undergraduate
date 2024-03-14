# 导入所需库
import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import time
import random

# 加载数据集
def load_data(file_path):
    data = pd.read_csv(file_path)
    labels = data.iloc[:, 0].values  # 获取标签列
    features = data.iloc[:, 1:].values /255.0  # 获取特征列并归一化
    return labels, features
# 生成正定矩阵
def generate_positive_definite_covariance_matrix(n_features):
    A = np.random.rand(n_features, n_features)
    covariance_matrix = np.dot(A, A.T)  # 通过 A * A^T 得到对称矩阵
    return covariance_matrix / 21

# 初始化协方差矩阵,分别使用一个对角形式的协方差矩阵，矩阵内的对角值不一定相等
def generate_diag_covariances(n_clusters, n_features):
    covariances = np.array([np.eye(n_features) for _ in range(n_clusters)])
    for i in range(n_clusters):
        diagonal_values = np.random.rand(n_features)  # 生成随机对角元素
        covariances[i] = np.diag(diagonal_values)  # 将随机对角元素构成对角矩阵并赋值给对应的协方差矩阵
    return covariances

# 生成一个对角形式的协方差矩阵，矩阵内的对角值相等
def generate_spherical_covariances(n_features):
    variance = random.random()
    covariance_matrix = np.zeros((n_features, n_features))
    np.fill_diagonal(covariance_matrix, variance)
    return covariance_matrix

def replicate_matrix(matrix, k):
    replicated_matrix = np.repeat(matrix[np.newaxis, :, :], k, axis=0)
    return replicated_matrix
# 初始化均值
def kmeans_pp_init(X, k):
    centers = [X[np.random.randint(0, len(X))]]

    for _ in range(1, k):
        distances = cdist(X, centers, 'euclidean')
        min_distances = np.min(distances, axis=1)
        weights = min_distances / np.sum(min_distances)
        next_center = X[np.random.choice(range(len(X)), p=weights)]
        centers.append(next_center)

    return np.array(centers)

# 初始化GMM模型参数
def initialize_parameters(X, n_clusters):
    n_samples, n_features = X.shape

    # 初始化权重、均值和协方差矩阵
    weights = np.ones(n_clusters) / n_clusters  # 初始化权重为等概率值

    # 初始化均值（K-means）
    means = kmeans_pp_init(X, n_clusters)
    # 随机初始化均值
    # means = X[np.random.choice(range(len(X)), n_clusters, replace=False)]
    # 初始化协方差矩阵为单位矩阵
    # covariances = np.array([np.eye(n_features) * variances for i in range(n_clusters)]
    # ’full’：每个高斯子模型各自拥有一个普通的协方差矩阵
    # covariances = np.array([generate_positive_definite_covariance_matrix(n_features) for i in range(n_clusters)])

    # ’tied’: 所有高斯子模型共用一个普通的协方差矩阵；
    covariances = replicate_matrix(generate_positive_definite_covariance_matrix(n_features), n_clusters)

    # ’spherical’: 每个高斯子模型分别使用一个对角形式的协方差矩阵，矩阵内的对角值相等
    # covariances = np.array([generate_spherical_covariances(n_features) for i in range(n_clusters)])

    # 'diag'：分别使用一个对角形式的协方差矩阵，矩阵内的对角值不一定相等
    # covariances = generate_diag_covariances(n_clusters, n_features)

    return weights, means, covariances

# E步，计算给定数据点属于每个簇的概率
def expectation_step(X, weights, means, covariances):
    n_samples, n_features = X.shape
    n_clusters = len(weights)

    # 初始化概率数组
    probabilities = np.zeros((n_samples, n_clusters))

    # 计算每个数据点属于每个簇的概率
    for k in range(n_clusters):
        probabilities[:, k] = weights[k] * multivariate_normal.pdf(X, mean=means[k], cov=covariances[k])

    # 检查概率数组是否包含无效值，并将其替换为零
    probabilities[np.isnan(probabilities) | np.isinf(probabilities)] = 0

    # 归一化概率数组
    probabilities /= (np.sum(probabilities, axis=1, keepdims=True))

    # 检查概率数组是否包含无效值，并将其替换为零
    probabilities[np.isnan(probabilities) | np.isinf(probabilities)] = 0.1

    return probabilities

# M步，更新模型参数
def maximization_step(X, probabilities):
    n_samples, n_features = X.shape
    n_clusters = probabilities.shape[1]
    # 更新权重
    weights = np.sum(probabilities, axis=0) / n_samples
    # 初始化均值
    means = np.zeros((n_clusters, n_features))
    for k in range(n_clusters):
        # 计算每个簇的均值
        means[k] = np.average(X, axis=0, weights=probabilities[:, k])
    # 初始化协方差矩阵
    covariances = np.zeros((n_clusters, n_features, n_features))
    for k in range(n_clusters):
        diff = X - means[k]
        weighted_diff = np.dot(probabilities[:, k] * diff.T, diff)
        # 计算每个簇的协方差矩阵
        covariances[k] = weighted_diff / np.sum(probabilities[:, k])
        # 加上一个微小对角矩阵，使得协方差矩阵可逆
        small_diag = 1e-6 * np.eye(n_features)
        covariances[k] = covariances[k] + small_diag
    return weights, means, covariances

# 训练GMM模型
def train_gmm(X, n_clusters, n_iterations):
    weights, means, covariances = initialize_parameters(X, n_clusters)  # 初始化参数

    final = np.zeros((X.shape[0],n_clusters))
    dict = np.zeros(n_clusters)
    prev_means = means.copy()  # 保存上一次迭代的均值
    t = 0
    # 迭代训练模型
    for t in range(n_iterations):
        probabilities = expectation_step(X, weights, means, covariances)  # E步
        weights, means, covariances = maximization_step(X, probabilities)  # M步

        # 检查参数的变化情况
        diff = np.mean(np.abs(means - prev_means))
        if diff < 1e-4:  # 设定差异阈值
            print("参数已收敛，停止迭代")
            break

        prev_means = means.copy()  # 更新上一次迭代的均值

        if t == n_iterations - 1:
            final = probabilities

        if t % 2 == 0:
            # 为不同高斯分布附上标签
            pred = np.argmax(probabilities, axis=0)
            for i in range(n_clusters):
                dict[i] = (y_train[pred[i]])
            # 在测试集上进行预测
            probabilities = expectation_step(X_test, weights, means, covariances)  # E步
            predicted_labels = np.argmax(probabilities, axis=1)  # 取概率最大的为预测标签

            # 计算准确率
            accuracy = np.mean([dict[label] for label in predicted_labels] == y_test) * 100
            print("Epoch:", t)
            print("Clustering Accuracy: {:.2f}%".format(accuracy))
            accuracy_list.append(accuracy)

    # 为不同高斯分布附上标签
    pred = np.argmax(final, axis=0)
    for i in range(n_clusters):
        dict[i] = (y_train[pred[i]])

    return weights, means, covariances, dict, t

if __name__ == "__main__":
    # 加载训练集和测试集
    y_train, X_train = load_data("E:\学习资料\大三上\机器学习与数据挖掘\lab3\data\mnist_train.csv")
    y_test, X_test = load_data("E:\学习资料\大三上\机器学习与数据挖掘\lab3\data\mnist_test.csv")

    # 选择主成分
    pca = PCA(n_components=50)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    # 转换为二进制标签，作为GMM的类别
    binary_labels_train = np.zeros((len(y_train), 10))
    binary_labels_train[np.arange(len(y_train)), y_train] = 1

    # 使用GMM模型进行训练
    n_clusters = 10  # GMM簇的数量，与类别数量一致
    n_iterations = 250
    accuracy_list = []
    start_time = time.time()
    weights, means, covariances, dict, epoch = train_gmm(X_train, n_clusters, n_iterations)
    end_time = time.time()
    # 在测试集上进行预测
    # probabilities = expectation_step(X_test, weights, means, covariances)  # E步
    # predicted_labels = np.argmax(probabilities, axis=1)  # 取概率最大的为预测标签

    # 计算准确率
    # accuracy = np.mean([dict[label] for label in predicted_labels] == y_test) * 100
    # accuracy = np.mean(dict[predicted_labels] == y_test) * 100
    print("Max Clustering Accuracy: {:.2f}%".format(max(accuracy_list)))
    print("It costs {:.2f}s".format(end_time-start_time))
    # 绘制accuracy_values的图像
    plt.plot(range(1, epoch + 1,2), accuracy_list, label='Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Test Accuracy over Epochs')
    plt.legend()
    plt.show()


