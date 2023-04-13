import os
import subprocess
import multiprocessing

FFMPEG_PATH = r'G:\ffmpeg-2023-04-10-git-b18a9c2971-full_build\bin\ffmpeg.exe'  # 需要替换成你的FFmpeg可执行文件路径
INPUT_PATH = r'D:\OBS'
OUTPUT_PATH = r'G:\FFOUTPUT'  # 需要替换成你的输出文件夹路径
THREAD_NUM = 16  # 处理视频的线程数
CRF = 23  # 自定义CRF参数，越小视频质量越好，文件越大

PROCESS_NUM = multiprocessing.cpu_count()  # 获取CPU核心数作为进程数

def compress_video(filename):
    input_file = os.path.join(INPUT_PATH, filename)
    output_file = os.path.join(OUTPUT_PATH, filename)
    try:
        command = [FFMPEG_PATH, '-i', input_file, '-c:v', 'libx264', '-preset', 'superfast', '-crf', str(CRF), '-c:a', 'copy', output_file]
        subprocess.check_call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'{filename} 压制成功。')
        return output_file
    except subprocess.CalledProcessError as e:
        print(f'{filename} 压制失败，请检查原因。')
        return None

def process_video_files_pool(file):
    result = compress_video(file)
    if result:
        print(f'{file} 压缩完成。')
        return result

def process_video_files():
    video_files = [f for f in os.listdir(INPUT_PATH) if f.endswith('.mp4') or f.endswith('.avi') or f.endswith('.mkv')]
    file_count = len(video_files)
    results = []

    with multiprocessing.Pool(processes=PROCESS_NUM) as pool:
        for result in pool.map(process_video_files_pool, video_files):
            if result:
                results.append(result)

    return results

if __name__ == '__main__':
    results = process_video_files()
    print(f'压缩完毕，共压缩 {len(results)} 个文件。')
