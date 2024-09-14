# coding=UTF-8
import os
import subprocess


def ffmpeg_MP3ToWav(input_path, output_path):
    # 提取input_path路径下所有文件名
    filename = os.listdir(input_path)
    for file in filename:
        path1 = input_path + "\\" + file
        path2 = output_path + "\\" + os.path.splitext(file)[0]
        cmd = "ffmpeg -i " + path1 + " " + path2 + ".mp3" #将input_path路径下所有音频文件转为.mp3文件
        subprocess.call(cmd, shell=True)

input_path = r"C:\Users\admin\Downloads\y"
output_path = r"C:\Users\admin\Downloads\y\y"
ffmpeg_MP3ToWav(input_path, output_path)
