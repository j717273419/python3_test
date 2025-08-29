import os
import random
import numpy as np
import matplotlib.pyplot as plt

# --- 配置 ---
IMG_WIDTH = 5120  # 增大2.5倍
IMG_HEIGHT = 2700  # 增大2.5倍
DPI = 100
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output_curves')
NUM_IMAGES_PER_CURVE = 2  # 改为2张

# --- 辅助函数 ---

def random_color():
    """生成一个随机的RGB颜色元组"""
    return (random.random(), random.random(), random.random())

def random_light_color():
    """生成一个随机的浅色RGB颜色元组（背景用）"""
    # 生成浅色背景，RGB值在0.7-0.95之间
    return (random.uniform(0.7, 0.95), random.uniform(0.7, 0.95), random.uniform(0.7, 0.95))

def create_output_directory():
    """如果输出目录不存在，则创建它"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

# --- 曲线函数 ---

def generate_bezier_curve(ax):
    """生成并绘制贝塞尔曲线"""
    # 随机生成控制点
    num_curves = random.randint(2, 5)
    for _ in range(num_curves):
        t = np.linspace(0, 1, 1000)
        # 三次贝塞尔曲线
        P0 = np.array([random.uniform(0, IMG_WIDTH), random.uniform(0, IMG_HEIGHT)])
        P1 = np.array([random.uniform(0, IMG_WIDTH), random.uniform(0, IMG_HEIGHT)])
        P2 = np.array([random.uniform(0, IMG_WIDTH), random.uniform(0, IMG_HEIGHT)])
        P3 = np.array([random.uniform(0, IMG_WIDTH), random.uniform(0, IMG_HEIGHT)])

        # 贝塞尔曲线公式
        curve = (1-t)**3 * P0[:, np.newaxis] + 3*(1-t)**2*t * P1[:, np.newaxis] + 3*(1-t)*t**2 * P2[:, np.newaxis] + t**3 * P3[:, np.newaxis]

        ax.plot(curve[0], curve[1], color=random_color(), linewidth=random.randint(2, 8), alpha=0.8)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)

def generate_sine_wave(ax):
    """生成并绘制正弦波"""
    x = np.linspace(0, IMG_WIDTH, 2000)

    # 生成多个正弦波
    num_waves = random.randint(2, 4)
    for _ in range(num_waves):
        amplitude = random.uniform(50, IMG_HEIGHT / 6)
        frequency = random.uniform(0.005, 0.02)
        phase = random.uniform(0, 2 * np.pi)
        y_offset = random.uniform(IMG_HEIGHT * 0.2, IMG_HEIGHT * 0.8)

        y = amplitude * np.sin(frequency * x + phase) + y_offset
        ax.plot(x, y, color=random_color(), linewidth=random.randint(2, 8), alpha=0.8)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)

def generate_spiral(ax):
    """生成并绘制阿基米德螺旋线"""
    # 阿基米德螺旋: r = a + b*θ
    theta = np.linspace(0, random.uniform(15, 30) * np.pi, 2000)
    a = random.uniform(5, 20)
    b = random.uniform(8, 25)
    r = a + b * theta

    # 转换为笛卡尔坐标
    x = r * np.cos(theta) + IMG_WIDTH / 2
    y = r * np.sin(theta) + IMG_HEIGHT / 2

    # 添加一些变化
    colors = [random_color() for _ in range(len(theta) // 200)]
    for i in range(0, len(theta) - 200, 200):
        ax.plot(x[i:i+200], y[i:i+200], color=colors[i//200], linewidth=random.randint(2, 6), alpha=0.7)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)
    ax.set_aspect('equal', adjustable='box')

def generate_lissajous_curve(ax):
    """生成并绘制利萨茹曲线"""
    # 利萨茹曲线: x = A*sin(at + δ), y = B*sin(bt)
    t = np.linspace(0, 4 * np.pi, 2000)

    # 生成多个利萨茹曲线
    num_curves = random.randint(2, 4)
    for _ in range(num_curves):
        A = random.uniform(IMG_WIDTH / 6, IMG_WIDTH / 3)
        B = random.uniform(IMG_HEIGHT / 6, IMG_HEIGHT / 3)
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        delta = random.uniform(0, np.pi)

        x = A * np.sin(a * t + delta) + IMG_WIDTH / 2
        y = B * np.sin(b * t) + IMG_HEIGHT / 2

        ax.plot(x, y, color=random_color(), linewidth=random.randint(2, 6), alpha=0.7)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)
    ax.set_aspect('equal', adjustable='box')

def generate_rose_curve(ax):
    """生成并绘制玫瑰曲线"""
    # 玫瑰曲线: r = a*cos(k*θ) 或 r = a*sin(k*θ)
    theta = np.linspace(0, 4 * np.pi, 2000)

    # 生成多个玫瑰曲线
    num_roses = random.randint(2, 4)
    for _ in range(num_roses):
        a = random.uniform(IMG_HEIGHT / 6, IMG_HEIGHT / 3)
        k = random.randint(2, 8)

        if random.choice([True, False]):
            r = a * np.cos(k * theta)
        else:
            r = a * np.sin(k * theta)

        # 转换为笛卡尔坐标
        x = r * np.cos(theta) + IMG_WIDTH / 2
        y = r * np.sin(theta) + IMG_HEIGHT / 2

        ax.plot(x, y, color=random_color(), linewidth=random.randint(2, 6), alpha=0.7)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)
    ax.set_aspect('equal', adjustable='box')

def generate_butterfly_curve(ax):
    """生成并绘制蝴蝶曲线"""
    # 蝴蝶曲线参数方程
    t = np.linspace(0, 12 * np.pi, 2000)

    # 蝴蝶曲线公式
    r = np.exp(np.cos(t)) - 2*np.cos(4*t) + np.sin(t/12)**5
    scale = random.uniform(30, 80)

    x = scale * r * np.cos(t) + IMG_WIDTH / 2
    y = scale * r * np.sin(t) + IMG_HEIGHT / 2

    ax.plot(x, y, color=random_color(), linewidth=random.randint(2, 6), alpha=0.8)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)
    ax.set_aspect('equal', adjustable='box')

def generate_fourier_curve(ax):
    """生成并绘制傅立叶级数曲线"""
    t = np.linspace(0, 4 * np.pi, 3000)

    # 生成多个傅立叶级数近似的曲线
    num_curves = random.randint(2, 4)
    for _ in range(num_curves):
        # 基础频率和幅度
        fundamental_freq = random.uniform(0.5, 2.0)
        base_amplitude = random.uniform(IMG_HEIGHT / 8, IMG_HEIGHT / 4)

        # 傅立叶级数：叠加多个谐波
        x_fourier = np.zeros_like(t)
        y_fourier = np.zeros_like(t)

        # 添加多个谐波分量
        num_harmonics = random.randint(5, 15)
        for n in range(1, num_harmonics + 1):
            # 随机幅度衰减
            amplitude_x = base_amplitude / (n ** random.uniform(0.5, 1.5))
            amplitude_y = base_amplitude / (n ** random.uniform(0.5, 1.5))

            # 添加谐波
            x_fourier += amplitude_x * np.cos(n * fundamental_freq * t + random.uniform(0, 2*np.pi))
            y_fourier += amplitude_y * np.sin(n * fundamental_freq * t + random.uniform(0, 2*np.pi))

        # 中心化
        x_final = x_fourier + IMG_WIDTH / 2
        y_final = y_fourier + IMG_HEIGHT / 2

        ax.plot(x_final, y_final, color=random_color(), linewidth=random.randint(2, 5), alpha=0.7)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)
    ax.set_aspect('equal', adjustable='box')

def generate_heart_curve(ax):
    """生成并绘制心形曲线"""
    t = np.linspace(0, 2 * np.pi, 2000)

    # 生成多个心形曲线，使用不同的变形
    num_hearts = random.randint(1, 3)
    for _ in range(num_hearts):
        scale = random.uniform(100, 300)

        # 经典心形曲线参数方程
        # x = 16sin³(t), y = 13cos(t) - 5cos(2t) - 2cos(3t) - cos(4t)
        x = scale * (16 * np.sin(t)**3)
        y = scale * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))

        # 添加一些随机变形
        variation = random.uniform(0.8, 1.2)
        x = x * variation + IMG_WIDTH / 2
        y = -y * variation + IMG_HEIGHT / 2  # 翻转Y轴使心形正向

        # 添加旋转
        angle = random.uniform(0, 2 * np.pi)
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        x_rot = (x - IMG_WIDTH/2) * cos_a - (y - IMG_HEIGHT/2) * sin_a + IMG_WIDTH/2
        y_rot = (x - IMG_WIDTH/2) * sin_a + (y - IMG_HEIGHT/2) * cos_a + IMG_HEIGHT/2

        ax.plot(x_rot, y_rot, color=random_color(), linewidth=random.randint(3, 8), alpha=0.8)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)
    ax.set_aspect('equal', adjustable='box')

def generate_wormhole_curve(ax):
    """生成并绘制虫洞曲线（优化版本，减少密度）"""
    # 创建径向和角度网格，减少密度避免重叠
    theta = np.linspace(0, 2 * np.pi, 30)  # 减少角度分割数
    r_values = np.linspace(50, min(IMG_WIDTH, IMG_HEIGHT) / 3, 8)  # 减少径向分割数

    center_x, center_y = IMG_WIDTH / 2, IMG_HEIGHT / 2

    # 绘制径向线（从中心向外）
    for i in range(0, len(theta), 3):  # 每3个角度画一条线
        t = theta[i]
        r_max = random.uniform(min(IMG_WIDTH, IMG_HEIGHT) / 4, min(IMG_WIDTH, IMG_HEIGHT) / 2.5)
        r_line = np.linspace(0, r_max, 100)

        # 添加扭曲效果
        twist = random.uniform(0.1, 0.3)
        x_line = center_x + r_line * np.cos(t + twist * r_line / r_max)
        y_line = center_y + r_line * np.sin(t + twist * r_line / r_max)

        ax.plot(x_line, y_line, color=random_color(), linewidth=random.randint(1, 3), alpha=0.6)

    # 绘制环形线（同心圆变形）
    for r in r_values[1::2]:  # 只绘制部分环形，避免过密
        # 创建变形的圆
        theta_circle = np.linspace(0, 2 * np.pi, 150)
        distortion = random.uniform(0.1, 0.4)

        x_circle = center_x + r * (1 + distortion * np.sin(3 * theta_circle)) * np.cos(theta_circle)
        y_circle = center_y + r * (1 + distortion * np.cos(2 * theta_circle)) * np.sin(theta_circle)

        ax.plot(x_circle, y_circle, color=random_color(), linewidth=random.randint(1, 3), alpha=0.5)

    # 添加一些螺旋效果
    spiral_theta = np.linspace(0, 6 * np.pi, 300)
    spiral_r = np.linspace(10, min(IMG_WIDTH, IMG_HEIGHT) / 3, len(spiral_theta))

    x_spiral = center_x + spiral_r * np.cos(spiral_theta)
    y_spiral = center_y + spiral_r * np.sin(spiral_theta)

    ax.plot(x_spiral, y_spiral, color=random_color(), linewidth=random.randint(2, 4), alpha=0.7)

    ax.set_xlim(0, IMG_WIDTH)
    ax.set_ylim(0, IMG_HEIGHT)
    ax.set_aspect('equal', adjustable='box')

# --- 主生成函数 ---

def generate_images():
    """主函数，循环生成所有曲线的图像"""
    try:
        create_output_directory()

        curves = {
            "Bezier": generate_bezier_curve,
            "SineWave": generate_sine_wave,
            "Spiral": generate_spiral,
            "Lissajous": generate_lissajous_curve,
            "Rose": generate_rose_curve,
            "Butterfly": generate_butterfly_curve,
            "Fourier": generate_fourier_curve,
            "Heart": generate_heart_curve,
            "Wormhole": generate_wormhole_curve,
        }

        total_images = len(curves) * NUM_IMAGES_PER_CURVE
        current_image = 0

        for curve_name, generator_func in curves.items():
            print(f"生成 {curve_name} 曲线...")
            for i in range(NUM_IMAGES_PER_CURVE):
                current_image += 1

                # 创建图形和坐标轴
                fig, ax = plt.subplots(figsize=(IMG_WIDTH / DPI, IMG_HEIGHT / DPI), dpi=DPI)

                # 设置随机背景色
                bg_color = random_light_color()
                fig.patch.set_facecolor(bg_color)
                ax.set_facecolor(bg_color)

                # 生成并绘制曲线
                generator_func(ax)

                # 隐藏坐标轴
                ax.axis('off')

                # 保存图像
                output_path = os.path.join(OUTPUT_DIR, f"{curve_name}_{i+1:02d}.png")
                plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1, dpi=DPI)
                plt.close(fig)

                print(f"  已保存 [{current_image}/{total_images}]: {output_path}")

        print(f"\n所有图像生成完成！共生成 {total_images} 张图片。")
        print(f"图片保存在: {OUTPUT_DIR}")

    except Exception as e:
        print(f"生成图像时发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("开始生成数学曲线图像...")
    print(f"图像尺寸: {IMG_WIDTH}x{IMG_HEIGHT} 像素")
    print(f"每种曲线生成: {NUM_IMAGES_PER_CURVE} 张图片")
    print("-" * 50)
    generate_images()
