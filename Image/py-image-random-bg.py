import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import os
import math
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
import colorsys


@dataclass
class ImageConfig:
    """图像生成配置类"""
    width: int = 1920
    height: int = 1080
    style: str = 'mixed'
    color_scheme: str = 'pastel'
    noise_intensity: float = 0.01
    blur_radius: float = 0.8
    effects: List[str] = None
    element_density: float = 1.0
    curve_types: List[str] = None

    def __post_init__(self):
        if self.effects is None:
            self.effects = ['gradient', 'bubbles', 'curves', 'particles']
        if self.curve_types is None:
            self.curve_types = ['bezier', 'sine', 'spiral', 'lissajous', 'rose']


class ColorManager:
    """颜色管理器 - 提取自参照文件"""

    # 原有的固定颜色池
    BASE_COLORS = [
        np.array([245, 222, 179]), np.array([255, 228, 196]), np.array([240, 248, 255]),
        np.array([255, 250, 240]), np.array([253, 245, 230]), np.array([250, 235, 215]),
        np.array([255, 239, 213]), np.array([255, 228, 225]), np.array([255, 240, 245]),
        np.array([248, 248, 255]), np.array([240, 255, 255]), np.array([255, 182, 193]),
        np.array([173, 216, 230]), np.array([144, 238, 144]), np.array([255, 218, 185]),
        np.array([230, 230, 250]), np.array([255, 255, 224]), np.array([255, 228, 181]),
        np.array([240, 255, 240]), np.array([255, 245, 238])
    ]

    @classmethod
    def get_gradient_colors(cls, count: int = 4) -> List[np.ndarray]:
        """获取渐变颜色，包含原有颜色和随机生成的柔和背景色"""
        color_pool = cls.BASE_COLORS.copy()

        # 生成2倍数量的随机背景色（适合背景的柔和颜色）
        num_random_colors = len(cls.BASE_COLORS) * 2
        for _ in range(num_random_colors):
            # 生成柔和的背景色：RGB值在180-255范围内，避免太暗、太亮或太鲜艳
            r = random.randint(180, 255)
            g = random.randint(180, 255)
            b = random.randint(180, 255)

            # 确保颜色不会太过鲜艳，通过限制RGB差值来保持柔和
            max_val = max(r, g, b)
            min_val = min(r, g, b)
            if max_val - min_val > 60:  # 如果差值太大，调整到更接近的值
                avg = (r + g + b) // 3
                r = random.randint(max(180, avg - 30), min(255, avg + 30))
                g = random.randint(max(180, avg - 30), min(255, avg + 30))
                b = random.randint(max(180, avg - 30), min(255, avg + 30))

            color_pool.append(np.array([r, g, b]))

        return random.sample(color_pool, count)

    @classmethod
    def random_color_rgba(cls, alpha_range: Tuple[int, int] = (10, 50)) -> Tuple[int, int, int, int]:
        """生成随机RGBA颜色"""
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        a = random.randint(*alpha_range)
        return (r, g, b, a)


class GradientGenerator:
    """渐变生成器 - 提取自参照文件并扩展"""

    @staticmethod
    def get_random_direction():
        """随机选择渐变方向"""
        directions = [
            'diagonal', 'diagonal_reverse', 'horizontal', 'vertical', 'radial',
            'radial_square', 'radial_ellipse', 'wave_horizontal', 'wave_vertical',
            'spiral', 'diamond', 'cross', 'triangle', 'four_corner', 'multi_radial', 'conic'
        ]
        return random.choice(directions)

    @staticmethod
    def create_gradient(w: int, h: int, colors: List[np.ndarray], direction: str = None) -> np.ndarray:
        """根据方向创建不同类型的渐变"""
        if direction is None:
            direction = GradientGenerator.get_random_direction()

        if len(colors) < 2:
            colors = colors * 2
        if len(colors) < 4:
            colors = colors + colors[:4-len(colors)]

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
            t = (X + Y) / 2
            gradient = colors[0][None, None, :] * (1 - t[:, :, None]) + colors[1][None, None, :] * t[:, :, None]
            return gradient

        elif direction == 'radial':
            # 径向渐变：中心到边缘
            x = np.linspace(-1, 1, w)
            y = np.linspace(-1, 1, h)
            X, Y = np.meshgrid(x, y)
            distance = np.sqrt(X ** 2 + Y ** 2)
            distance = np.clip(distance / np.sqrt(2), 0, 1)
            gradient = colors[0][None, None, :] * (1 - distance[:, :, None]) + colors[1][None, None, :] * distance[:, :, None]
            return gradient

        else:  # four_corner - 默认四角渐变
            top_left, top_right, bottom_left, bottom_right = colors[:4]
            x = np.linspace(0, 1, w)
            y = np.linspace(0, 1, h)
            X, Y = np.meshgrid(x, y)

            top = top_left[None, None, :] * (1 - X[:, :, None]) + top_right[None, None, :] * X[:, :, None]
            bottom = bottom_left[None, None, :] * (1 - X[:, :, None]) + bottom_right[None, None, :] * X[:, :, None]
            gradient = top * (1 - Y[:, :, None]) + bottom * Y[:, :, None]
            return gradient


class CurveGenerator:
    """数学曲线生成器 - 提取自参照文件"""

    @staticmethod
    def bezier_curve(p0, p1, p2, p3, num_points=100):
        """三次贝塞尔曲线"""
        t = np.linspace(0, 1, num_points)
        curve = np.outer((1 - t) ** 3, p0) + \
                3 * np.outer((1 - t) ** 2 * t, p1) + \
                3 * np.outer((1 - t) * t ** 2, p2) + \
                np.outer(t ** 3, p3)
        return curve

    @staticmethod
    def sine_wave(start_x, start_y, length, amplitude, frequency, num_points=50):
        """正弦波曲线"""
        x = np.linspace(start_x, start_x + length, num_points)
        y = start_y + amplitude * np.sin(frequency * np.linspace(0, 2 * np.pi, num_points))
        return list(zip(x, y))

    @staticmethod
    def spiral(center_x, center_y, max_radius, turns=3, num_points=100):
        """螺旋线"""
        t = np.linspace(0, turns * 2 * np.pi, num_points)
        r = max_radius * t / (turns * 2 * np.pi)
        x = center_x + r * np.cos(t)
        y = center_y + r * np.sin(t)
        return list(zip(x, y))

    @staticmethod
    def lissajous(center_x, center_y, a, b, delta, scale=20, num_points=200):
        """利萨茹曲线"""
        t = np.linspace(0, 2 * np.pi, num_points)
        x = center_x + scale * np.sin(a * t + delta)
        y = center_y + scale * np.sin(b * t)
        return list(zip(x, y))

    @staticmethod
    def rose_curve(center_x, center_y, k, scale=20, num_points=200):
        """玫瑰曲线"""
        t = np.linspace(0, 2 * np.pi, num_points)
        r = scale * np.cos(k * t)
        x = center_x + r * np.cos(t)
        y = center_y + r * np.sin(t)
        return list(zip(x, y))

    @staticmethod
    def parabola(center_x, center_y, a=1, scale=50, num_points=100):
        """抛物线"""
        x = np.linspace(-scale, scale, num_points)
        y = a * x**2 / scale
        return list(zip(center_x + x, center_y + y))

    @staticmethod
    def hyperbola(center_x, center_y, a=1, b=1, scale=50, num_points=100):
        """双曲线"""
        t = np.linspace(-2, 2, num_points)
        x = scale * a * np.cosh(t)
        y = scale * b * np.sinh(t)
        return list(zip(center_x + x, center_y + y))

    @staticmethod
    def exponential(start_x, start_y, length, base=2, scale=10, num_points=50):
        """指数曲线"""
        x = np.linspace(0, length, num_points)
        y = scale * (base ** (x / length)) - scale
        return list(zip(start_x + x, start_y + y))


class ElementDrawer:
    """装饰元素绘制器"""

    def __init__(self, draw: ImageDraw.Draw, width: int, height: int):
        self.draw = draw
        self.width = width
        self.height = height

    def add_bubbles(self, count: int = 15):
        """添加气泡效果"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            radius = random.randint(10, 60)
            alpha = random.randint(15, 60)

            bubble_color = ColorManager.random_color_rgba((alpha, alpha + 20))
            self.draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=bubble_color)

            # 高光
            highlight_radius = radius // 3
            highlight_x = x - radius // 3
            highlight_y = y - radius // 3
            highlight_color = (255, 255, 255, min(255, alpha + 30))
            self.draw.ellipse([
                highlight_x - highlight_radius, highlight_y - highlight_radius,
                highlight_x + highlight_radius, highlight_y + highlight_radius
            ], fill=highlight_color)

    def add_curves(self, count: int = 8, curve_types: List[str] = None):
        """添加数学曲线"""
        if curve_types is None:
            curve_types = ['bezier', 'sine', 'spiral', 'lissajous', 'rose', 'parabola']

        for _ in range(count):
            curve_type = random.choice(curve_types)
            color = ColorManager.random_color_rgba((20, 60))

            try:
                if curve_type == 'bezier':
                    p0 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                    p1 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                    p2 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                    p3 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                    points = CurveGenerator.bezier_curve(p0, p1, p2, p3, 50)
                    self._draw_curve_points(points, color)

                elif curve_type == 'sine':
                    start_x = random.randint(0, self.width // 2)
                    start_y = random.randint(0, self.height)
                    length = random.randint(100, 400)
                    amplitude = random.randint(20, 80)
                    frequency = random.uniform(1.0, 4.0)
                    points = CurveGenerator.sine_wave(start_x, start_y, length, amplitude, frequency)
                    self._draw_curve_line(points, color)

                elif curve_type == 'spiral':
                    center_x = random.randint(100, self.width - 100)
                    center_y = random.randint(100, self.height - 100)
                    max_radius = random.randint(50, 150)
                    turns = random.uniform(2, 5)
                    points = CurveGenerator.spiral(center_x, center_y, max_radius, turns)
                    self._draw_curve_line(points, color)

                elif curve_type == 'lissajous':
                    center_x = random.randint(100, self.width - 100)
                    center_y = random.randint(100, self.height - 100)
                    a = random.randint(2, 6)
                    b = random.randint(2, 6)
                    delta = random.uniform(0, np.pi)
                    scale = random.randint(30, 100)
                    points = CurveGenerator.lissajous(center_x, center_y, a, b, delta, scale)
                    self._draw_curve_line(points, color)

                elif curve_type == 'rose':
                    center_x = random.randint(100, self.width - 100)
                    center_y = random.randint(100, self.height - 100)
                    k = random.randint(3, 8)
                    scale = random.randint(40, 120)
                    points = CurveGenerator.rose_curve(center_x, center_y, k, scale)
                    self._draw_curve_line(points, color)

            except Exception as e:
                print(f"Error drawing {curve_type} curve: {e}")
                continue

    def _draw_curve_points(self, points, color):
        """绘制贝塞尔曲线点"""
        for i in range(len(points) - 1):
            p1_coords = (int(points[i][0]), int(points[i][1]))
            p2_coords = (int(points[i + 1][0]), int(points[i + 1][1]))
            if (0 <= p1_coords[0] < self.width and 0 <= p1_coords[1] < self.height and
                    0 <= p2_coords[0] < self.width and 0 <= p2_coords[1] < self.height):
                self.draw.line([p1_coords, p2_coords], fill=color, width=random.randint(1, 3))

    def _draw_curve_line(self, points, color):
        """绘制曲线"""
        for i in range(len(points) - 1):
            p1_coords = (int(points[i][0]), int(points[i][1]))
            p2_coords = (int(points[i + 1][0]), int(points[i + 1][1]))
            if (0 <= p1_coords[0] < self.width and 0 <= p1_coords[1] < self.height and
                    0 <= p2_coords[0] < self.width and 0 <= p2_coords[1] < self.height):
                self.draw.line([p1_coords, p2_coords], fill=color, width=random.randint(1, 3))

    def add_particles(self, count: int = 50):
        """添加粒子效果"""
        particle_types = ['dot', 'star', 'cross', 'ring']

        for _ in range(count):
            particle_type = random.choice(particle_types)
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 8)
            color = ColorManager.random_color_rgba((20, 80))

            if particle_type == 'dot':
                self.draw.ellipse([x - size, y - size, x + size, y + size], fill=color)
            elif particle_type == 'star':
                # 简单星形
                for i in range(4):
                    angle = i * math.pi / 2
                    x2 = x + size * math.cos(angle)
                    y2 = y + size * math.sin(angle)
                    self.draw.line([(x, y), (x2, y2)], fill=color, width=1)
            elif particle_type == 'cross':
                self.draw.line([(x - size, y), (x + size, y)], fill=color, width=2)
                self.draw.line([(x, y - size), (x, y + size)], fill=color, width=2)
            elif particle_type == 'ring':
                self.draw.ellipse([x - size, y - size, x + size, y + size], outline=color, width=1)

    def add_abstract_shapes(self, count: int = 10):
        """添加抽象形状"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(20, 100)
            color = ColorManager.random_color_rgba((10, 40))

            shape_type = random.choice(['blob', 'organic', 'geometric'])

            if shape_type == 'blob':
                # 不规则blob形状
                points = []
                num_points = random.randint(6, 12)
                for i in range(num_points):
                    angle = 2 * math.pi * i / num_points
                    radius = size * (0.7 + random.random() * 0.6)
                    px = x + radius * math.cos(angle)
                    py = y + radius * math.sin(angle)
                    points.append((px, py))
                self.draw.polygon(points, fill=color)

            elif shape_type == 'organic':
                # 有机形状（多个重叠圆）
                for i in range(3):
                    offset_x = random.randint(-size // 2, size // 2)
                    offset_y = random.randint(-size // 2, size // 2)
                    radius = random.randint(size // 3, size // 2)
                    self.draw.ellipse([
                        x + offset_x - radius, y + offset_y - radius,
                        x + offset_x + radius, y + offset_y + radius
                    ], fill=color)


class ImageGenerator:
    """主图像生成器"""

    def __init__(self, config: ImageConfig = None):
        self.config = config or ImageConfig()

    def create_noisy_gradient_background(self) -> Image.Image:
        """创建带噪声的渐变背景"""
        w, h = self.config.width, self.config.height

        # 1. 创建基础渐变
        colors = ColorManager.get_gradient_colors(4)
        direction = GradientGenerator.get_random_direction()
        gradient = GradientGenerator.create_gradient(w, h, colors, direction)

        # 2. 添加噪声
        if self.config.noise_intensity > 0:
            noise = np.random.normal(0, self.config.noise_intensity * 50, gradient.shape).astype(np.float32)
            gradient = gradient.astype(np.float32) + noise
            gradient = np.clip(gradient, 0, 255)

        # 3. 转换为PIL图像
        base_img = Image.fromarray(gradient.astype(np.uint8), 'RGB')

        # 4. 应用高斯模糊
        if self.config.blur_radius > 0:
            base_img = base_img.filter(ImageFilter.GaussianBlur(radius=self.config.blur_radius))

        return base_img

    def generate_image(self) -> Image.Image:
        """生成完整图像"""
        # 创建背景
        img = self.create_noisy_gradient_background()

        # 创建装饰图层
        overlay = Image.new('RGBA', (self.config.width, self.config.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        drawer = ElementDrawer(draw, self.config.width, self.config.height)

        # 根据配置添加效果
        density = self.config.element_density

        for effect in self.config.effects:
            if effect == 'bubbles':
                drawer.add_bubbles(count=int(15 * density))
            elif effect == 'curves':
                drawer.add_curves(count=int(8 * density), curve_types=self.config.curve_types)
            elif effect == 'particles':
                drawer.add_particles(count=int(50 * density))
            elif effect == 'shapes':
                drawer.add_abstract_shapes(count=int(10 * density))

        # 合并图层
        final_img = Image.alpha_composite(img.convert('RGBA'), overlay)
        return final_img.convert('RGB')

    def batch_generate(self, count: int, output_dir: str = "output_random_bg") -> List[str]:
        """批量生成图像"""
        # 判断输出目录output_dir是否为默认值，如果是，则在后边添加随机数
        if output_dir == "output_random_bg":
            output_dir += f"_{random.randint(1000, 9999)}"
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []

        for i in range(count):
            print(f"Generating image {i + 1}/{count}")

            # 每次都随机化配置
            self.config.noise_intensity = random.uniform(0.005, 0.02)
            self.config.blur_radius = random.uniform(0.5, 1.5)
            self.config.element_density = random.uniform(0.8, 1.5)

            # 随机选择效果组合
            all_effects = ['gradient', 'bubbles', 'curves', 'particles', 'shapes']
            self.config.effects = random.sample(all_effects, random.randint(3, 5))

            # 生成图像
            img = self.generate_image()

            # 保存
            filename = f"random_bg_{i+1:03d}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, 'PNG', optimize=True)
            generated_files.append(filepath)
            print(f"Saved: {filename}")

        return generated_files


def create_sample_images(count: int = 20):
    """创建示例图像"""
    print(f"开始生成 {count} 张示例图片...")

    # 创建不同配置的生成器
    configs = [
        ImageConfig(width=1920, height=1080, style='modern', effects=['gradient', 'bubbles', 'curves']),
        ImageConfig(width=1920, height=1080, style='artistic', effects=['curves', 'particles', 'shapes']),
        ImageConfig(width=1920, height=1080, style='minimal', effects=['gradient', 'curves']),
        ImageConfig(width=1920, height=1080, style='vibrant', effects=['bubbles', 'curves', 'particles', 'shapes']),
    ]

    all_files = []
    images_per_config = count // len(configs)
    remaining = count % len(configs)

    for i, config in enumerate(configs):
        generator = ImageGenerator(config)
        current_count = images_per_config + (1 if i < remaining else 0)
        files = generator.batch_generate(current_count, f"output_random_bg_{config.style}")
        all_files.extend(files)

    print(f"\n✅ 成功生成 {len(all_files)} 张图片！")
    return all_files


if __name__ == "__main__":
    print("🎨 随机渐变背景图片生成器")
    print("=" * 50)

    # 生成20张示例图片
    sample_files = create_sample_images(20)

    print("\n📁 生成的文件:")
    for file in sample_files[:5]:  # 只显示前5个文件路径
        print(f"  {file}")
    if len(sample_files) > 5:
        print(f"  ... 还有 {len(sample_files) - 5} 个文件")

    print("\n🎯 功能特点:")
    print("✓ 随机渐变背景（16种渐变方向）")
    print("✓ 噪声纹理效果")
    print("✓ 高斯模糊处理")
    print("✓ 数学曲线（贝塞尔、正弦、螺旋、利萨茹、玫瑰等）")
    print("✓ 装饰元素（气泡、粒子、抽象形状）")
    print("✓ 柔和配色方案")
    print("✓ 参数化配置")
    print("✓ 高分辨率输出 (1920x1080)")
