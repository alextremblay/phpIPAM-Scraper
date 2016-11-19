

path = None


def get_url_from_config_file(cls):
    cls.path = cls.get_config_file_path()
    if Config.config_file_exists():
        return cls.load_config_file()
    else:
        return cls.create_config_file()


def get_config_file_path(cls):
    pass


def config_file_exists(cls):
    pass


def load_config_file(cls):
    pass


def create_config_file(cls):
    pass