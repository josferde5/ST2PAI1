import time
import client
import file_server
import os
import schedule

from email_module import create_message, init_service, send_message


def prueba_jorge():
    token = client.generate_token()
    hashfile = client.hash_file('prueba.txt')
    challenge = client.challenge(token, hashfile)
    print(file_server.mac_function(hashfile, token, challenge))


def periodical_check():
    path = "Prueba"
    dummy = True
    file_server.store_files(path)
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if dummy:
                with open(full_path, 'w') as f:
                    f.write("holaquetal")
            client.check_file_integrity(full_path)
            if dummy:
                with open(full_path, 'w') as f:
                    f.write("Esto es una prueba para las mac.")
                dummy = False

def send_email():
    email_sender = 'HIDS ST2 Service'
    email_to = 'jorrapdia@alum.us.es'
    email_subject = 'Informe periódico de integridad del sistema'
    email_body = 'Este email es una prueba.'
    email_file = 'Prueba/salida.csv'

    gmail_service = init_service()
    raw_message = create_message(email_sender, email_to, email_subject, email_body, email_file)
    send_message(gmail_service, "me", raw_message)

# Programación de tareas:
schedule.every(0.5).minutes.do(prueba_jorge)
schedule.every().minute.do(periodical_check)
schedule.every().minute.do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
