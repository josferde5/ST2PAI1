from configparser import ConfigParser
import logging

_log_level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "NOTSET": logging.NOTSET
}


class ConfigSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ConfigSingleton, cls).__call__(*args, **kwargs)

            config = ConfigParser()
            config.read('config.ini')

            cls.directories = config['DIRECTORIES']['dirsToCheck'].split(',')

            cls.check_periodicity = 1440
            cls.report_generation_periodicity = 43200
            if 'TIME' in config:
                config_tiempos = config['TIME']
                cls.check_periodicity = int(config_tiempos.get('checkPeriodicity', '1440'))
                cls.report_generation_periodicity = int(config_tiempos.get('reportGenerationPeriodicity', '43200'))

            cls.hashing_algorithm = 'BLAKE2S'
            if 'MISC' in config:
                config_misc = config['MISC']
                cls.hashing_algorithm = config_misc.get('hashingAlgorithm', 'BLAKE2S')

            config_email = config['EMAIL']
            cls.contact_email = config_email.get('contactEmail', '')

            logging_format = '%(levelname)s %(asctime)s: %(message)s'
            logging_level = 'INFO'
            if 'LOGGING' in config:
                config_logging = config['LOGGING']
                logging_format = config_logging.get('format', '%(levelname)s %(asctime)s: %(message)s', raw=True)
                logging_level = config_logging.get('level', 'INFO')

            logging.basicConfig(format=logging_format, level=_log_level.get(logging_level, logging.INFO))

        return cls._instances[cls]


class Config(metaclass=ConfigSingleton):
    pass
