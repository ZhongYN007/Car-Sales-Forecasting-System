import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error
from math import sqrt

# 读取数据，假设数据集中有两列：日期（date）和销售量（sales）
# 注意：数据应该是按照时间顺序排列的
data = pd.read_csv('car_sales_data.csv')

data['date'] = pd.to_datetime(data['date'])
print(data)
data.set_index('date', inplace=True)
sales = data['sales'].values.reshape(-1, 1)

# 将销售数据进行归一化
scaler = MinMaxScaler(feature_range=(0, 1))
sales_normalized = scaler.fit_transform(sales)

# 创建训练数据集和测试数据集
train_size = int(len(sales_normalized) * 0.8)
train_data, test_data = sales_normalized[0:train_size, :], sales_normalized[train_size:len(sales_normalized), :]


# 将时间序列数据转换为监督学习问题
def create_dataset(dataset, time_steps=1):
    data_x, data_y = [], []
    for i in range(len(dataset) - time_steps):
        a = dataset[i:(i + time_steps), 0]
        data_x.append(a)
        data_y.append(dataset[i + time_steps, 0])
    return np.array(data_x), np.array(data_y)


time_steps = 12  # 假设使用过去 12 个月的销售数据来预测下个月的销量
train_x, train_y = create_dataset(train_data, time_steps)
test_x, test_y = create_dataset(test_data, time_steps)

# 将数据重塑为 LSTM 输入的 3D 格式 [样本数, 时间步数, 特征数]
train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))

# 构建 LSTM 模型
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(train_x.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型
model.fit(train_x, train_y, epochs=50, batch_size=32, validation_data=(test_x, test_y), verbose=2)

# 使用模型进行预测
train_predict = model.predict(train_x)
test_predict = model.predict(test_x)

# 反归一化预测结果
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

# 反归一化真实销售数据
train_original = scaler.inverse_transform([train_y])
test_original = scaler.inverse_transform([test_y])

# 计算训练集和测试集上的均方根误差（Root Mean Squared Error，RMSE）
train_score = sqrt(mean_squared_error(train_original[0], train_predict[:, 0]))
test_score = sqrt(mean_squared_error(test_original[0], test_predict[:, 0]))

# 可视化预测结果
train_plot = np.empty_like(sales_normalized)
train_plot[:, :] = np.nan
train_plot[time_steps:len(train_predict) + time_steps, :] = train_predict

test_plot = np.empty_like(sales_normalized)
test_plot[:, :] = np.nan
test_plot[len(train_predict) + (time_steps * 2):len(sales_normalized), :] = test_predict

plt.plot(scaler.inverse_transform(sales_normalized), label='Actual Sales')
plt.plot(train_plot, label='Training Predictions')
plt.plot(test_plot, label='Testing Predictions')
plt.title('LSTM Model for Sales Prediction')
plt.legend()
plt.show()

print(f"Training RMSE: {train_score}")
print(f"Testing RMSE: {test_score}")
