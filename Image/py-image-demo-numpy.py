# This script creates and displays a horizontal gradient image using NumPy and PIL.
# import numpy as np
# from PIL import Image
#
# w, h = 400, 200
# gradient = np.zeros((h, w, 3), dtype=np.uint8)
#
# for x in range(w):
#     gradient[:, x] = (x % 256, 128, 255 - (x % 256))
#
# img = Image.fromarray(gradient)
# img.show()

# 使用numpy创建一个400x400的RGB图像，用来做背景图片，所以颜色不要太鲜艳，过渡自然，生成一个渐变色的背景
# import numpy as np
# from PIL import Image
#
# # 图像尺寸
# w, h = 400, 400
#
# # 创建空白图像数组
# gradient = np.zeros((h, w, 3), dtype=np.uint8)
#
# import random
#
# # 定义四个角落的颜色 (柔和的颜色)
# colors = [
#     np.array([220, 230, 11]),   # 浅蓝色
#     np.array([90, 220, 210]),   # 浅棕色
#     np.array([210, 134, 220]),  # 浅绿色
#     np.array([68, 220, 230])    # 浅紫色
# ]
# random.shuffle(colors)
# top_left, top_right, bottom_left, bottom_right = colors
#
# # 定义四个角落的颜色 (柔和的颜色)
# # top_left = np.array([220, 230, 11])  # 浅蓝色
# # top_right = np.array([90, 220, 210])  # 浅棕色
# # bottom_left = np.array([210, 134, 220])  # 浅绿色
# # bottom_right = np.array([68, 220, 230])  # 浅紫色
#
# # 对于每个像素，使用双线性插值计算颜色
# for y in range(h):
#     for x in range(w):
#         # 计算归一化坐标 (0到1范围)
#         nx = x / (w - 1)
#         ny = y / (h - 1)
#
#         # 双线性插值公式
#         top = top_left * (1 - nx) + top_right * nx
#         bottom = bottom_left * (1 - nx) + bottom_right * nx
#         color = top * (1 - ny) + bottom * ny
#
#         # 将颜色值设置为整数
#         gradient[y, x] = color.astype(np.uint8)
#
# # 创建并显示图像
# img = Image.fromarray(gradient)
# img.show()

# 使用numpy创建一个400x400的RGB图像，用来做背景图片，所以颜色不要太鲜艳，过渡自然，生成一个渐变色的背景
# import numpy as np
# from PIL import Image
# import random
#
#
# def get_random_gradient_colors():
#     """
#     随机返回一个渐变色组合
#     返回值: 包含4个角落颜色的numpy数组列表
#     """
#     # 柔和的颜色池
#     color_pool = [
#         np.array([245, 222, 179]),  # 浅黄色，米色
#         np.array([255, 228, 196]),  # 浅橙色，类似羊皮纸
#         np.array([240, 248, 255]),  # 爱丽丝蓝
#         np.array([255, 250, 240]),  # 花的白色
#         np.array([253, 245, 230]),  # 海贝壳色
#         np.array([250, 235, 215]),  # 古董白
#         np.array([255, 239, 213]),  # 珊瑚色
#         np.array([255, 228, 225]),  # 薄雾玫瑰
#         np.array([255, 240, 245]),  # 紫罗兰
#         np.array([248, 248, 255]),  # 幽灵白
#         np.array([240, 255, 255]),  # 苍白的绿宝石
#         np.array([255, 182, 193]),  # 浅粉色
#         np.array([173, 216, 230]),  # 浅蓝色
#         np.array([144, 238, 144]),  # 浅绿色
#         np.array([255, 218, 185]),  # 桃色
#         np.array([230, 230, 250]),  # 薰衣草色
#         np.array([255, 255, 224]),  # 浅黄色
#         np.array([255, 228, 181]),  # 鹿皮色
#         np.array([240, 255, 240]),  # 蜜瓜色
#         np.array([255, 245, 238]),  # 海贝色
#     ]
#
#     # 随机选择4个不同的颜色作为四个角落
#     selected_colors = random.sample(color_pool, 4)
#     return selected_colors
#
#
# # 图像尺寸
# w, h = 400, 400
#
# # 创建空白图像数组
# gradient = np.zeros((h, w, 3), dtype=np.uint8)
#
# # 获取随机的四个角落颜色
# colors = get_random_gradient_colors()
# top_left, top_right, bottom_left, bottom_right = colors
#
# # 对于每个像素，使用双线性插值计算颜色
# for y in range(h):
#     for x in range(w):
#         # 计算归一化坐标 (0到1范围)
#         nx = x / (w - 1)
#         ny = y / (h - 1)
#
#         # 双线性插值公式
#         top = top_left * (1 - nx) + top_right * nx
#         bottom = bottom_left * (1 - nx) + bottom_right * nx
#         color = top * (1 - ny) + bottom * ny
#
#         # 将颜色值设置为整数，并确保在0-255范围内
#         gradient[y, x] = np.clip(color, 0, 255).astype(np.uint8)
#
# # 创建并显示图像
# # img = Image.fromarray(gradient)
# # img.show()
#
# # 保存图像到文件
# # 指定保存路径，默认保存到当前目录下的background文件夹
# # 批量生成30个
# import os
# output_dir = "background"
# os.makedirs(output_dir, exist_ok=True)
# for i in range(3):
#     # 每次都生成新的渐变
#     colors = get_random_gradient_colors()
#     top_left, top_right, bottom_left, bottom_right = colors
#     for y in range(h):
#         for x in range(w):
#             nx = x / (w - 1)
#             ny = y / (h - 1)
#             top = top_left * (1 - nx) + top_right * nx
#             bottom = bottom_left * (1 - nx) + bottom_right * nx
#             color = top * (1 - ny) + bottom * ny
#             gradient[y, x] = np.clip(color, 0, 255).astype(np.uint8)
#     img = Image.fromarray(gradient)
#     img.save(os.path.join(output_dir, f"background_{i+1}.png"))
#     print(f"Saved background_{i+1}.png")


import numpy as np
from PIL import Image
import random
import os


def get_random_gradient_colors():
    color_pool = [
        np.array([245, 222, 179]), np.array([255, 228, 196]), np.array([240, 248, 255]),
        np.array([255, 250, 240]), np.array([253, 245, 230]), np.array([250, 235, 215]),
        np.array([255, 239, 213]), np.array([255, 228, 225]), np.array([255, 240, 245]),
        np.array([248, 248, 255]), np.array([240, 255, 255]), np.array([255, 182, 193]),
        np.array([173, 216, 230]), np.array([144, 238, 144]), np.array([255, 218, 185]),
        np.array([230, 230, 250]), np.array([255, 255, 224]), np.array([255, 228, 181]),
        np.array([240, 255, 240]), np.array([255, 245, 238])
    ]
    return random.sample(color_pool, 4)


def create_gradient_fast(w, h, colors):
    """快速生成渐变图像"""
    top_left, top_right, bottom_left, bottom_right = colors

    # 创建坐标网格
    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    X, Y = np.meshgrid(x, y)

    # 矢量化双线性插值
    top = top_left[None, None, :] * (1 - X[:, :, None]) + top_right[None, None, :] * X[:, :, None]
    bottom = bottom_left[None, None, :] * (1 - X[:, :, None]) + bottom_right[None, None, :] * X[:, :, None]
    gradient = top * (1 - Y[:, :, None]) + bottom * Y[:, :, None]

    return np.clip(gradient, 0, 255).astype(np.uint8)


# 批量生成
w, h = 400, 400
output_dir = "background"
os.makedirs(output_dir, exist_ok=True)

# for i in range(30):
#     colors = get_random_gradient_colors()
#     gradient = create_gradient_fast(w, h, colors)
#     img = Image.fromarray(gradient)
#     img.save(os.path.join(output_dir, f"background_{i + 1}.png"))
#     print(f"Saved background_{i + 1}.png")

def get_random_gradient_direction():
    """随机选择渐变方向"""
    directions = [
        'diagonal',  # 对角线
        'horizontal',  # 水平
        'vertical',  # 垂直
        'radial',  # 径向
        'four_corner'  # 四角(原方案)
    ]
    return random.choice(directions)


def create_random_gradient(w, h, colors, direction):
    """根据方向创建不同类型的渐变"""
    if direction == 'horizontal':
        # 水平渐变：左到右
        x = np.linspace(0, 1, w)
        gradient = colors[0][None, :] * (1 - x[:, None]) + colors[1][None, :] * x[:, None]
        return np.tile(gradient[None, :, :], (h, 1, 1))

    elif direction == 'vertical':
        # 垂直渐变：上到下
        y = np.linspace(0, 1, h)
        gradient = colors[0][None, :] * (1 - y[:, None]) + colors[1][None, :] * y[:, None]
        return np.tile(gradient[:, None, :], (1, w, 1))

    elif direction == 'diagonal':
        # 对角线渐变：左上到右下
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        X, Y = np.meshgrid(x, y)
        t = (X + Y) / 2  # 对角线权重
        gradient = colors[0][None, None, :] * (1 - t[:, :, None]) + colors[1][None, None, :] * t[:, :, None]
        return gradient

    elif direction == 'radial':
        # 径向渐变：中心到边缘
        x = np.linspace(-1, 1, w)
        y = np.linspace(-1, 1, h)
        X, Y = np.meshgrid(x, y)
        distance = np.sqrt(X ** 2 + Y ** 2)
        distance = np.clip(distance / np.sqrt(2), 0, 1)  # 归一化
        gradient = colors[0][None, None, :] * (1 - distance[:, :, None]) + colors[1][None, None, :] * distance[
            :, :, None]
        return gradient

    else:  # four_corner
        return create_gradient_fast(w, h, colors)


# 使用示例
for i in range(10):
    colors = get_random_gradient_colors()
    direction = get_random_gradient_direction()
    gradient = create_random_gradient(w, h, colors, direction)
    gradient = np.clip(gradient, 0, 255).astype(np.uint8)

    img = Image.fromarray(gradient)
    img.save(os.path.join(output_dir, f"gradient_{direction}_{i + 1}.png"))
    print(f"Saved gradient_{direction}_{i + 1}.png")
