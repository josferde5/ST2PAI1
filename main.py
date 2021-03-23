import time
import client
import file_server
import os
import schedule
import config
from error import ApplicationError

from email_module import create_message, init_service, send_message


def prueba_jorge():
    token = client.generate_token()
    hashfile = client.hash_file('prueba.txt')
    challenge = client.challenge(token, hashfile)
    print(file_server.mac_function(hashfile, token, challenge))


def initial_store(c):
    for d in c.directories:
        file_server.store_files(d)


def periodical_check():
    c = config.Config()
    file_server.register_analysis_time()
    for d in c.directories:
        for root, dirs, filenames in os.walk(d):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                client.check_integrity_file(full_path)

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
    schedule.every(0.5).minutes.do(prueba_jorge)
    schedule.every(c.intervalo_comprobacion).minutes.do(periodical_check)
    schedule.every(c.intervalo_informes).minutes.do(send_email)
    


if __name__ == "__main__":

    configuration()

    while True:
        schedule.run_pending()
        time.sleep(1)
