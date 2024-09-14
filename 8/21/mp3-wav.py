import os
import subprocess

def convert_m4a_to_wav(input_file, output_file):
    ffmpeg_path = "C:\\ffmpeg-7.0.2-essentials_build\\bin\\ffmpeg.exe"  # 修改为你的 ffmpeg 路径
    command = [
        ffmpeg_path,
        '-i', input_file,
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        output_file
    ]
    subprocess.run(command, check=True)

def main():
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.endswith('.m4a'):
            input_file = os.path.join(current_directory, filename)
            output_file = os.path.join(current_directory, filename.replace('.m4a', '.wav'))
            print(f'Converting {input_file} to {output_file}')
            convert_m4a_to_wav(input_file, output_file)

if __name__ == '__main__':
    main()