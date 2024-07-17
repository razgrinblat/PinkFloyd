import configparser


def read_config(file_path):
    """
    Reads a configuration file and returns a ConfigParser object.
    :param file_path: Path to the configuration file.
    :return: A ConfigParser object containing the configuration data.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
