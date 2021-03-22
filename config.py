from configparser import ConfigParser


class ConfigSingleton(type):

    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(ConfigSingleton, self).__call__(*args, **kwargs)
            config = ConfigParser()
            config.read('config.ini')
            self.directories = config['DIRECTORIOS']['directoriosQueVigilar'].split(',')

            config_tiempos = config['TIEMPOS']
            self.intervalo_comprobacion = int(config_tiempos.get('intervaloComprobacion', 1440))
            self.intervalo_informes = int(config_tiempos.get('intervaloInformes', 43200))

            config_misc = config['MISC']
            self.algoritmo_hashing = config_misc.get('algoritmoHashing', 'BLAKE2S')

        return self._instances[self]


class Config(metaclass=ConfigSingleton):
    pass

