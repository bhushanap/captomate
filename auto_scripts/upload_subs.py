import os
from shutil import copyfile

def copy_and_rename_subs_files(user, gradio_path):
    try:
        
        # Concatenate the chosen directory and filename to get the full path
        destination_path = os.path.join(user, 'tmp', 'subrip.' + gradio_path[-3:])

        # Copy the file to the chosen directory
        copyfile(gradio_path, destination_path)

        return True, f"File '{gradio_path}' successfully saved to '{destination_path}'."

    except Exception as e:
        return False, f"Error: {str(e)}"
    
# import os
# import subprocess
# import argparse

# def copy_and_rename_subs_files(src_folder='media', dest_folder='tmp', dest_filename='subrip.srt'):
    
#         # List all files in the source folder
#         files = os.listdir(src_folder)

#         # Filter files to include only those ending with
#         extensions = ['.srt']
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
#                         raise Exception('Something seems to have gone wrong with saving the uploaded video files. Please try again :( \n')
                    # except PermissionError:
                    #     print(f"Error: Permission denied to copy files from {src_folder}")

        

    
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Copy and convert srt files with specified name.")
#     parser.add_argument("--source_folder", default='media', help="Path to the source folder containing srt files.")
#     parser.add_argument("--destination_folder", default='tmp', help="Path to the destination folder for converted srt.")
#     parser.add_argument("--destination_filename", default='subrip.srt', help="Name of the destination file.")
    

#     args = parser.parse_args()

#     copy_and_rename_subs_files(
#         args.source_folder,
#         args.destination_folder,
#         args.destination_filename
#     )
