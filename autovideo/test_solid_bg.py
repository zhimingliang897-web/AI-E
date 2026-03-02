import os
import sys

# add parent dir so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compositor.assembler import _make_title_on_bg, _make_gradient_bg

width, height = 1920, 1080
duration = 2.0

bg = _make_gradient_bg(width, height, duration)
clip = _make_title_on_bg(bg, "函数调用定义", width, height, duration, text_color="#333333", font_size=56)

clip.save_frame("test_solid_bg.png", t=1.0)
print("Finished saving test_solid_bg.png")
