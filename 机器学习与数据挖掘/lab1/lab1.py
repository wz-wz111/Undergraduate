import pandas as pd
import time
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

# 读取训练集数据
train_data = pd.read_csv("mnist_01_train.csv")
X_train = train_data.iloc[:, 1:].values
y_train = train_data.iloc[:, 0].values

# 读取测试集数据
test_data = pd.read_csv("mnist_01_test.csv")
X_test = test_data.iloc[:, 1:].values
y_test = test_data.iloc[:, 0].values

# 数据预处理
# fit_transform 用于训练数据，它适应并转换数据，同时计算适应过程中所需的参数。
# transform 用于测试数据或其他未见过的数据，它只应用之前在训练数据上计算的参数，以保持数据的一致性。
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
for c in (0.001,0.01,0.1,1,10,100):
    # 训练SVM分类器（线性核函数）
    start_time = time.time()
    linear_svm = svm.SVC(kernel='linear',C = c)
    linear_svm.fit(X_train, y_train)
    y_pred_linear = linear_svm.predict(X_test)
    end_time = time.time()

    # 计算线性SVM分类器的准确度
    y_train_pred_linear = linear_svm.predict(X_train)
    linear_svm_train_accuracy = accuracy_score(y_train, y_train_pred_linear)
    print("C =",c)
    print("Linear SVM 训练集准确度: {:.5f}%".format(linear_svm_train_accuracy * 100))
    linear_accuracy = accuracy_score(y_test, y_pred_linear)
    print("Linear SVM 测试集准确度: {:.5f}%".format(linear_accuracy * 100))
    print("Linear SVM takes",end_time- start_time,"s")

# # 训练SVM分类器（高斯核函数）
for c in (0.001,0.01,0.1,1,10):
    start_time = time.time()
    rbf_svm = svm.SVC(kernel='rbf',C=c)
    rbf_svm.fit(X_train, y_train)
    y_pred_rbf = rbf_svm.predict(X_test)
    end_time = time.time()

    # 计算高斯SVM分类器的准确度
    y_train_pred_rbf = rbf_svm.predict(X_train)
    gaussian_svm_train_accuracy = accuracy_score(y_train_pred_rbf, y_train)
    print("C =", c)
    print("RBF SVM 训练集准确度: {:.5f}%".format(gaussian_svm_train_accuracy * 100))
    rbf_accuracy = accuracy_score(y_test, y_pred_rbf)
    print("RBF SVM 测试集准确度: {:.5f}%".format(rbf_accuracy * 100))
    print("RBF SVM takes",end_time- start_time,"s")
#
# # 手动实现线性分类模型（Hinge Loss）
# linear_classifier = SGDClassifier(loss='hinge', max_iter=1000, random_state=42)
# linear_classifier.fit(X_train, y_train)
# y_pred_linear_manual = linear_classifier.predict(X_test)
# linear_manual_accuracy = accuracy_score(y_test, y_pred_linear_manual)
# print("Linear (Hinge Loss) Accuracy: {:.5f}%".format(linear_manual_accuracy * 100))
#
#
# # 手动实现线性分类模型（Cross-Entropy Loss）
# cross_entropy_classifier = SGDClassifier(loss='log', max_iter=1000, random_state=42)
# cross_entropy_classifier.fit(X_train, y_train)
# y_pred_cross_entropy_manual = cross_entropy_classifier.predict(X_test)
# cross_entropy_manual_accuracy = accuracy_score(y_test, y_pred_cross_entropy_manual)
# print("Linear (Cross-Entropy Loss) Accuracy: {:.5f}%".format(cross_entropy_manual_accuracy * 100))

# 不做预处理
# Linear SVM 训练集准确度: 100.00000%
# Linear SVM 测试集准确度: 99.90544%
# RBF SVM 训练集准确度: 99.99210%
# RBF SVM 测试集准确度: 99.95272%
# Linear (Hinge Loss) Accuracy: 99.90544%
# Linear (Cross-Entropy Loss) Accuracy: 99.95272%


