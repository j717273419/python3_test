# pynput库的简单使用示例，监听键盘和鼠标事件（含移动）
# 需要安装pynput库：pip install pynput
from pynput import keyboard, mouse

def on_key_press(key):
    print(f'按下了键盘: {key}')
    if key == keyboard.Key.esc:
        print('按下了ESC键，程序即将退出...')
        return False

def on_click(x, y, button, pressed):
    if pressed:
        print(f'鼠标点击: {button} at ({x}, {y})')
    else:
        print(f'鼠标释放: {button} at ({x}, {y})')

def on_move(x, y):
    print(f'鼠标移动到: ({x}, {y})')

print("程序已启动，监听键盘和鼠标（含移动），按ESC键退出...")

keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

keyboard_listener.start()
mouse_listener.start()

try:
    keyboard_listener.join()
except KeyboardInterrupt:
    print("程序被中断退出")
finally:
    print("程序已退出")