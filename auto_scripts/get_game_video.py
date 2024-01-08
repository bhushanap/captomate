import random
import os
import subprocess

def get_video(user, resx, resy, demo):
    w = int(resx/resy*720)
    h = 720
    x = int((1280 - w)/2)
    y = 0
    if demo == 'Minecraft':
        video_file = os.path.join('demo', 'minecraft_gameplay.mp4')
    elif demo == 'Fortnite':
        video_file = os.path.join('demo', 'fortnite_gameplay.mp4')
    elif demo == 'MarioKart':
        video_file = os.path.join('demo', 'mariokart_gameplay.mp4')
    elif demo == 'GTA V':
        video_file = os.path.join('demo', 'gtav_gameplay.mp4')
    elif demo == 'Miscellaneous':
        video_file = os.path.join('demo', 'misc_gameplay.mp4')
    audio_file = os.path.join(user, 'tmp', 'audio.mp3')
    output_file = os.path.join(user, 'tmp', 'video.mp4')
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
        raise Exception('Something seems to have gone wrong in demo video conversion. Please try again :( \n')
