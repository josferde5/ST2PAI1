from configparser import ConfigParser


class ConfigSingleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(ConfigSingleton, cls).__call__(*args, **kwargs)
            config = ConfigParser()
            config.read('config.ini')
            cls.directories = config['DIRECTORIOS']['directoriosQueVigilar'].split(',')

            config_tiempos = config['TIEMPOS']
            cls.intervalo_comprobacion = int(config_tiempos.get('intervaloComprobacion', '1440'))
            cls.intervalo_informes = int(config_tiempos.get('intervaloInformes', '43200'))

            config_misc = config['MISC']
            cls.algoritmo_hashing = config_misc.get('algoritmoHashing', 'BLAKE2S')

            config_email = config['EMAIL']
            cls.contact_email = config_email.get('contactEmail', '')

        return cls._instances[cls]


class Config(metaclass=ConfigSingleton):
    pass

