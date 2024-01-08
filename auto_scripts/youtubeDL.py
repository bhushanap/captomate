import random
import yt_dlp
import os
import imageio
import subprocess
import random

def get_video_resolution(file_path):
    try:
        # Run ffprobe command to get video information
        result = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', file_path])

        # Parse the output to get width and height
        w, h = map(int, result.decode('utf-8').strip().split(','))

        return w, h

    except subprocess.CalledProcessError:
        # Handle errors, such as file not found or invalid video file
        print(f"Error: Unable to get resolution for {file_path}")
        return None

def downloadVideo(user, resx, resy, start_time, video_url):
    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(user,'tmp','yt'),
            'filesize': 900e6,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)

        print(f"Download successful: {os.path.join(user,'tmp','yt')}")
    except yt_dlp.DownloadError as e:
        print(f"Error during download: {e}")
        raise Exception('Failed to download video. Either the video is too long or no file formats are available for download.\n')

    directory_path = os.path.join(user,'tmp')
    for filename in os.listdir(directory_path):
        print(filename)
        if filename.startswith('yt'):
            video_file = filename

    # print(yt_files)
    video_file = os.path.join(user, 'tmp', video_file)
    audio_file = os.path.join(user, 'tmp', 'audio.mp3')
    output_file = os.path.join(user, 'tmp', 'video.mp4')
    
    # resx, resy = 640, 480  # Set your desired resolution
    wo, ho = get_video_resolution(video_file)
    
    w = int(resx / resy * ho)
    h = ho
    x = int((wo - w) / 2)
    y = 0

    speed_factor = 1

    try:
        # Get audio duration using ffprobe
        if os.path.exists(audio_file):
            audio_duration = subprocess.check_output(['ffprobe', '-i', audio_file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], text=True).strip()
        elif os.path.exists(os.path.join(user, 'tmp', 'subrip.srt')):
            from auto_scripts.subtitle import srt_duration
            audio_duration = srt_duration(os.path.join(user, 'tmp', 'subrip.srt'))
        else:
            audio_duration = 10
        # Get audio duration using ffprobe
        # audio_duration = subprocess.check_output(['ffprobe', '-i', audio_file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], text=True).strip()
        video_duration = subprocess.check_output(['ffprobe', '-i', video_file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], text=True).strip()
        video_duration = int(float(video_duration))
        # print(video_duration, type(video_duration))
        start_time = random.randint(0, video_duration-int(float(audio_duration))*speed_factor)
        print(start_time)
        # Run ffmpeg command
        if os.path.exists(audio_file):
            subprocess.run(['ffmpeg', '-ss', str(start_time), '-i', video_file, '-i', audio_file, '-filter_complex', f'[0:v]crop={w}:{h}:{x}:0,setpts=PTS/{speed_factor},scale={resx}:{resy}[v];[1:a]atempo={1}[a]', '-t', str(audio_duration), '-c:v', 'libx264','-map', '[v]', '-map', '[a]', '-shortest', output_file, "-y"],check=True)
        else:
            subprocess.run(['ffmpeg', '-ss', str(start_time), '-i', video_file, '-filter_complex', f'[0:v]crop={w}:{h}:{x}:0,setpts=PTS/{speed_factor},scale={resx}:{resy}[v]', '-t', str(audio_duration), '-c:v', 'libx264','-map', '[v]', output_file, "-y"],check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        raise Exception('Something seems to have gone wrong in youtube video trimming. Please try again with another video. If this error persists, please contact the developers. \n')

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Download youtube video from given start time.")
#     parser.add_argument("--resx", type=int, default=720, help="Resolution X.")
#     parser.add_argument("--resy", type=int, default=1280, help="Resolution Y.")
#     parser.add_argument("--start_time", default=0, help="video start time")
#     parser.add_argument("--URL", default=None, help="URL of the video")
    

#     args = parser.parse_args()

#     downloadVideo(
#         args.resx,
#         args.resy,
#         args.start_time,
#         args.URL
#     )