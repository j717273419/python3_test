
# 创建一个400x200的RGB图像，并填充一个从黑色到红色的渐变
# from PIL import Image
#
# w, h = 400, 200
# img = Image.new("RGB", (w, h))
#
# for x in range(w):
#     r = int(255 * (x / w))  # 从黑到红渐变
#     g = 0
#     b = 255 - r
#     for y in range(h):
#         img.putpixel((x, y), (r, g, b))
#
# img.show()

# 创建一个400x200的RGB图像，并填充一个从黑色到红色的渐变,间隔色彩
# from PIL import Image
# import random
# w, h = 400, 200
# img = Image.new("RGB", (w, h))
# colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
# for x in range(w):
#     color = random.choice(colors)
#     for y in range(h):
#         img.putpixel((x, y), color)
# img.show()


# 创建一个400x200的RGB图像，并填充一个从黑色到红色的渐变,从左下角到右上角过渡
# from PIL import Image
# w, h = 400, 200
# img = Image.new("RGB", (w, h))
# for x in range(w):
#     for y in range(h):
#         r = int(255 * (x / w))  # 从黑到红渐变
#         g = 0
#         b = int(255 * (1 - y / h))  # 从蓝到黑渐变
#         img.putpixel((x, y), (r, g, b))
# img.show()


# 创建一个400x400的图像，并填充4种不同颜色的渐变,从左下角到右上角过渡
from PIL import Image
w, h = 400, 400
img = Image.new("RGB", (w, h))
for x in range(w):
    for y in range(h):
        if x < w / 2 and y < h / 2:  # 左上角
            r = int(255 * (x / (w / 2)))
            g = int(255 * (y / (h / 2)))
            b = 0
        elif x >= w / 2 and y < h / 2:  # 右上角
            r = int(255 * (1 - (x - w / 2) / (w / 2)))
            g = int(255 * (y / (h / 2)))
            b = 0
        elif x < w / 2 and y >= h / 2:  # 左下角
            r = 0
            g = int(255 * (1 - (y - h / 2) / (h / 2)))
            b = int(255 * (x / (w / 2)))
        else:  # 右下角
            r = 0
            g = int(255 * (1 - (y - h / 2) / (h / 2)))
            b = int(255 * (1 - (x - w / 2) / (w / 2)))
        img.putpixel((x, y), (r, g, b))
img.show()
