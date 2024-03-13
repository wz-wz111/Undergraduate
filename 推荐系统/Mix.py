import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# 预测挖去内容的评分(一个用户对应一个物品的评分）
def predict_rating(similarity, ratings_matrix, user_id, item_id, k):
    sim_scores = similarity[item_id].dropna()  # 获取与目标物品的相似度
    item_ratings = ratings_matrix[user_id].dropna()  # 获取目标用户的评分

    # 获取相似度中在item_ratings中存在的索引
    valid_indices = sim_scores.index.isin(item_ratings.index)

    # 筛选出在item_ratings中存在的相似度
    valid_sim_scores = sim_scores[valid_indices]

    # 选择前k个最大的值
    top_k = valid_sim_scores.nlargest(k)
    sum_sim_scores = 0
    weighted_sum = 0

    for item in top_k.index:   # item--物品id
        if item != item_id and item in item_ratings.index:
            similarity = top_k[item]
            rating = ratings_matrix.loc[item, user_id]
            if similarity <= 0:
                break
            if pd.notnull(rating):
                weighted_sum += similarity * rating
                sum_sim_scores += similarity

    if sum_sim_scores != 0:
        predicted_rating = weighted_sum / sum_sim_scores
    else:
        predicted_rating = np.nan

    return predicted_rating

# 计算RMSE(忽略Nan）
def calculate_rmse(real_matrix, predicted_matrix):
    # 将DataFrame对象转换为NumPy数组
    real_matrix = real_matrix.to_numpy()
    predicted_matrix = np.array(predicted_matrix)

    # 计算非NaN元素的均方误差
    mask = ~np.isnan(real_matrix) & ~np.isnan(predicted_matrix)
    mse = np.mean((real_matrix[mask] - predicted_matrix[mask]) ** 2)
    rmse = np.sqrt(mse)

    return rmse

# 计算coverage
def calculate_coverage(predicted_matrix):
    total_elements = np.size(predicted_matrix)  # 计算总元素数量
    non_nan_elements = np.count_nonzero(~np.isnan(predicted_matrix))  # 计算非 NaN 值的数量
    coverage = non_nan_elements / total_elements  # 计算非 NaN 值的占比
    return coverage


# 预测评分并计算RMSE
def evaluate_model(similarity, ratings_matrix, real_matrix, k):
    predicted_matrix = []  # 存储预测评分矩阵的列表

    test_row = len(real_matrix)
    test_col = len(real_matrix.columns)
    for i in range(test_row):
        predicted_rating = []
        for j in range(test_col):
            item_id = real_matrix.index[i]
            user_id = real_matrix.columns[j]
            rating = predict_rating(similarity, ratings_matrix, user_id, item_id, k)  # 使用相似度和评分矩阵预测评分
            predicted_rating.append(rating)
        predicted_matrix.append(predicted_rating)  # 将每个用户的预测评分列表添加到预测评分矩阵中

    # 计算真实评分矩阵和预测评分矩阵之间的RMSE
    rmse = calculate_rmse(real_matrix,predicted_matrix)

    # 计算覆盖率
    coverage = calculate_coverage(predicted_matrix)

    return rmse, coverage


if __name__ == "__main__":
    # 读取评分数据
    data = pd.read_csv(r'E:\学习资料\大三上\机器学习与数据挖掘\大作业\src\ml-latest-small\ratings.csv')

    # 读取电影数据
    movies = pd.read_csv(r'E:\学习资料\大三上\机器学习与数据挖掘\大作业\src\ml-latest-small\movies.csv')

    # 创建用户-物品评分矩阵
    # ratings_matrix = data.pivot_table(index='userId', columns='movieId', values='rating')
    ratings_matrix = data.pivot_table(index='movieId', columns='userId', values='rating')

    # 计算要提取的行和列范围
    # test_rate = 0.05
    # num_rows = len(ratings_matrix)
    # num_cols = len(ratings_matrix.columns)
    # rows_to_extract = int(num_rows * test_rate)
    # cols_to_extract = int(num_cols * test_rate)
    rows_to_extract = 300
    cols_to_extract = 100

    # 提取部分行和列来测试
    real_matrix = ratings_matrix.iloc[:rows_to_extract, :cols_to_extract]
    real_matrix = real_matrix.copy()
    ratings_matrix.iloc[:rows_to_extract, :cols_to_extract] = np.nan

    # 计算电影之间的相似度（使用电影的标题和类型）
    tfidf = TfidfVectorizer(stop_words='english')
    movies['genres'] = movies['genres'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # 计算电影之间的相似度
    similarity = pd.DataFrame(cosine_sim, index=movies['movieId'], columns=movies['movieId'])

    # 选取前k个相似度最大的用户/项
    k_list = list(range(5, 100, 5))
    coverage_list = []
    rmse_list = []
    start_time = time.time()
    # 计算评价指标
    for i in range(len(k_list)):
        rmse, coverage = evaluate_model(similarity, ratings_matrix, real_matrix, k_list[i])
        coverage_list.append(coverage)
        rmse_list.append(rmse)
        print(f"For k={k_list[i]}, RMSE={rmse}, Coverage: {coverage*100}%")

    end_time = time.time()
    print("It costs", end_time - start_time, "s")

    plt.plot(k_list, rmse_list, marker='o')
    plt.title('Mix')
    plt.xlabel('k')
    plt.ylabel('RMSE')
    plt.show()

    plt.plot(k_list, coverage_list, marker='o')
    plt.title('Mix')
    plt.xlabel('k')
    plt.ylabel('Coverage')
    plt.show()
