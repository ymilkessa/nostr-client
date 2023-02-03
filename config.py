import json
from base_interface import BaseInterface

CLIENT_CONFIG_FILE = "clientConfigs.json"
KEY_STORAGE_FILE_KEY = "KEY_STORAGE_FILE"
RELAY_FILE_KEY = "RELAY_FILE"

class UserConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.file_name = CLIENT_CONFIG_FILE
            cls.client_configs = cls.load_client_configs()
        return cls._instance

    @classmethod
    def load_client_configs(cls, interface = BaseInterface()):
        """
        Load the client configs from the config file.
        """
        configs = {}
        keys = [KEY_STORAGE_FILE_KEY, RELAY_FILE_KEY]
        try:
            with open(cls.file_name, 'r') as f:
                content = f.read()
            if content:
                configs = json.loads(content)
        except FileNotFoundError:
            with open(cls.file_name, 'w') as f:
                f.close()
        new_file_added = False
        for key in keys:
            storage_file = configs.get(key)
            if not storage_file:
                storage_file = cls.get_config_file_from_input(key, interface)
                new_file_added = True
            configs[key] = storage_file
        if new_file_added: cls.set_client_configs(configs)
        return configs


    @classmethod
    def set_client_configs(cls, configs):
        with open(CLIENT_CONFIG_FILE, 'w') as f:
            json.dump(configs, f)
            f.close()
        cls.client_configs = configs
    
    @classmethod
    def get_config_file_from_input(cls, configuration_file_key, interface = BaseInterface()):
        file_path = None
        while not file_path:
            file_path = interface.get_input(f"Enter the file name for your {configuration_file_key}:\n>").strip()
        try:
            with open(file_path, 'r') as f:
                f.close()
        except:
            with open(file_path, 'w') as f:
                f.close()
        return file_path

    @classmethod
    def get_client_config(cls, configuration_file_key):
        return cls.client_configs.get(configuration_file_key)