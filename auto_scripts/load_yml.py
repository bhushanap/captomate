import yaml
import os

def load_config(file_path):
    with open(file_path, 'r') as yaml_file:
        config_data = yaml.safe_load(yaml_file)
    return config_data

# if __name__ == "__main__":
#     config_path = "cfg/cfg.yml"  # Update this path accordingly
#     config_dict = load_config(config_path)
#     print(config_dict)
