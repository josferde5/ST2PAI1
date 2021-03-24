import time
import client, reports
import file_server
import os
import schedule
import config
from error import ApplicationError
from datetime import datetime

from email_module import create_message, init_service, send_message


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
                entries.append([datetime.now().strftime('%d/%m/%Y %H:%M:%S'), filepath, file_hash_server, verification_hash])
    
    reports.create_logs(tuple(entries))
    file_server.check_deleted_files()


def send_email():
    email_sender = 'HIDS ST2 Service'
    email_to = 'jorrapdia@alum.us.es'
    email_subject = 'Informe periódico de integridad del sistema'
    email_body = 'Este email es una prueba.'
    email_file = 'Prueba/salida.csv'

    gmail_service = init_service()
    raw_message = create_message(email_sender, email_to, email_subject, email_body, email_file)
    send_message(gmail_service, "me", raw_message)


def configuration():
    if not os.path.exists('config.ini'):
        raise ApplicationError("There's no configuration file in the root folder of the project")

    # Lectura del archivo de configuración
    c = config.Config()

    # Populación inicial del sistema de archivos
    initial_store(c)

    # Programación de tareas:
    schedule.every(0.2).minutes.do(periodical_check)
    schedule.every(3).minutes.do(reports.create_report('Reports/logs.csv'))
    

if __name__ == "__main__":

    configuration()

    while True:
        schedule.run_pending()
        time.sleep(1)
