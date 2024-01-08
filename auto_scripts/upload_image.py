
import glob
import subprocess
import os
from PIL import Image

def img2mp4(user, gradio_path, resx, resy):
    try:
        
        # Concatenate the chosen directory and filename to get the full path
        destination_path = os.path.join(user, 'tmp', 'image.' + gradio_path[-3:])

        # Copy the file to the chosen directory
        scale_image(gradio_path, destination_path,resx,resy)

        # return True, f"File '{gradio_path}' successfully saved to '{destination_path}'."

    except Exception as e:
        return False, f"Error: {str(e)}"
    audio_file = os.path.join(user,'tmp','audio.mp3')
    try:
        # Get audio duration using ffprobe
        if os.path.exists(audio_file):
            audio_duration = subprocess.check_output(['ffprobe', '-i', audio_file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'], text=True).strip()
        elif os.path.exists(os.path.join(user, 'tmp', 'subrip.srt')):
            from auto_scripts.subtitle import srt_duration
            audio_duration = srt_duration(os.path.join(user, 'tmp', 'subrip.srt'))
        else:
            audio_duration = 10
    
        
        print('audio duration is ', audio_duration)
        output_video = os.path.join(user,'tmp','video.mp4')
        # Build the ffmpeg command with scaling
        ffmpeg_command = [
            'ffmpeg',
            '-loop', '1',
            '-i', destination_path,
            '-c:v', 'libx264',
            '-t', str(audio_duration),
            '-pix_fmt', 'yuv420p',
            output_video
        ]

        subprocess.run(ffmpeg_command)

    except Exception as e:
        return False, f"Error: {str(e)}"
    
def scale_image(input_path, output_path, resx, resy):
    """
    Scale the input image to the target resolution.

    Args:
    - input_path (str): Path to the input image file.
    - output_path (str): Path to save the scaled image.
    - resx (int): Target resolution width.
    - resy (int): Target resolution height.
    """
    # Open the input image
    input_image = Image.open(input_path)

    # Calculate new dimensions while preserving the aspect ratio
    original_width, original_height = input_image.size

    # Calculate the scaling factor for both axes
    width_ratio = resx / input_image.width
    height_ratio = resy / input_image.height

    # Choose the minimum scaling factor to maintain the aspect ratio
    max_ratio = max(width_ratio, height_ratio)

    # Calculate the new size after scaling
    new_size = (int(input_image.width * max_ratio), int(input_image.height * max_ratio))

    # Resize the image using the calculated size
    scaled_image = input_image.resize(new_size)

    # Calculate the cropping box
    left = (new_size[0] - resx) / 2
    top = (new_size[1] - resy) / 2
    right = (new_size[0] + resx) / 2
    bottom = (new_size[1] + resy) / 2

    # Crop the image
    cropped_image = scaled_image.crop((left, top, right, bottom))

    # Save the scaled and cropped image
    cropped_image.save(output_path)

# import os
# import subprocess
# import argparse

# def img2mp4(resx, resy, src_folder='media', dest_folder='tmp', dest_filename='video.mp4'):
#         # List all files in the source folder
#         files = os.listdir(src_folder)

#         # Filter files to include only those ending with 
#         extensions = ['.jpg','.png']
#         for file in files:
#             for extension in extensions:
#                 if file.endswith(extension):
#                     img_file = file 
#                     src_path = os.path.join(src_folder, img_file)
#                     dest_path = os.path.join(dest_folder, dest_filename)

#                     try:
#                         # Use ffmpeg to convert the video to the specified resolution
                        # subprocess.run(["ffmpeg", "-loop", "1", "-i", src_path, "-i", "tmp/audio.mp3", "-vf",f"scale={resx}:{resy}", "-shortest", dest_path, "-y"],check=True)
#                         print(f"Successfully converted image to video: {src_path} -> {dest_path}")
#                     except subprocess.CalledProcessError as e:
#                         print(f"Error during conversion: {e}")
#                         raise Exception('Something seems to have gone wrong in image to video conversion. Please try again :( \n')
#                     # except FileNotFoundError:
#                     #     raise Exception('Something seems to have gone wrong in demo video conversion. Please try again :( \n')
#                     #     print("Error: ffmpeg not found. Please install ffmpeg.")
#                     # except subprocess.CalledProcessError:
#                     #     print(f"Error: Failed to convert video: {src_path}")
#                     # except PermissionError:
#                     #     print(f"Error: Permission denied to convert video: {dest_path}")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Copy and convert image files to video with specified resolution.")
#     parser.add_argument("resx", type=int, default=720, help="Resolution X.")
#     parser.add_argument("resy", type=int, default=1280, help="Resolution Y.")
#     parser.add_argument("--source_folder", default='media', help="Path to the source folder containing img files.")
#     parser.add_argument("--destination_folder", default='tmp', help="Path to the destination folder for converted videos.")
#     parser.add_argument("--destination_filename", default='video.mp4', help="Name of the destination file.")
    

#     args = parser.parse_args()

#     img2mp4(
#         args.resx,
#         args.resy,
#         args.source_folder,
#         args.destination_folder,
#         args.destination_filename
#     )
