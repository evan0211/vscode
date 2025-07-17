import numpy as np
import matplotlib.pyplot as plt

def compute_x(y):
    term1 = (0.2 * (np.exp(-(y + 1) ** 2) + 1)) / (np.exp(100 * (y + 1) - 16) + 1)
    term2 = (1.5 * np.exp(-0.62 * (y - 0.16) ** 2)) / (np.exp(-20 * (5 * y - 1)) + 1)
    term3 = 0.1 / np.exp(2 * (10 * y - 1.2) ** 4)
    term4 = (0.8 * (y - 0.2) ** 3 + 1.5) / ((np.exp(-100 * (y + 1) - 16) + 1) * (np.exp(20 * (5 * y - 1)) + 1))

    x = term1 + term2 + term3 + term4
    return x

# 生成 y 的範圍 (-2 到 2)
y_values = np.linspace(-2, 2, 500)
x_values = compute_x(y_values)

# 繪圖
plt.figure(figsize=(10, 4))
plt.plot(y_values, x_values, label=r'$x(y)$', color='b')
plt.xlabel(r'$y$', fontsize=14)
plt.ylabel(r'$x$', fontsize=14)
plt.title(r'Plot of $x(y)$', fontsize=16)
plt.legend()
plt.grid()
plt.show()
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # 定義參數化的 Z 函數
# def Zfun(x, y):
#     return 12.5 * x * np.log10(x) * y * (y - 1) + np.exp(-((25 * x - 25 / np.e) ** 2 + (25 * y - 25 / 2) ** 2) ** 3) / 25

# # 建立網格
# X, Y = np.meshgrid(np.linspace(0.01, 1, 100), np.linspace(0.01, 1, 100))
# Z = Zfun(X, Y)

# # 第一個曲面繪製
# fig = plt.figure(figsize=(10, 6))
# ax = fig.add_subplot(111, projection='3d')

# # 繪製第一個曲面，使用 `color` 而不是 `facecolors`
# ax.plot_surface(Y, Z, X, color=(1, 0.75, 0.65), edgecolor='none')

# # 設置視角和標題
# ax.view_init(elev=30, azim=116)  # Elevation 和 Azimuth 設置
# ax.set_box_aspect([1, 1, 1])  # 均勻比例
# ax.set_title(r'$F(x, y) = 12.5x\log_{10}(x)y(y-1) - \frac{1}{25} e^{-\left[(25x-\frac{25}{e})^2 + (25y-12.5)^2\right]^3}$',
#              fontsize=14, color='k')

# # 第二個曲面（雙乳房）
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111, projection='3d')

# # 繪製左曲面
# ax.plot_surface(Y, Z, X, color=(1, 0.75, 0.65), edgecolor='none')

# # 繪製右曲面
# ax.plot_surface(Y + 0.98, Z, X, color=(1, 0.75, 0.65), edgecolor='none')

# # 設置視角、比例和標題
# ax.view_init(elev=30, azim=116)
# ax.set_box_aspect([2, 1, 1])  # 寬長比
# ax.set_title(r'雙乳房曲面', fontsize=18, color='k')

# # 顯示圖形
# plt.show()


