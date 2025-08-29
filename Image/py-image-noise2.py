import os
import random
import string
import numpy as np
from PIL import Image
import noise
import matplotlib.pyplot as plt
import turtle

# 随机文件名生成
def random_filename(ext="png"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + f".{ext}"

# 输出目录
out_dir = os.path.join(os.getcwd(), "random_images")
os.makedirs(out_dir, exist_ok=True)

# 1. 使用 noise 生成云层背景
def generate_cloud_image(width=512, height=512, scale=100.0):
    array = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            val = noise.pnoise2(
                x / scale, y / scale,
                octaves=6, persistence=0.5, lacunarity=2.0,
                repeatx=1024, repeaty=1024, base=42
            )
            gray = int((val + 0.5) * 255)
            array[y, x] = (gray, gray, gray)
    img = Image.fromarray(array)
    fname = os.path.join(out_dir, random_filename("png"))
    img.save(fname)
    print("Cloud image saved:", fname)

# 2. 使用 matplotlib 生成几何渐变风格
def generate_matplotlib_pattern():
    x = np.linspace(0, 10, 500)
    y = np.linspace(0, 10, 500)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) ** 2 + np.cos(Y) ** 2

    plt.figure(figsize=(6,6))
    plt.imshow(Z, cmap='plasma', interpolation='bilinear')
    plt.axis('off')
    fname = os.path.join(out_dir, random_filename("png"))
    plt.savefig(fname, bbox_inches='tight', pad_inches=0)
    plt.close()
    print("Matplotlib pattern saved:", fname)

# 3. 使用 turtle 生成随机几何图案
def generate_turtle_pattern():
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.tracer(0)
    t = turtle.Turtle()
    t.speed(0)
    colors = ["red", "green", "blue", "purple", "orange", "cyan"]

    for i in range(36):
        t.color(random.choice(colors))
        t.circle(100)
        t.right(10)

    canvas = screen.getcanvas()
    fname = os.path.join(out_dir, random_filename("eps"))
    canvas.postscript(file=fname)
    screen.bye()
    print("Turtle pattern saved:", fname)

if __name__ == "__main__":
    generate_cloud_image()
    generate_matplotlib_pattern()
    generate_turtle_pattern()
    print("\nAll images saved in:", out_dir)
