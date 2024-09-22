import os
import argparse
from auto_scripts import load_yml
import yaml
from automate import generate_out
from auto_scripts import initialize
  

def main(video_path, config_path, audio_path, sub_path):
    # Create the full file path
    user = str(os.path.join(os.path.dirname(__file__),'user'))
    initialize.remove_folder(user)
    initialize.make_folder(user)
    video_path = os.path.abspath(video_path)

    # Load the configuration file
    config_dict = load_yml.load_config(os.path.abspath(config_path))
    config_dict['video']['input'] = video_path
    if audio_path:
        audio_path = os.path.abspath(audio_path)
        config_dict['audio']['input'] = audio_path
    
    if sub_path:
        sub_path = os.path.abspath(sub_path)
        config_dict['subs']['input'] = sub_path 

    # Save the updated configuration
    with open(os.path.join(os.path.expanduser('~'), 'captomate', 'user', 'cfg', 'config.yml'), 'w') as yaml_file:
        yaml.dump(config_dict, yaml_file, default_flow_style=False)

    # Generate output
    gpath = {'video': video_path, 'audio': audio_path, 'subtitle': sub_path}
    try:
        message = None
        fn = generate_out(user,gpath)
        while message != 'Done':
            message = next(fn)
            print(message)
        
    except Exception as e:
        raise Exception(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process video and config paths.')
    parser.add_argument('--video_path', type=str, required=True, help='Path to the video file')
    parser.add_argument('--config_path', type=str, required=True, help='Path to the config file')
    parser.add_argument('--audio_path', type=str, required=False, help='Path to the video file')
    parser.add_argument('--sub_path', type=str, required=False, help='Path to the config file')

    args = parser.parse_args()
    main(args.video_path, args.config_path, args.audio_path, args.sub_path)
