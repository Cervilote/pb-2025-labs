import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Создаем фигуру и оси
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title('Динамика кривой спроса')
ax.set_xlabel('Количество, Q')
ax.set_ylabel('Цена, P')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.grid(True)

# Начальные параметры кривой спроса: P = a - b*Q
a = 50
b = 1

# Создаем массив значений количества
q = np.linspace(0, 100, 200)


# Функция для расчета цены
def demand_curve(q, a, b):
    return a - b * q


# Функция инициализации анимации
def init():
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title('Динамика кривой спроса')
    ax.set_xlabel('Количество, Q')
    ax.set_ylabel('Цена, P')
    ax.grid(True)
    return []


# Функция анимации для каждого кадра
def animate(frame):
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title('Динамика кривой спроса')
    ax.set_xlabel('Количество, Q')
    ax.set_ylabel('Цена, P')
    ax.grid(True)

    # Изменяем параметры кривой спроса для анимации
    current_a = a + 20 * np.sin(frame * 0.1)  # Колебания спроса
    current_b = 0.5 + 0.5 * np.sin(frame * 0.05)  # Колебания наклона

    # Рассчитываем текущую кривую спроса
    p = demand_curve(q, current_a, current_b)

    # Отображаем кривую спроса
    ax.plot(q, p, 'b-', linewidth=2, label=f'Спрос: P = {current_a:.1f} - {current_b:.1f}Q')
    ax.legend(loc='upper right')

    return []


# Создаем анимацию
ani = FuncAnimation(fig, animate, frames=200, init_func=init, blit=True, interval=50)

# Сохраняем анимацию как GIF
ani.save('dynamic_demand_curve.gif', writer='pillow', fps=20)

plt.tight_layout()
plt.show()