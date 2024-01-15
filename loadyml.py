import yaml

def load_config(file_path='cfg/config.yml'):
    with open(file_path, 'r') as yaml_file:
        config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return config_data

# Example usage:
loaded_config = load_config()
print("Loaded Configuration:")
print(loaded_config)
