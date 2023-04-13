import os
import subprocess
import threading

# 修改以下参数
FFMPEG_PATH = r'G:\ffmpeg-2023-04-10-git-b18a9c2971-full_build\bin\ffmpeg.exe'  # FFmpeg路径
INPUT_PATH = r'G:\FFINPUT'  # 输入路径
OUTPUT_PATH = r'G:\FFOUTPUT'  # 输出路径
THREAD_NUM = 16  # 线程数
CRF = 18  # 自定义CRF参数，越小视频质量越好，文件越大

def progress_bar(current, total, bar_length=50):
    percent = int(current/total * 100)
    done = int(percent * bar_length / 100)
    remain = bar_length - done
    progress = '[' + '='*done + ' ' * remain + ']'
    return f'[{progress}] {percent:.0f}%'

def compress_video(filename):
    input_file = os.path.join(INPUT_PATH, filename)
    output_file = os.path.join(OUTPUT_PATH, filename)
    try:
        command = [FFMPEG_PATH, '-i', input_file, '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', str(CRF), '-c:a', 'copy', output_file]
        subprocess.check_call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f'视频"{filename}"压缩成功（CRF={CRF}）.'
    except subprocess.CalledProcessError as e:
        return f'视频"{filename}"压缩失败.'

def process_video_files():
    video_files = os.listdir(INPUT_PATH)
    file_count = len(video_files)
    file_proc = threading.Lock()
    progress_count = 0
    total_progress = progress_bar(0, file_count)
    print(total_progress)
    threads = []

    def process_video_files_thread(video_files):
        nonlocal progress_count
        for filename in video_files:
            if filename.endswith('.mp4') or filename.endswith('.avi') or filename.endswith('.mkv'):  # 可以根据需要扩展到更多的视频格式
                result = compress_video(filename)
                with file_proc:
                    progress_count += 1
                    current_progress = progress_bar(progress_count, file_count)
                    print(current_progress)
                    print(result)

    for i in range(THREAD_NUM):
        start = int(i * file_count / THREAD_NUM)
        end = int((i + 1) * file_count / THREAD_NUM)
        t = threading.Thread(target=process_video_files_thread, args=(video_files[start:end],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    process_video_files()
