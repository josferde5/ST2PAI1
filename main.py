import time
import client, reports
import file_server
import os
import schedule
import config
from error import ApplicationError
from datetime import datetime


def initial_store(c):
    for d in c.directories:
        file_server.store_files(d)


def periodical_check():
    c = config.Config()
    file_server.register_analysis_time()
    entries = []
    for d in c.directories:
        for root, dirs, filenames in os.walk(d):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                filepath, file_hash_server, verification_hash = client.check_file_integrity(full_path)
                entries.append(
                    [datetime.now().strftime('%d/%m/%Y %H:%M:%S'), filepath, file_hash_server, verification_hash])

    reports.create_logs(tuple(entries))
    file_server.check_deleted_files()


def configuration():
    if not os.path.exists('config.ini'):
        raise ApplicationError("There's no configuration file in the root folder of the project")

    # Lectura del archivo de configuración
    c = config.Config()

    # Populación inicial del sistema de archivos
    initial_store(c)

    # Programación de tareas:
    schedule.every(0.5).minutes.do(periodical_check)


if __name__ == "__main__":

    configuration()

    while True:
        schedule.run_pending()
        time.sleep(1)
