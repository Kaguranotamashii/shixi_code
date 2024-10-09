
from moviepy.editor import TextClip, CompositeVideoClip

# 创建一个文本剪辑，显示 "Hello World" 并设置尺寸为 1920x1080
txt_clip = TextClip("Hello World", fontsize=70, color='white', size=(1920, 1080))
# 设置文本剪辑的持续时间
txt_clip = txt_clip.set_duration(5).set_pos(('center', 'center'))

# 创建一个视频剪辑，将文本剪辑添加到视频上
final_clip = CompositeVideoClip([txt_clip])

# 导出视频，设置分辨率为 1920x1080
final_clip.write_videofile("hello_world.mp4", fps=24, codec='libx264', preset='fast', bitrate='5000k')