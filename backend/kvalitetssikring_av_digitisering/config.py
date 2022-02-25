"""Module used for loading and using config values.

"""

import configparser


class Config:
    """Simple configuration class.

    Contains only a config() function that will return object used for getting config values.
    """

    __conf = None

    @staticmethod
    def config():
        """Loads config values from file.

        Lazy loads the config on first call, then uses the loaded values for any further calls

        Returns:
            ConfigParser - A subscriptable object for getting the config values
        """

        if Config.__conf is None:
            Config.__conf = configparser.ConfigParser()
            Config.__conf.read("config")
        return Config.__conf
