import os
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


def copy_and_rename_mp4_files(user, gradio_path, resx, resy):
    # Create the destination directory if it doesn't exist
    destination_path = os.path.join(user, 'tmp')
    os.makedirs(destination_path, exist_ok=True)

    # Form the new filename
    new_filename = f'video.{gradio_path[-3:]}'

    # Build the full path for the new file
    new_filepath = os.path.join(destination_path, new_filename)

    # Use ffmpeg to copy, scale, and save the video
    ffmpeg_command = [
        'ffmpeg',
        '-i', gradio_path,
        '-vf', f'scale={resx}:{resy}:force_original_aspect_ratio=increase,crop={resx}:{resy}',
        new_filepath
    ]

    # Run the ffmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        return f'Success! Video saved at: {new_filepath}'
    except subprocess.CalledProcessError as e:
        return f'Error during ffmpeg execution: {e}'
    
def trim_mp4_files(user, gradio_path, resx, resy):
    wo, ho = get_video_resolution(gradio_path)
    
    w = int(resx / resy * ho)
    h = ho
    x = int((wo - w) / 2)
    y = 0
    video_file = gradio_path
    audio_file = os.path.join(user, 'tmp', 'audio.mp3')
    output_file = os.path.join(user, 'tmp', 'video.mp4')
    speed_factor = 2

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
        raise Exception('Something seems to have gone wrong in uploaded video trimming. Please try again with another video. If this error persists, please contact the developers. \n')


# import os
# import subprocess
# import argparse

# def copy_and_rename_mp4_files(resx, resy, src_folder='media', dest_folder='tmp', dest_filename='video.mp4'):

#         # List all files in the source folder
#         files = os.listdir(src_folder)

#         # Filter files to include only those ending with 
#         extensions = ['.mp4','.mkv']
#         for file in files:
#             for extension in extensions:
#                 if file.endswith(extension):
#                     mp4_file = file 
#                     src_path = os.path.join(src_folder, mp4_file)
#                     dest_path = os.path.join(dest_folder, dest_filename)

#                     try:
#                         # Use ffmpeg to convert the video to the specified resolution
                        # subprocess.run(["ffmpeg", "-i", src_path, "-vf", f"scale={resx}:{resy}", dest_path, "-y"],check=True)
#                         print(f"Successfully converted video to {resx}x{resy}: {src_path} -> {dest_path}")

#                     except subprocess.CalledProcessError as e:
#                         print(f"Error during conversion: {e}")
#                         raise Exception('Something seems to have gone wrong with saving the uploaded video files. Please try again :( \n')
#                     # except FileNotFoundError:
#                     #     print("Error: ffmpeg not found. Please install ffmpeg.")
#                     # except subprocess.CalledProcessError:
#                     #     print(f"Error: Failed to convert video: {src_path}")
#                     # except PermissionError:
#                     #     print(f"Error: Permission denied to convert video: {dest_path}")
                


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Copy and convert MP4 files with specified resolution.")
#     parser.add_argument("resx", type=int, default=720, help="Resolution X.")
#     parser.add_argument("resy", type=int, default=1280, help="Resolution Y.")
#     parser.add_argument("--source_folder", default='media', help="Path to the source folder containing MP4 files.")
#     parser.add_argument("--destination_folder", default='tmp', help="Path to the destination folder for converted videos.")
#     parser.add_argument("--destination_filename", default='video.mp4', help="Name of the destination file.")
    

#     args = parser.parse_args()

#     copy_and_rename_mp4_files(
#         args.resx,
#         args.resy,
#         args.source_folder,
#         args.destination_folder,
#         args.destination_filename
#     )
