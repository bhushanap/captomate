import os
# import ffmpeg
import subprocess

def merge_subs(user,bright,con,sat):
    video_path = os.path.join(user, 'tmp', 'video.mp4')
    subs_path = os.path.join(user, 'tmp', 'output.ass')
    output_path = os.path.join(user, 'tmp', 'output.mp4')
    
    brightness = float(bright) / 100 - 0.5  # value normalized from -100 to 100
    contrast = float(con) / 50  # adjust the contrast level as needed (1.0 is the default, values greater than 1 increase contrast)
    saturation = float(sat) / 50  # adjust the saturation level as needed (1.0 is the default, values greater than 1 increase saturation)

    try:
        # Use eq filter for brightness, contrast, and saturation adjustments
        filters = f'eq=brightness={brightness}:contrast={contrast}:saturation={saturation}'
        
        # ffmpeg.input(video_path).output(output_path, vf=f"{filters},ass={subs_path}", vsync=2).run(overwrite_output=True)
        ffmpeg_command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'{filters},ass={subs_path}',
            '-vsync', '2',
            output_path,
            '-y'
        ]

        subprocess.run(ffmpeg_command)
        print(f"Merging successful: subtitles on video")
    except subprocess.CalledProcessError as e:
        print(f"Error during merging: {e}")
