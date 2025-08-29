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
class GenerationConfig:
    """生成配置类"""
    width: int = 1920  # 默认改为1920
    height: int = 1080  # 默认改为1080
    style: str = 'mixed'
    color_scheme: str = 'pastel'
    noise_intensity: float = 0.01
    blur_radius: float = 0.5
    effects: List[str] = None
    element_density: float = 1.0
    export_sizes: List[Tuple[int, int]] = None

    def __post_init__(self):
        if self.effects is None:
            self.effects = ['gradient', 'bubbles', 'dots', 'curves']  # 默认包含curves
        if self.export_sizes is None:
            self.export_sizes = [(self.width, self.height)]  # 使用动态尺寸


class CurveGenerator:
    """曲线生成器类，包含各种数学曲线"""

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


class ColorSchemeManager:
    """配色方案管理器"""

    SCHEMES = {
        'pastel': [
            np.array([245, 222, 179]), np.array([255, 228, 196]), np.array([240, 248, 255]),
            np.array([255, 250, 240]), np.array([253, 245, 230]), np.array([250, 235, 215]),
        ],
        'vibrant': [
            np.array([255, 99, 132]), np.array([54, 162, 235]), np.array([255, 205, 86]),
            np.array([75, 192, 192]), np.array([153, 102, 255]), np.array([255, 159, 64]),
        ],
        'ocean': [
            np.array([0, 119, 190]), np.array([0, 180, 216]), np.array([144, 224, 239]),
            np.array([173, 232, 244]), np.array([202, 240, 248]), np.array([233, 247, 251]),
        ],
        'sunset': [
            np.array([255, 94, 77]), np.array([255, 154, 0]), np.array([255, 206, 84]),
            np.array([255, 238, 173]), np.array([129, 212, 250]), np.array([224, 247, 250]),
        ],
        'forest': [
            np.array([46, 125, 50]), np.array([76, 175, 80]), np.array([129, 199, 132]),
            np.array([165, 214, 167]), np.array([200, 230, 201]), np.array([232, 245, 233]),
        ],
        'monochrome': [
            np.array([33, 33, 33]), np.array([97, 97, 97]), np.array([158, 158, 158]),
            np.array([189, 189, 189]), np.array([224, 224, 224]), np.array([245, 245, 245]),
        ]
    }

    @classmethod
    def get_colors(cls, scheme: str) -> List[np.ndarray]:
        """获取配色方案"""
        return cls.SCHEMES.get(scheme, cls.SCHEMES['pastel'])

    @classmethod
    def generate_analogous(cls, base_hue: float, count: int = 6) -> List[np.ndarray]:
        """生成类似色配色方案"""
        colors = []
        for i in range(count):
            hue = (base_hue + i * 30 / 360) % 1.0
            saturation = 0.3 + random.random() * 0.4
            lightness = 0.7 + random.random() * 0.2
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            colors.append(np.array([int(c * 255) for c in rgb]))
        return colors


class AdvancedDecorator:
    """高级装饰器类"""

    def __init__(self, draw: ImageDraw.Draw, width: int, height: int):
        self.draw = draw
        self.width = width
        self.height = height

    def add_watermark_texture(self, count: int = 30, opacity: int = 10):
        """添加水印纹理"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(20, 60)
            rotation = random.randint(0, 360)

            # 创建简单的水印形状
            shapes = ['line', 'cross', 'diamond']
            shape = random.choice(shapes)
            color = (255, 255, 255, opacity)

            if shape == 'line':
                angle = math.radians(rotation)
                x2 = x + size * math.cos(angle)
                y2 = y + size * math.sin(angle)
                self.draw.line([(x, y), (x2, y2)], fill=color, width=1)
            elif shape == 'cross':
                half_size = size // 2
                self.draw.line([(x - half_size, y), (x + half_size, y)], fill=color, width=1)
                self.draw.line([(x, y - half_size), (x, y + half_size)], fill=color, width=1)
            elif shape == 'diamond':
                points = [(x, y - size // 2), (x + size // 2, y), (x, y + size // 2), (x - size // 2, y)]
                self.draw.polygon(points, outline=color, width=1)

    def add_gradient_grid(self, cell_size: int = 40, opacity: int = 15):
        """添加渐变网格"""
        for x in range(0, self.width, cell_size):
            for y in range(0, self.height, cell_size):
                # 随机决定是否绘制这个网格
                if random.random() > 0.7:
                    continue

                # 创建渐变色
                hue = random.random()
                saturation = 0.2 + random.random() * 0.3
                lightness = 0.8 + random.random() * 0.15
                rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
                color = tuple([int(c * 255) for c in rgb] + [opacity])

                self.draw.rectangle([x, y, x + cell_size, y + cell_size], fill=color)

    def add_abstract_shapes(self, count: int = 10):
        """添加抽象形状"""
        shapes = ['blob', 'organic', 'fluid']

        for _ in range(count):
            shape_type = random.choice(shapes)
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(15, 50)
            opacity = random.randint(5, 25)

            hue = random.random()
            saturation = 0.3 + random.random() * 0.4
            lightness = 0.7 + random.random() * 0.2
            rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
            color = tuple([int(c * 255) for c in rgb] + [opacity])

            if shape_type == 'blob':
                # 创建不规则blob形状
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

    def add_particle_effects(self, count: int = 50):
        """添加粒子效果"""
        particle_types = ['dot', 'star', 'cross', 'ring']

        for _ in range(count):
            particle_type = random.choice(particle_types)
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(1, 4)
            opacity = random.randint(10, 40)

            color = (200 + random.randint(-50, 50),
                     200 + random.randint(-50, 50),
                     200 + random.randint(-50, 50), opacity)

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
                self.draw.line([(x - size, y), (x + size, y)], fill=color, width=1)
                self.draw.line([(x, y - size), (x, y + size)], fill=color, width=1)
            elif particle_type == 'ring':
                self.draw.ellipse([x - size, y - size, x + size, y + size], outline=color, width=1)

    def add_curve_patterns(self, count: int = 8):
        """添加曲线图案"""
        curve_gen = CurveGenerator()

        for _ in range(count):
            curve_type = random.choice(['bezier', 'sine', 'spiral', 'lissajous', 'rose'])
            opacity = random.randint(10, 30)
            color = (180 + random.randint(-30, 30),
                     180 + random.randint(-30, 30),
                     180 + random.randint(-30, 30), opacity)

            if curve_type == 'bezier':
                p0 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                p1 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                p2 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                p3 = np.array([random.randint(0, self.width), random.randint(0, self.height)], dtype=np.float32)
                points = curve_gen.bezier_curve(p0, p1, p2, p3, 50)
                for i in range(len(points) - 1):
                    p1_coords = (int(points[i][0]), int(points[i][1]))
                    p2_coords = (int(points[i + 1][0]), int(points[i + 1][1]))
                    if (0 <= p1_coords[0] < self.width and 0 <= p1_coords[1] < self.height and
                            0 <= p2_coords[0] < self.width and 0 <= p2_coords[1] < self.height):
                        self.draw.line([p1_coords, p2_coords], fill=color, width=1)

            elif curve_type == 'sine':
                start_x = random.randint(0, self.width // 2)
                start_y = random.randint(0, self.height)
                length = random.randint(50, 150)
                amplitude = random.randint(10, 30)
                frequency = random.uniform(0.5, 2.0)
                points = curve_gen.sine_wave(start_x, start_y, length, amplitude, frequency)
                for i in range(len(points) - 1):
                    p1_coords = (int(points[i][0]), int(points[i][1]))
                    p2_coords = (int(points[i + 1][0]), int(points[i + 1][1]))
                    if (0 <= p1_coords[0] < self.width and 0 <= p1_coords[1] < self.height and
                            0 <= p2_coords[0] < self.width and 0 <= p2_coords[1] < self.height):
                        self.draw.line([p1_coords, p2_coords], fill=color, width=1)

            elif curve_type == 'spiral':
                center_x = random.randint(50, self.width - 50)
                center_y = random.randint(50, self.height - 50)
                max_radius = random.randint(20, 40)
                turns = random.uniform(1, 3)
                points = curve_gen.spiral(center_x, center_y, max_radius, turns)
                for i in range(len(points) - 1):
                    p1_coords = (int(points[i][0]), int(points[i][1]))
                    p2_coords = (int(points[i + 1][0]), int(points[i + 1][1]))
                    if (0 <= p1_coords[0] < self.width and 0 <= p1_coords[1] < self.height and
                            0 <= p2_coords[0] < self.width and 0 <= p2_coords[1] < self.height):
                        self.draw.line([p1_coords, p2_coords], fill=color, width=1)


class EffectsProcessor:
    """效果处理器"""

    @staticmethod
    def add_lighting_effects(img: Image.Image, light_count: int = 3) -> Image.Image:
        """添加光影效果"""
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        for _ in range(light_count):
            x = random.randint(0, img.width)
            y = random.randint(0, img.height)
            radius = random.randint(30, 80)
            intensity = random.randint(5, 15)

            # 创建径向渐变光源
            for r in range(radius, 0, -5):
                alpha = max(0, intensity - (radius - r) // 3)
                color = (255, 255, 255, alpha)
                draw.ellipse([x - r, y - r, x + r, y + r], fill=color)

        return Image.alpha_composite(img.convert('RGBA'), overlay)

    @staticmethod
    def add_depth_blur(img: Image.Image, blur_map_intensity: float = 0.3) -> Image.Image:
        """添加景深模糊效果"""
        # 创建深度图
        depth_map = Image.new('L', img.size, 128)
        draw = ImageDraw.Draw(depth_map)

        # 添加一些深度变化
        for _ in range(5):
            x = random.randint(0, img.width)
            y = random.randint(0, img.height)
            radius = random.randint(50, 150)
            intensity = random.randint(50, 200)
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=intensity)

        # 应用模糊
        blurred = img.filter(ImageFilter.GaussianBlur(radius=2))

        # 根据深度图混合原图和模糊图
        result = Image.composite(img, blurred, depth_map)
        return result

    @staticmethod
    def add_color_overlay(img: Image.Image, blend_mode: str = 'multiply') -> Image.Image:
        """添加色彩叠加"""
        overlay_color = (
            random.randint(200, 255),
            random.randint(200, 255),
            random.randint(200, 255),
            30
        )

        overlay = Image.new('RGBA', img.size, overlay_color)

        if blend_mode == 'multiply':
            # 简化的乘法混合
            result = Image.blend(img.convert('RGBA'), overlay, 0.1)
        elif blend_mode == 'overlay':
            # 简化的覆盖混合
            result = Image.blend(img.convert('RGBA'), overlay, 0.05)
        else:
            result = Image.alpha_composite(img.convert('RGBA'), overlay)

        return result

    @staticmethod
    def add_dynamic_noise(img_array: np.ndarray, noise_type: str = 'perlin') -> np.ndarray:
        """添加动态噪声"""
        if noise_type == 'perlin':
            # 简化的柏林噪声模拟
            noise = np.zeros(img_array.shape[:2], dtype=np.float32)
            for octave in range(3):
                freq = 2 ** octave
                amplitude = 1.0 / (2 ** octave)

                x = np.arange(img_array.shape[1]) * freq / img_array.shape[1]
                y = np.arange(img_array.shape[0]) * freq / img_array.shape[0]
                X, Y = np.meshgrid(x, y)

                octave_noise = amplitude * np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)
                noise = noise + octave_noise.astype(np.float32)

            # 标准化噪声到合理范围
            if noise.max() != noise.min():
                noise = (noise - noise.min()) / (noise.max() - noise.min()) * 20 - 10
            else:
                noise = np.zeros_like(noise)

            # 扩展到RGB三个通道
            noise_3d = np.stack([noise, noise, noise], axis=2)
            result = img_array.astype(np.float32) + noise_3d
        else:
            # 标准随机噪声
            noise = np.random.normal(0, 5, img_array.shape).astype(np.float32)
            result = img_array.astype(np.float32) + noise

        return np.clip(result, 0, 255).astype(np.uint8)


class EnhancedBackgroundGenerator:
    """增强版背景生成器"""

    def __init__(self, config: GenerationConfig = None):
        self.config = config or GenerationConfig()
        self.color_manager = ColorSchemeManager()
        self.curve_gen = CurveGenerator()

    def create_gradient_fast(self, w: int, h: int, colors: List[np.ndarray]) -> np.ndarray:
        """快速生成渐变图像"""
        if len(colors) < 4:
            colors = colors * (4 // len(colors) + 1)

        top_left, top_right, bottom_left, bottom_right = colors[:4]
        x = np.linspace(0, 1, w)
        y = np.linspace(0, 1, h)
        X, Y = np.meshgrid(x, y)

        top = top_left[None, None, :] * (1 - X[:, :, None]) + top_right[None, None, :] * X[:, :, None]
        bottom = bottom_left[None, None, :] * (1 - X[:, :, None]) + bottom_right[None, None, :] * X[:, :, None]
        gradient = top * (1 - Y[:, :, None]) + bottom * Y[:, :, None]

        return np.clip(gradient, 0, 255).astype(np.uint8)

    def create_background(self, config: GenerationConfig = None) -> Image.Image:
        """创建背景图像"""
        if config:
            self.config = config

        w, h = self.config.width, self.config.height

        # 1. 创建基础渐变
        colors = self.color_manager.get_colors(self.config.color_scheme)
        if self.config.color_scheme == 'random':
            colors = self.color_manager.generate_analogous(random.random())

        gradient = self.create_gradient_fast(w, h, random.sample(colors, min(4, len(colors))))
        base_img = Image.fromarray(gradient.astype(np.uint8), 'RGB')

        # 2. 创建装饰图层
        overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        decorator = AdvancedDecorator(draw, w, h)

        # 3. 根据配置添加效果
        density_factor = self.config.element_density

        for effect in self.config.effects:
            if effect == 'watermark':
                decorator.add_watermark_texture(count=int(30 * density_factor))
            elif effect == 'grid':
                decorator.add_gradient_grid(opacity=15)
            elif effect == 'shapes':
                decorator.add_abstract_shapes(count=int(10 * density_factor))
            elif effect == 'particles':
                decorator.add_particle_effects(count=int(50 * density_factor))
            elif effect == 'curves':
                decorator.add_curve_patterns(count=int(8 * density_factor))
            elif effect == 'bubbles':
                self.add_bubbles(draw, w, h, count=int(15 * density_factor))
            elif effect == 'dots':
                self.add_dots(draw, w, h, count=int(25 * density_factor))

        # 4. 合并图层
        final_img = Image.alpha_composite(base_img.convert('RGBA'), overlay)

        # 5. 应用后处理效果
        if 'lighting' in self.config.effects:
            final_img = EffectsProcessor.add_lighting_effects(final_img)
        if 'depth_blur' in self.config.effects:
            final_img = EffectsProcessor.add_depth_blur(final_img)
        if 'color_overlay' in self.config.effects:
            final_img = EffectsProcessor.add_color_overlay(final_img)

        # 6. 添加模糊和噪声
        if self.config.blur_radius > 0:
            final_img = final_img.filter(ImageFilter.GaussianBlur(radius=self.config.blur_radius))

        if self.config.noise_intensity > 0:
            img_array = np.array(final_img.convert('RGB'))
            img_array = EffectsProcessor.add_dynamic_noise(img_array, 'standard')
            final_img = Image.fromarray(img_array)

        return final_img.convert('RGB')

    def add_bubbles(self, draw: ImageDraw.Draw, w: int, h: int, count: int = 15):
        """添加气泡效果"""
        for _ in range(count):
            x = random.randint(0, w)
            y = random.randint(0, h)
            radius = random.randint(5, 30)
            alpha = random.randint(10, 40)

            bubble_color = (255, 255, 255, alpha)
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=bubble_color)

            # 高光
            highlight_radius = radius // 3
            highlight_x = x - radius // 3
            highlight_y = y - radius // 3
            highlight_color = (255, 255, 255, alpha + 20)
            draw.ellipse([
                highlight_x - highlight_radius, highlight_y - highlight_radius,
                highlight_x + highlight_radius, highlight_y + highlight_radius
            ], fill=highlight_color)

    def add_dots(self, draw: ImageDraw.Draw, w: int, h: int, count: int = 25):
        """添加点状装饰"""
        for _ in range(count):
            x = random.randint(0, w)
            y = random.randint(0, h)
            radius = random.randint(1, 3)
            alpha = random.randint(15, 40)

            color = (180 + random.randint(-30, 30),
                     180 + random.randint(-30, 30),
                     180 + random.randint(-30, 30), alpha)
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)

    def batch_generate(self, count: int, output_dir: str = "enhanced_backgrounds",
                       configs: List[GenerationConfig] = None) -> List[str]:
        """批量生成背景"""
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []

        if not configs:
            # 生成随机配置
            configs = self.generate_random_configs(count)

        for i, config in enumerate(configs[:count]):
            print(f"Generating background {i + 1}/{count}")

            bg_img = self.create_background(config)

            # 导出多种尺寸
            for size_idx, (width, height) in enumerate(config.export_sizes):
                if width != config.width or height != config.height:
                    resized_img = bg_img.resize((width, height), Image.Resampling.LANCZOS)
                else:
                    resized_img = bg_img

                filename = f"enhanced_bg_{config.style}_{config.color_scheme}_{width}x{height}_{i + 1:03d}.png"
                filepath = os.path.join(output_dir, filename)
                resized_img.save(filepath)
                generated_files.append(filepath)
                print(f"Saved {filename}")

            # 保存配置
            config_filename = f"config_{i + 1:03d}.json"
            config_filepath = os.path.join(output_dir, config_filename)
            with open(config_filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(config), f, indent=2, ensure_ascii=False)

        return generated_files

    def generate_random_configs(self, count: int) -> List[GenerationConfig]:
        """生成随机配置"""
        configs = []
        styles = ['mixed', 'bubble', 'geometric', 'organic', 'minimal', 'abstract']
        color_schemes = list(self.color_manager.SCHEMES.keys()) + ['random']

        effect_pools = [
            ['gradient', 'bubbles', 'dots', 'curves'],  # 确保curves在效果池中
            ['watermark', 'particles', 'curves'],
            ['grid', 'shapes', 'lighting', 'curves'],
            ['bubbles', 'particles', 'depth_blur', 'curves'],
            ['curves', 'shapes', 'color_overlay'],
        ]

        export_sizes_options = [
            [(1920, 1080)],  # 默认1080p
            [(1920, 1080), (1280, 720)],  # 1080p + 720p
            [(1920, 1080), (3840, 2160)],  # 1080p + 4K
            [(1920, 1080), (1280, 720), (3840, 2160)],  # 多种分辨率
        ]

        for _ in range(count):
            config = GenerationConfig(
                width=1920,  # 默认1920
                height=1080,  # 默认1080
                style=random.choice(styles),
                color_scheme=random.choice(color_schemes),
                noise_intensity=random.uniform(0.005, 0.02),
                blur_radius=random.uniform(0.2, 1.0),
                effects=random.choice(effect_pools),
                element_density=random.uniform(0.5, 1.5),
                export_sizes=random.choice(export_sizes_options)
            )
            configs.append(config)

        return configs

    def create_preview_grid(self, backgrounds_dir: str = "enhanced_backgrounds",
                            grid_size: int = 4, cell_size: int = 100) -> str:
        """创建预览网格"""
        files = [f for f in os.listdir(backgrounds_dir) if f.endswith('.png') and not f.startswith('preview')]
        files = sorted(files)[:grid_size * grid_size]

        if not files:
            print("No background images found!")
            return ""

        grid_img = Image.new('RGB', (grid_size * cell_size, grid_size * cell_size), 'white')

        for i, filename in enumerate(files):
            if i >= grid_size * grid_size:
                break

            row = i // grid_size
            col = i % grid_size

            img = Image.open(os.path.join(backgrounds_dir, filename))
            img = img.resize((cell_size, cell_size), Image.Resampling.LANCZOS)

            grid_img.paste(img, (col * cell_size, row * cell_size))

        preview_path = os.path.join(backgrounds_dir, "preview_grid.png")
        grid_img.save(preview_path)
        print(f"Preview grid saved as {preview_path}")
        return preview_path


def create_random_background(width: int = 1920, height: int = 1080,
                             style: str = None, effects: List[str] = None) -> Image.Image:
    """便捷函数：创建随机背景（供第三方调用）"""
    config = GenerationConfig(
        width=width,
        height=height,
        style=style or random.choice(['mixed', 'bubble', 'geometric', 'organic', 'minimal']),
        color_scheme=random.choice(['pastel', 'vibrant', 'ocean', 'sunset', 'forest']),
        effects=effects or random.choice([
            ['gradient', 'bubbles', 'dots', 'curves'],
            ['watermark', 'particles', 'curves'],
            ['grid', 'shapes', 'lighting', 'curves'],
            ['bubbles', 'particles', 'curves'],
        ]),
        element_density=random.uniform(0.7, 1.3),
        noise_intensity=random.uniform(0.005, 0.015),
        blur_radius=random.uniform(0.3, 0.8)
    )

    generator = EnhancedBackgroundGenerator(config)
    return generator.create_background()


def create_themed_background(theme: str = 'corporate', width: int = 1920, height: int = 1080) -> Image.Image:
    """创建主题背景"""
    themes = {
        'corporate': {
            'style': 'minimal',
            'color_scheme': 'monochrome',
            'effects': ['gradient', 'grid', 'dots', 'curves'],
            'element_density': 0.6,
            'noise_intensity': 0.005,
            'blur_radius': 0.3
        },
        'creative': {
            'style': 'mixed',
            'color_scheme': 'vibrant',
            'effects': ['shapes', 'curves', 'particles', 'color_overlay'],
            'element_density': 1.2,
            'noise_intensity': 0.015,
            'blur_radius': 0.8
        },
        'nature': {
            'style': 'organic',
            'color_scheme': 'forest',
            'effects': ['bubbles', 'curves', 'lighting'],
            'element_density': 0.9,
            'noise_intensity': 0.01,
            'blur_radius': 0.6
        },
        'ocean': {
            'style': 'bubble',
            'color_scheme': 'ocean',
            'effects': ['bubbles', 'particles', 'curves'],
            'element_density': 1.0,
            'noise_intensity': 0.008,
            'blur_radius': 0.5
        },
        'sunset': {
            'style': 'geometric',
            'color_scheme': 'sunset',
            'effects': ['shapes', 'lighting', 'curves'],
            'element_density': 0.8,
            'noise_intensity': 0.012,
            'blur_radius': 0.7
        }
    }

    theme_config = themes.get(theme, themes['corporate'])

    config = GenerationConfig(
        width=width,
        height=height,
        **theme_config
    )

    generator = EnhancedBackgroundGenerator(config)
    return generator.create_background()


class BackgroundAPI:
    """背景生成API类（供第三方调用）"""

    def __init__(self):
        self.generator = EnhancedBackgroundGenerator()

    def generate(self, **kwargs) -> Image.Image:
        """生成背景图像"""
        config = GenerationConfig(**kwargs)
        return self.generator.create_background(config)

    def generate_batch(self, count: int, output_dir: str, **kwargs) -> List[str]:
        """批量生成"""
        configs = []
        for _ in range(count):
            config_dict = kwargs.copy()
            # 添加随机变化
            if 'style' not in config_dict:
                config_dict['style'] = random.choice(['mixed', 'bubble', 'geometric', 'organic'])
            if 'color_scheme' not in config_dict:
                config_dict['color_scheme'] = random.choice(['pastel', 'vibrant', 'ocean', 'sunset'])

            configs.append(GenerationConfig(**config_dict))

        return self.generator.batch_generate(count, output_dir, configs)

    def get_random_config(self) -> Dict[str, Any]:
        """获取随机配置"""
        config = self.generator.generate_random_configs(1)[0]
        return asdict(config)

    def save_config(self, config: Dict[str, Any], filepath: str):
        """保存配置文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def load_config(self, filepath: str) -> GenerationConfig:
        """加载配置文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        return GenerationConfig(**config_dict)


# 使用示例和工厂函数
def create_wallpaper(width: int = 1920, height: int = 1080, style: str = 'mixed') -> Image.Image:
    """创建壁纸"""
    return create_random_background(width, height, style, ['curves', 'particles', 'lighting'])


def create_social_media_bg(platform: str = 'instagram') -> Image.Image:
    """创建社交媒体背景"""
    sizes = {
        'instagram': (1080, 1080),
        'facebook': (1200, 630),
        'twitter': (1200, 675),
        'linkedin': (1200, 627),
        'youtube': (1280, 720)
    }

    size = sizes.get(platform, (1080, 1080))
    return create_themed_background('creative', size[0], size[1])


def create_presentation_bg(style: str = 'corporate') -> Image.Image:
    """创建演示文稿背景"""
    return create_themed_background(style, 1920, 1080)


if __name__ == "__main__":
    print("增强版背景生成器启动...")

    # 创建生成器实例
    generator = EnhancedBackgroundGenerator()

    # 示例1：生成单个背景
    print("\n1. 生成单个背景...")
    single_bg = create_random_background(1920, 1080, 'mixed', ['curves', 'bubbles', 'particles'])  # 明确指定包含curves
    os.makedirs('output', exist_ok=True)
    single_bg.save('output/single_background.png')
    print("单个背景已保存: output/single_background.png")

    # 示例2：批量生成不同主题
    print("\n2. 批量生成主题背景...")
    themes = ['corporate', 'creative', 'nature', 'ocean', 'sunset']
    for theme in themes:
        themed_bg = create_themed_background(theme, 1920, 1080)
        themed_bg.save(f'output/{theme}_theme.png')
        print(f"{theme} 主题背景已保存")

    # 示例3：使用API批量生成
    print("\n3. 使用API批量生成...")
    api = BackgroundAPI()
    generated_files = api.generate_batch(
        count=100,  # 减少数量，便于观察
        output_dir='output/batch',
        width=1920,
        height=1080,
        style='mixed',
        effects=['curves', 'particles', 'bubbles', 'shapes']  # 明确包含curves
    )
    print(f"批量生成完成，共 {len(generated_files)} 个文件")
    # 示例3：使用API批量生成
    print("\n3. 使用API批量生成curves...")
    api = BackgroundAPI()
    generated_files = api.generate_batch(
        count=100,  # 减少数量，便于观察
        output_dir='output/batch',
        width=1920,
        height=1080,
        style='mixed',
        effects=['curves']  # 明确包含curves
    )
    print(f"批量生成完成，共 {len(generated_files)} 个文件")
    # 示例3：使用API批量生成
    print("\n3. 使用API批量生成particles...")
    api = BackgroundAPI()
    generated_files = api.generate_batch(
        count=100,  # 减少数量，便于观察
        output_dir='output/batch',
        width=1920,
        height=1080,
        style='mixed',
        effects=['particles']  # 明确包含curves
    )
    print(f"批量生成完成，共 {len(generated_files)} 个文件")
    # 示例3：使用API批量生成
    print("\n3. 使用API批量生成bubbles...")
    api = BackgroundAPI()
    generated_files = api.generate_batch(
        count=100,  # 减少数量，便于观察
        output_dir='output/batch',
        width=1920,
        height=1080,
        style='mixed',
        effects=['bubbles']  # 明确包含curves
    )
    print(f"批量生成完成，共 {len(generated_files)} 个文件")
    # 示例3：使用API批量生成
    print("\n3. 使用API批量生成shapes...")
    api = BackgroundAPI()
    generated_files = api.generate_batch(
        count=100,  # 减少数量，便于观察
        output_dir='output/batch',
        width=1920,
        height=1080,
        style='mixed',
        effects=['shapes']  # 明确包含curves
    )
    print(f"批量生成完成，共 {len(generated_files)} 个文件")
    # # 示例4：创建预览网格
    # print("\n4. 创建预览网格...")
    # preview_path = generator.create_preview_grid('output/batch')
    # if preview_path:
    #     print(f"预览网格已创建: {preview_path}")

    # 批量生成100个create_random_background
    for i in range(100):
        bg = create_random_background()
        bgwallpaper = create_wallpaper()
        bgsocial_media = create_social_media_bg()
        bgpresentation = create_presentation_bg()
        filepath = f'output/create_random_background/random_bg_{i+1:03d}.png'
        filepath_bgwallpaper = f'output/create_random_background/random_bgwallpaper_{i+1:03d}.png'
        filepath_bgsocial_media = f'output/create_random_background/random_bgsocial_media_{i+1:03d}.png'
        filepath_bgpresentation = f'output/create_random_background/random_bgpresentation_{i+1:03d}.png'
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        bg.save(filepath)
        bgwallpaper.save(filepath_bgwallpaper)
        bgsocial_media.save(filepath_bgsocial_media)
        bgpresentation.save(filepath_bgpresentation)

    # 示例5：保存和加载配置
    print("\n5. 配置管理示例...")
    random_config = api.get_random_config()
    api.save_config(random_config, 'output/sample_config.json')
    print("随机配置已保存: output/sample_config.json")

    loaded_config = api.load_config('output/sample_config.json')
    config_bg = api.generate(**asdict(loaded_config))
    config_bg.save('output/config_based.png')
    print("基于配置的背景已生成: output/config_based.png")

    print("\n✅ 所有示例完成！")
    print("\n📁 生成的文件:")
    print("- output/single_background.png - 单个随机背景")
    print("- output/*_theme.png - 各种主题背景")
    print("- output/batch/ - 批量生成的背景和配置")
    print("- output/sample_config.json - 示例配置文件")
    print("- output/config_based.png - 基于配置生成的背景")

    print("\n🔧 使用说明:")
    print("1. 直接调用函数：create_random_background()")
    print("2. 主题背景：create_themed_background('creative')")
    print("3. 特定用途：create_wallpaper(), create_social_media_bg()")
    print("4. API调用：BackgroundAPI().generate()")
    print("5. 配置文件：支持保存/加载 JSON 配置")

    print("\n🎨 支持的效果:")
    print("- 数学曲线：贝塞尔、正弦波、螺旋、利萨茹、玫瑰曲线")
    print("- 装饰元素：水印纹理、渐变网格、抽象形状、粒子效果")
    print("- 高级效果：光影效果、景深模糊、色彩叠加、动态噪声")
    print("- 多尺寸导出：支持批量导出不同分辨率")
    print("- 配色方案：6种预设 + 自动生成类似色")