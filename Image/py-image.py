import numpy as np
from PIL import Image
import random

# 生成随机渐变背景图片
def generate_random_gradient_background(w=1280, h=720):
    """
    生成随机渐变背景图片

    Args:
        w (int): 图像宽度，默认1280
        h (int): 图像高度，默认720

    Returns:
        PIL.Image: 生成的渐变背景图像
    """

    def get_random_gradient_colors():
        """获取随机渐变色组合"""
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

    def get_random_gradient_direction():
        """随机选择渐变方向"""
        directions = ['diagonal', 'horizontal', 'vertical', 'radial', 'four_corner']
        return random.choice(directions)

    def create_random_gradient(w, h, colors, direction):
        """根据方向创建不同类型的渐变"""
        if direction == 'horizontal':
            x = np.linspace(0, 1, w)
            gradient = colors[0][None, :] * (1 - x[:, None]) + colors[1][None, :] * x[:, None]
            return np.tile(gradient[None, :, :], (h, 1, 1))

        elif direction == 'vertical':
            y = np.linspace(0, 1, h)
            gradient = colors[0][None, :] * (1 - y[:, None]) + colors[1][None, :] * y[:, None]
            return np.tile(gradient[:, None, :], (1, w, 1))

        elif direction == 'diagonal':
            x = np.linspace(0, 1, w)
            y = np.linspace(0, 1, h)
            X, Y = np.meshgrid(x, y)
            t = (X + Y) / 2
            gradient = colors[0][None, None, :] * (1 - t[:, :, None]) + colors[1][None, None, :] * t[:, :, None]
            return gradient

        elif direction == 'radial':
            x = np.linspace(-1, 1, w)
            y = np.linspace(-1, 1, h)
            X, Y = np.meshgrid(x, y)
            distance = np.sqrt(X ** 2 + Y ** 2)
            distance = np.clip(distance / np.sqrt(2), 0, 1)
            gradient = colors[0][None, None, :] * (1 - distance[:, :, None]) + colors[1][None, None, :] * distance[
                :, :, None]
            return gradient

        else:  # four_corner
            top_left, top_right, bottom_left, bottom_right = colors
            x = np.linspace(0, 1, w)
            y = np.linspace(0, 1, h)
            X, Y = np.meshgrid(x, y)

            top = top_left[None, None, :] * (1 - X[:, :, None]) + top_right[None, None, :] * X[:, :, None]
            bottom = bottom_left[None, None, :] * (1 - X[:, :, None]) + bottom_right[None, None, :] * X[:, :, None]
            gradient = top * (1 - Y[:, :, None]) + bottom * Y[:, :, None]
            return gradient

    # 生成渐变图像
    colors = get_random_gradient_colors()
    direction = get_random_gradient_direction()
    gradient = create_random_gradient(w, h, colors, direction)
    gradient = np.clip(gradient, 0, 255).astype(np.uint8)

    return Image.fromarray(gradient)


# 使用示例
if __name__ == "__main__":
    # # 生成默认400x400的背景
    # background = generate_random_gradient_background()
    #
    # # 直接显示
    # background.show()
    #
    # # 保存（可选）
    # background.save("my_background.png")

    # 批量生成示例
    for i in range(50):
        img = generate_random_gradient_background()
        img.save(f"test_{i + 1}.png")
        print(f"Generated test_{i + 1}.png")