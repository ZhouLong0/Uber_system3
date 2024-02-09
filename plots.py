import matplotlib.pyplot as plt
import numpy as np

# Data
num_taxis_list = [5, 10, 20, 50, 100,]
welfare_list = [59.2, 84.9, 38.35, 11.62, 5.21]
delivery_time_list = [3149, 2531, 2020, 1846,1703]

# Create bar plot for welfare
plt.figure(figsize=(10, 5))
bar_width = 0.35
r1 = np.arange(len(num_taxis_list))
plt.bar(r1, welfare_list, color='b', width=bar_width, edgecolor='grey', label='Welfare')

# Display numbers on top of bars for welfare
for i in range(len(num_taxis_list)):
    plt.text(x=i, y=welfare_list[i] + 0.5, s=str(welfare_list[i]), ha='center')

plt.xlabel('Number of Taxis', fontweight='bold')
plt.ylabel('Welfare', fontweight='bold')
plt.title('Welfare vs. Number of Taxis')
plt.xticks(r1, num_taxis_list)
plt.legend()
plt.show()

# Create bar plot for delivery time
plt.figure(figsize=(10, 5))
r2 = np.arange(len(num_taxis_list))
plt.bar(r2, delivery_time_list, color='r', width=bar_width, edgecolor='grey', label='Delivery Time')

# Display numbers on top of bars for delivery time
for i in range(len(num_taxis_list)):
    plt.text(x=i, y=delivery_time_list[i] + 0.5, s=str(delivery_time_list[i]), ha='center')

plt.xlabel('Number of Taxis', fontweight='bold')
plt.ylabel('Delivery Time', fontweight='bold')
plt.title('Delivery Time vs. Number of Taxis')
plt.xticks(r2, num_taxis_list)
plt.legend()
plt.show()
