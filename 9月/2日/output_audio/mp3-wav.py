
import os
import subprocess

def convert_mp3_to_pcm(input_file, output_file):
    ffmpeg_path = "C:\\ffmpeg-7.0.2-essentials_build\\bin\\ffmpeg.exe"  # 修改为你的 ffmpeg 路径
    command = [
        ffmpeg_path,
        '-i', input_file,
        '-f', 's16le',  # 设置输出格式为 16 位 PCM
        '-ar', '44100',  # 设置采样率为 44100 Hz
        '-ac', '2',  # 设置声道数为 2
        output_file
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed for {input_file}: {e.stderr}")

def main():
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.mp3'):
            input_file = os.path.join(current_directory, filename)
            output_file = os.path.join(current_directory, filename.replace('.mp3', '.pcm'))
            print(f'Converting {input_file} to {output_file}')
            convert_mp3_to_pcm(input_file, output_file)

if __name__ == '__main__':
    main()