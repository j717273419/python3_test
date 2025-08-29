import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
import os
import math
import json
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
import colorsys
import asyncio
import concurrent.futures
from functools import partial
import multiprocessing
import time
import threading
from queue import Queue


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


class PerformanceMonitor:
    """性能监控器"""
    def __init__(self):
        self.start_time = None
        self.stats = {}

    def start(self):
        self.start_time = time.time()

    def log(self, operation: str):
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.stats[operation] = elapsed
            print(f"⏱️  {operation}: {elapsed:.2f}s")

    def summary(self):
        total = sum(self.stats.values())
        print(f"\n📊 性能统计:")
        for op, duration in self.stats.items():
            percentage = (duration / total * 100) if total > 0 else 0
            print(f"  {op}: {duration:.2f}s ({percentage:.1f}%)")
        print(f"  总耗时: {total:.2f}s")


class ColorManager:
    """颜色管理器 - 优化版本"""

    # 预计算的颜色池，避免每次都重新生成
    _COLOR_POOL_CACHE = None
    _CACHE_LOCK = threading.Lock()

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
    def _generate_color_pool(cls):
        """生成并缓存颜色池"""
        color_pool = cls.BASE_COLORS.copy()

        # 批量生成随机颜色，使用numpy向量化操作
        num_random_colors = len(cls.BASE_COLORS) * 2

        # 向量化生成随机RGB值
        rgb_values = np.random.randint(180, 256, (num_random_colors, 3))

        # 向量化调整颜色饱和度
        for rgb in rgb_values:
            max_val = np.max(rgb)
            min_val = np.min(rgb)
            if max_val - min_val > 60:
                avg = np.mean(rgb)
                rgb[:] = np.clip(np.random.randint(max(180, avg - 30), min(255, avg + 30), 3), 180, 255)
            color_pool.append(rgb.astype(np.uint8))

        return color_pool

    @classmethod
    def get_gradient_colors(cls, count: int = 4) -> List[np.ndarray]:
        """获取渐变颜色，使用缓存提高性能"""
        with cls._CACHE_LOCK:
            if cls._COLOR_POOL_CACHE is None:
                cls._COLOR_POOL_CACHE = cls._generate_color_pool()

        return random.sample(cls._COLOR_POOL_CACHE, count)

    @classmethod
    def random_color_rgba(cls, alpha_range: Tuple[int, int] = (10, 50)) -> Tuple[int, int, int, int]:
        """生成随机RGBA颜色"""
        # 使用numpy一次性生成所有随机数
        rgba = np.random.randint([100, 100, 100, alpha_range[0]],
                                [256, 256, 256, alpha_range[1] + 1])
        return tuple(rgba)


class FastGradientGenerator:
    """快速渐变生成器 - 优化版本"""

    DIRECTIONS = [
        'diagonal', 'diagonal_reverse', 'horizontal', 'vertical', 'radial',
        'radial_square', 'radial_ellipse', 'wave_horizontal', 'wave_vertical',
        'spiral', 'diamond', 'cross', 'triangle', 'four_corner', 'multi_radial', 'conic'
    ]

    @staticmethod
    def get_random_direction():
        """随机选择渐变方向"""
        return random.choice(FastGradientGenerator.DIRECTIONS)

    @staticmethod
    def create_gradient_vectorized(w: int, h: int, colors: List[np.ndarray], direction: str = None) -> np.ndarray:
        """向量化的渐变生成，大幅提升性能"""
        if direction is None:
            direction = FastGradientGenerator.get_random_direction()

        if len(colors) < 2:
            colors = colors * 2
        if len(colors) < 4:
            colors = colors + colors[:4-len(colors)]

        # 预分配输出数组
        gradient = np.zeros((h, w, 3), dtype=np.float32)

        if direction == 'horizontal':
            # 水平渐变：向量化实现
            x_weight = np.linspace(0, 1, w, dtype=np.float32)
            gradient[:, :, :] = (colors[0][None, None, :] * (1 - x_weight[None, :, None]) +
                               colors[1][None, None, :] * x_weight[None, :, None])

        elif direction == 'vertical':
            # 垂直渐变：向量化实现
            y_weight = np.linspace(0, 1, h, dtype=np.float32)
            gradient[:, :, :] = (colors[0][None, None, :] * (1 - y_weight[:, None, None]) +
                               colors[1][None, None, :] * y_weight[:, None, None])

        elif direction == 'diagonal':
            # 对角线渐变：优化的meshgrid
            x = np.linspace(0, 1, w, dtype=np.float32)
            y = np.linspace(0, 1, h, dtype=np.float32)
            X, Y = np.meshgrid(x, y, indexing='xy')
            t = (X + Y) * 0.5
            gradient = (colors[0][None, None, :] * (1 - t[:, :, None]) +
                       colors[1][None, None, :] * t[:, :, None])

        elif direction == 'radial':
            # 径向渐变：优化计算
            x = np.linspace(-1, 1, w, dtype=np.float32)
            y = np.linspace(-1, 1, h, dtype=np.float32)
            X, Y = np.meshgrid(x, y, indexing='xy')
            distance = np.sqrt(X ** 2 + Y ** 2)
            distance = np.clip(distance * 0.7071067811865476, 0, 1)  # 1/sqrt(2) 预计算
            gradient = (colors[0][None, None, :] * (1 - distance[:, :, None]) +
                       colors[1][None, None, :] * distance[:, :, None])

        else:  # four_corner - 默认四角渐变
            top_left, top_right, bottom_left, bottom_right = colors[:4]
            x = np.linspace(0, 1, w, dtype=np.float32)
            y = np.linspace(0, 1, h, dtype=np.float32)
            X, Y = np.meshgrid(x, y, indexing='xy')

            # 双线性插值 - 向量化实现
            top = (top_left[None, None, :] * (1 - X[:, :, None]) +
                   top_right[None, None, :] * X[:, :, None])
            bottom = (bottom_left[None, None, :] * (1 - X[:, :, None]) +
                     bottom_right[None, None, :] * X[:, :, None])
            gradient = top * (1 - Y[:, :, None]) + bottom * Y[:, :, None]

        return np.clip(gradient, 0, 255).astype(np.uint8)


class FastElementDrawer:
    """快速元素绘制器 - 减少绘制数量，提高性能"""

    def __init__(self, draw: ImageDraw.Draw, width: int, height: int):
        self.draw = draw
        self.width = width
        self.height = height

    def add_bubbles_fast(self, count: int = 8):  # 减少数量
        """快速添加气泡效果"""
        # 批量生成位置和属性
        positions = np.random.randint([0, 0], [self.width, self.height], (count, 2))
        radii = np.random.randint(15, 40, count)  # 减小尺寸范围
        alphas = np.random.randint(20, 50, count)

        for i in range(count):
            x, y = positions[i]
            radius = radii[i]
            alpha = alphas[i]

            bubble_color = ColorManager.random_color_rgba((alpha, alpha + 15))
            self.draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=bubble_color)

            # 简化高光效果
            if random.random() > 0.5:  # 只有50%的气泡有高光
                highlight_radius = radius // 4
                highlight_x = x - radius // 4
                highlight_y = y - radius // 4
                highlight_color = (255, 255, 255, min(255, alpha + 20))
                self.draw.ellipse([
                    highlight_x - highlight_radius, highlight_y - highlight_radius,
                    highlight_x + highlight_radius, highlight_y + highlight_radius
                ], fill=highlight_color)

    def add_curves_fast(self, count: int = 4):  # 减少数量
        """快速添加简化的曲线"""
        curve_types = ['sine', 'spiral']  # 只使用计算量小的曲线类型

        for _ in range(count):
            curve_type = random.choice(curve_types)
            color = ColorManager.random_color_rgba((25, 50))

            if curve_type == 'sine':
                # 简化的正弦波
                start_x = random.randint(0, self.width // 2)
                start_y = random.randint(0, self.height)
                length = random.randint(200, 400)
                amplitude = random.randint(30, 60)

                # 减少点数
                num_points = 20
                x = np.linspace(start_x, start_x + length, num_points)
                y = start_y + amplitude * np.sin(np.linspace(0, 4 * np.pi, num_points))

                points = list(zip(x.astype(int), y.astype(int)))
                self._draw_polyline_fast(points, color)

            elif curve_type == 'spiral':
                # 简化的螺旋
                center_x = random.randint(100, self.width - 100)
                center_y = random.randint(100, self.height - 100)
                max_radius = random.randint(40, 80)

                # 减少点数
                num_points = 25
                t = np.linspace(0, 4 * np.pi, num_points)
                r = max_radius * t / (4 * np.pi)
                x = center_x + r * np.cos(t)
                y = center_y + r * np.sin(t)

                points = list(zip(x.astype(int), y.astype(int)))
                self._draw_polyline_fast(points, color)

    def _draw_polyline_fast(self, points, color):
        """快速绘制多段线"""
        valid_points = [(x, y) for x, y in points if 0 <= x < self.width and 0 <= y < self.height]
        if len(valid_points) > 1:
            for i in range(len(valid_points) - 1):
                self.draw.line([valid_points[i], valid_points[i + 1]], fill=color, width=2)

    def add_particles_fast(self, count: int = 25):  # 减少数量
        """快速添加粒子效果"""
        # 批量生成属性
        positions = np.random.randint([0, 0], [self.width, self.height], (count, 2))
        sizes = np.random.randint(2, 6, count)

        for i in range(count):
            x, y = positions[i]
            size = sizes[i]
            color = ColorManager.random_color_rgba((30, 70))

            # 只绘制圆点，最简单的形状
            self.draw.ellipse([x - size, y - size, x + size, y + size], fill=color)


class FastImageGenerator:
    """快速图像生成器"""

    def __init__(self, config: ImageConfig = None):
        self.config = config or ImageConfig()
        self.monitor = PerformanceMonitor()

    def create_fast_background(self) -> Image.Image:
        """快速创建背景"""
        w, h = self.config.width, self.config.height

        # 1. 快速创建渐变
        colors = ColorManager.get_gradient_colors(4)
        direction = FastGradientGenerator.get_random_direction()
        gradient = FastGradientGenerator.create_gradient_vectorized(w, h, colors, direction)

        # 2. 可选噪声（减少强度）
        if self.config.noise_intensity > 0:
            # 使用更高效的噪声生成
            noise_scale = self.config.noise_intensity * 25  # 减少噪声强度
            noise = np.random.normal(0, noise_scale, gradient.shape).astype(np.float32)
            gradient = gradient.astype(np.float32) + noise
            gradient = np.clip(gradient, 0, 255)

        # 3. 转换为PIL图像
        base_img = Image.fromarray(gradient.astype(np.uint8), 'RGB')

        # 4. 轻量级模糊
        if self.config.blur_radius > 0:
            blur_radius = min(self.config.blur_radius, 1.0)  # 限制模糊半径
            base_img = base_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        return base_img

    def generate_image_fast(self) -> Image.Image:
        """快速生成图像"""
        # 创建背景
        img = self.create_fast_background()

        # 创建装饰图层（减少元素数量）
        overlay = Image.new('RGBA', (self.config.width, self.config.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        drawer = FastElementDrawer(draw, self.config.width, self.config.height)

        # 根据配置添加效果（减少密度）
        density = min(self.config.element_density * 0.6, 1.0)  # 减少元素密度

        for effect in self.config.effects:
            if effect == 'bubbles':
                drawer.add_bubbles_fast(count=max(1, int(8 * density)))
            elif effect == 'curves':
                drawer.add_curves_fast(count=max(1, int(4 * density)))
            elif effect == 'particles':
                drawer.add_particles_fast(count=max(1, int(25 * density)))

        # 合并图层
        final_img = Image.alpha_composite(img.convert('RGBA'), overlay)
        return final_img.convert('RGB')


def generate_single_image(args):
    """单个图像生成函数（用于多进程）"""
    config, output_dir, index = args

    # 随机化配置
    config.noise_intensity = random.uniform(0.005, 0.015)
    config.blur_radius = random.uniform(0.3, 1.0)
    config.element_density = random.uniform(0.6, 1.2)

    # 随机选择效果组合
    all_effects = ['gradient', 'bubbles', 'curves', 'particles']
    config.effects = random.sample(all_effects, random.randint(2, 4))

    # 生成图像
    generator = FastImageGenerator(config)
    img = generator.generate_image_fast()

    # 保存
    filename = f"fast_bg_{index:03d}.png"
    filepath = os.path.join(output_dir, filename)

    # 使用更快的保存选项
    img.save(filepath, 'PNG', optimize=False, compress_level=1)

    return filepath


class FastBatchGenerator:
    """快速批量生成器"""

    def __init__(self, max_workers: int = None):
        if max_workers is None:
            # 使用CPU核心数，但不超过8个进程避免过载
            self.max_workers = min(multiprocessing.cpu_count(), 8)
        else:
            self.max_workers = max_workers

        print(f"🚀 使用 {self.max_workers} 个进程并行生成")

    def batch_generate_parallel(self, configs: List[ImageConfig], images_per_config: int,
                               output_base_dir: str = "output_fast_bg") -> List[str]:
        # 当output_fast_bg是默认值时，添加随机数子目录，格式为output_fast_bg-xxxx
        if output_base_dir == "output_fast_bg":
            output_base_dir = f"{output_base_dir}-{random.randint(1000, 9999)}"
        """并行批量生成图像"""
        monitor = PerformanceMonitor()
        monitor.start()

        total_images = len(configs) * images_per_config
        print(f"📊 准备生成 {total_images} 张图片...")

        # 准备任务列表
        tasks = []
        all_files = []

        for i, config in enumerate(configs):
            output_dir = f"{output_base_dir}_{config.style}_{random.randint(1000, 9999)}"
            os.makedirs(output_dir, exist_ok=True)

            for j in range(images_per_config):
                task_index = i * images_per_config + j + 1
                tasks.append((config, output_dir, task_index))

        monitor.log("任务准备")

        # 并行执行
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            print(f"🔄 开始并行生成...")

            # 提交所有任务
            future_to_task = {executor.submit(generate_single_image, task): task for task in tasks}

            # 收集结果
            completed = 0
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    filepath = future.result()
                    all_files.append(filepath)
                    completed += 1

                    # 显示进度
                    if completed % 5 == 0 or completed == total_images:
                        percentage = (completed / total_images) * 100
                        print(f"✅ 已完成: {completed}/{total_images} ({percentage:.1f}%)")

                except Exception as exc:
                    task = future_to_task[future]
                    print(f"❌ 任务失败: {task} - {exc}")

        monitor.log("图像生成")
        monitor.summary()

        print(f"\n🎉 成功生成 {len(all_files)} 张图片！")
        print(f"📁 平均每张耗时: {(time.time() - monitor.start_time) / len(all_files):.2f}s")

        return all_files


async def generate_images_async(count: int = 20):
    """异步生成图像"""
    print("🚀 启动异步快速图像生成器")
    print("=" * 50)

    # 创建不同配置
    configs = [
        ImageConfig(width=1920, height=1080, style='modern', effects=['gradient', 'bubbles', 'curves']),
        ImageConfig(width=1920, height=1080, style='artistic', effects=['curves', 'particles']),
        ImageConfig(width=1920, height=1080, style='minimal', effects=['gradient', 'curves']),
        ImageConfig(width=1920, height=1080, style='vibrant', effects=['bubbles', 'curves', 'particles']),
    ]

    # 计算每个配置的图片数量
    images_per_config = count // len(configs)
    remaining = count % len(configs)

    # 调整数量
    config_counts = [images_per_config] * len(configs)
    for i in range(remaining):
        config_counts[i] += 1

    # 启动并行生成
    generator = FastBatchGenerator()

    # 为每个配置生成对应数量的图片
    all_files = []
    for i, (config, img_count) in enumerate(zip(configs, config_counts)):
        if img_count > 0:
            files = generator.batch_generate_parallel([config], img_count)
            all_files.extend(files)

    return all_files


def benchmark_performance():
    """性能基准测试"""
    print("🔬 性能基准测试")
    print("=" * 30)

    test_configs = [
        ImageConfig(width=1920, height=1080, style='test', effects=['gradient', 'curves']),
    ]

    # 测试不同进程数的性能
    for workers in [1, 2, 4, 8]:
        print(f"\n测试 {workers} 个进程:")
        start_time = time.time()

        generator = FastBatchGenerator(max_workers=workers)
        files = generator.batch_generate_parallel(test_configs, 5, f"benchmark_{workers}")

        total_time = time.time() - start_time
        avg_time = total_time / len(files)

        print(f"  总耗时: {total_time:.2f}s")
        print(f"  平均每张: {avg_time:.2f}s")
        print(f"  吞吐量: {len(files)/total_time:.2f} 张/秒")


def create_random_background(width: int = 1920, height: int = 1080, save: bool = False,
                             save_path: str = "random_background.png") -> Image.Image:
    """
    创建随机背景图片，优化版本

    参数:
        width: 图片宽度
        height: 图片高度
        save: 是否保存图片，默认False
        save_path: 保存路径，默认为"random_background.png"

    返回:
        PIL.Image.Image: 生成的图片对象
    """
    # 创建配置，降低元素密度和增加模糊
    config = ImageConfig(
        width=width,
        height=height,
        noise_intensity=random.uniform(0.01, 0.02),  # 适度降低噪点
        blur_radius=random.uniform(0.8, 2.0),  # 增加模糊效果
        element_density=random.uniform(0.8, 1.2)  # 降低元素密度
    )

    # 确保使用所有效果但密度适中
    config.effects = ['gradient', 'bubbles', 'curves', 'particles']

    # 生成图像
    generator = FastImageGenerator(config)
    img = generator.generate_image_fast()

    # 转为RGBA以便添加半透明元素
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)

    # 定义中心安全区域 - 将避免在这里放置明显元素
    center_margin_x = width // 4
    center_margin_y = height // 4
    center_box = (
        width // 2 - center_margin_x,
        height // 2 - center_margin_y,
        width // 2 + center_margin_x,
        height // 2 + center_margin_y
    )

    # 将图像划分为4×4网格，确保元素分布均匀
    grid_w, grid_h = 4, 4
    cell_w, cell_h = width // grid_w, height // grid_h

    # 1. 添加分散的半透明几何形状(数量减少20%)
    shape_count = random.randint(2, 6)  # 减少形状数量

    # 在每个网格单元中放置不超过1个形状
    used_cells = set()

    for _ in range(shape_count):
        # 随机选择一个未使用的网格单元
        available_cells = [(x, y) for x in range(grid_w) for y in range(grid_h)
                           if (x, y) not in used_cells]
        if not available_cells:
            break

        cell_x, cell_y = random.choice(available_cells)
        used_cells.add((cell_x, cell_y))

        # 计算此单元格内的随机位置
        base_x = cell_x * cell_w + random.randint(10, cell_w - 10)
        base_y = cell_y * cell_h + random.randint(10, cell_h - 10)

        # 检查是否在中心安全区域
        is_in_center = (
                center_box[0] <= base_x <= center_box[2] and
                center_box[1] <= base_y <= center_box[3]
        )

        # 形状类型和颜色
        shape_type = random.choice(['rect', 'circle', 'polygon'])

        # 如果在中心区域，使用更高透明度
        alpha = random.randint(5, 15) if is_in_center else random.randint(15, 30)

        # 降低颜色饱和度 - 使用更柔和的颜色
        r = random.randint(180, 240)
        g = random.randint(180, 240)
        b = random.randint(180, 240)
        color = (r, g, b, alpha)

        if shape_type == 'rect':
            size = random.randint(20, 100)
            x1 = base_x
            y1 = base_y
            x2 = x1 + size
            y2 = y1 + size
            draw.rectangle([x1, y1, x2, y2], fill=color)

        elif shape_type == 'circle':
            radius = random.randint(20, 80)
            draw.ellipse([base_x - radius, base_y - radius,
                          base_x + radius, base_y + radius], fill=color)

        else:  # polygon
            points = []
            sides = random.randint(3, 5)
            radius = random.randint(20, 60)
            for i in range(sides):
                angle = 2 * math.pi * i / sides
                px = base_x + radius * math.cos(angle)
                py = base_y + radius * math.sin(angle)
                points.append((px, py))
            draw.polygon(points, fill=color)

    # 2. 添加随机线条 (减少数量，增加透明度)
    line_count = random.randint(4, 10)  # 减少线条数量

    for _ in range(line_count):
        # 均匀分布线条
        start_grid_x, start_grid_y = random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)
        end_grid_x, end_grid_y = random.randint(0, grid_w - 1), random.randint(0, grid_h - 1)

        x1 = start_grid_x * cell_w + random.randint(10, cell_w - 10)
        y1 = start_grid_y * cell_h + random.randint(10, cell_h - 10)
        x2 = end_grid_x * cell_w + random.randint(10, cell_w - 10)
        y2 = end_grid_y * cell_h + random.randint(10, cell_h - 10)

        # 如果线条穿过中心区域，降低其可见度
        crosses_center = (
                (x1 <= center_box[2] and x2 >= center_box[0]) and
                (y1 <= center_box[3] and y2 >= center_box[1])
        )

        line_width = random.randint(1, 3)  # 减小线宽
        alpha = random.randint(10, 25) if crosses_center else random.randint(20, 40)

        # 使用柔和颜色
        r = random.randint(160, 220)
        g = random.randint(160, 220)
        b = random.randint(160, 220)
        color = (r, g, b, alpha)

        draw.line([x1, y1, x2, y2], fill=color, width=line_width)

    # 对整个图像应用轻微模糊，使元素更加柔和
    img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

    # 如果需要保存
    if save:
        # 确保目录存在
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        # 保存图像
        img.save(save_path)
        print(f"图片已保存至: {save_path}")

    return img.convert('RGB')  # 返回RGB模式的图像

# 这个版本，生成的元素太密，并且颜色太重，影响后期添加的标题
# def create_random_background(width: int = 1920, height: int = 1080, save: bool = False,
#                             save_path: str = "random_background.png") -> Image.Image:
#     """
#     创建随机背景图片，增强版
#
#     参数:
#         width: 图片宽度
#         height: 图片高度
#         save: 是否保存图片，默认False
#         save_path: 保存路径，默认为"random_background.png"
#
#     返回:
#         PIL.Image.Image: 生成的图片对象
#     """
#     # 创建丰富的配置
#     config = ImageConfig(
#         width=width,
#         height=height,
#         noise_intensity=random.uniform(0.01, 0.03),  # 增加噪点
#         blur_radius=random.uniform(0.5, 1.5),       # 更多模糊变化
#         element_density=random.uniform(1.2, 2.0)    # 增加元素密度
#     )
#
#     # 随机选择效果组合，确保使用所有效果
#     config.effects = ['gradient', 'bubbles', 'curves', 'particles']
#
#     # 随机选择曲线类型
#     config.curve_types = random.sample([
#         'bezier', 'sine', 'spiral', 'lissajous', 'rose'
#     ], random.randint(3, 5))
#
#     # 生成图像
#     generator = FastImageGenerator(config)
#     img = generator.generate_image_fast()
#
#     # 添加额外的图形元素增强层次感
#     draw = ImageDraw.Draw(img)
#
#     # 1. 添加半透明几何形状
#     for _ in range(random.randint(3, 8)):
#         shape_type = random.choice(['rect', 'circle', 'polygon'])
#         color = tuple(list(random.randint(0, 255) for _ in range(3)) + [random.randint(10, 40)])
#
#         if shape_type == 'rect':
#             x1 = random.randint(0, width)
#             y1 = random.randint(0, height)
#             x2 = random.randint(x1, min(x1 + width//2, width))
#             y2 = random.randint(y1, min(y1 + height//2, height))
#             draw.rectangle([x1, y1, x2, y2], fill=color)
#
#         elif shape_type == 'circle':
#             x = random.randint(0, width)
#             y = random.randint(0, height)
#             radius = random.randint(30, 150)
#             draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
#
#         else:  # polygon
#             points = []
#             for _ in range(random.randint(3, 6)):
#                 points.append((random.randint(0, width), random.randint(0, height)))
#             draw.polygon(points, fill=color)
#
#     # 2. 添加随机渐变线条
#     for _ in range(random.randint(5, 15)):
#         line_width = random.randint(1, 5)
#         x1 = random.randint(0, width)
#         y1 = random.randint(0, height)
#         x2 = random.randint(0, width)
#         y2 = random.randint(0, height)
#         color = tuple(random.randint(100, 255) for _ in range(3)) + (random.randint(20, 60),)
#         draw.line([x1, y1, x2, y2], fill=color, width=line_width)
#
#     # 如果需要保存
#     if save:
#         # 确保目录存在
#         save_dir = os.path.dirname(save_path)
#         if save_dir and not os.path.exists(save_dir):
#             os.makedirs(save_dir, exist_ok=True)
#
#         # 保存图像
#         img.save(save_path)
#         print(f"图片已保存至: {save_path}")
#
#     return img

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        benchmark_performance()
    else:
        # 正常生成
        print("🚀 快速随机背景图片生成器")
        # print("=" * 50)
        # print("⚡ 性能优化特性:")
        # print("✓ 多进程并行生成")
        # print("✓ 向量化渐变计算")
        # print("✓ 颜色池缓存")
        # print("✓ 减少元素密度")
        # print("✓ 优化图像保存")
        # print("✓ 内存使用优化")
        # print("-" * 50)
        #
        # # 异步生成20张图片
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # files = loop.run_until_complete(generate_images_async(100))
        # loop.close()
        #
        # print(f"\n📂 生成完成！共 {len(files)} 张图片")
        # if files:
        #     print(f"📁 示例文件: {files[0]}")

        # # 不保存，仅获取图片对象
        # img = create_random_background(1280, 720)
        #
        # # 生成并保存图片
        # img = create_random_background(1920, 1080, save=True, save_path="output/backgrounds/my_bg.png")

        img = create_random_background(1920, 1080)
        img.show()
