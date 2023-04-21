import configparser


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigManager(metaclass = Singleton):
    """
    Wrapper for configparser. Reads the .config file and provides
    configuration information.

    Can be initialised without a path once the first instance of the class
    is initialised.

    Input:
        - path: path to the configuration file
    """
    def __init__(self, path=None):
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, field, section='DEFAULT'):
        """
        Gets the configuration for the field requested, under the section 
        specified. Will search under the 'DEFAULT' section by default.

        Input:
            - field: The configuration field you want to get the value of
            - section: The section under which you want to search for the configuration field
        """
        return self.config[section][field]
