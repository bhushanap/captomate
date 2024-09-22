
import os
from shutil import copyfile
from pydub import AudioSegment

def copy_and_rename_mp3_files(user, gradio_path):
    try:
        # Extract the file extension
        _, file_extension = os.path.splitext(gradio_path)

        # Concatenate the chosen directory and filename to get the full path
        destination_path = os.path.join(user, 'tmp', 'audio.mp3')

        # Try to convert the audio file to audio.mp3
        if True:#file_extension.lower() == '.mp3':
            audio = AudioSegment.from_file(gradio_path, format=file_extension[1:])
            audio.export(destination_path, format='mp3')
            print(f'Audio file saved as ', destination_path)
            # Remove the original audio file if the conversion is successful
            # os.remove(gradio_path)

        return True, f"File '{gradio_path}' successfully saved to '{destination_path}'."

    except Exception as e:
        raise Exception(e)
        return False, f"Error: {str(e)}"



# import subprocess
# import argparse

# def copy_and_rename_mp3_files(user):
#         # src_folder='media'
#         dest_folder=os.path.join(user,'tmp')
#         dest_filename='audio.mp3'
    
#         # List all files in the source folder
#         files = os.listdir(src_folder)

#         # Filter files to include only those ending with
#         extensions = ['.mp3','.m4a', '.aac']
#         for file in files:
#             for extension in extensions:
#                 if file.endswith(extension):
#                     mp3_file = file
#                     src_path = os.path.join(src_folder, mp3_file)
#                     dest_path = os.path.join(dest_folder, dest_filename)
#                     try:
#                         subprocess.run(["cp", src_path, dest_path],check=True)
#                     except subprocess.CalledProcessError as e:
#                         print(f"Error during conversion: {e}")
#                         raise Exception('Something seems to have gone wrong with saving the uploaded audio files. Please try again :( \n')
                    # except PermissionError:
                    #     print(f"Error: Permission denied to copy files from {src_folder}")

        

    
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Copy and convert MP3 files with specified name.")
#     parser.add_argument("--source_folder", default='media', help="Path to the source folder containing MP3 files.")
#     parser.add_argument("--destination_folder", default='tmp', help="Path to the destination folder for converted audios.")
#     parser.add_argument("--destination_filename", default='audio.mp3', help="Name of the destination file.")
    

#     args = parser.parse_args()

#     copy_and_rename_mp3_files(
#         args.source_folder,
#         args.destination_folder,
#         args.destination_filename
#     )
