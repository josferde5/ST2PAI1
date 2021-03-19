import time
import client
import file_server
import os
import schedule


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


# Programación de tareas:
schedule.every().minute.do(periodical_check)
schedule.every(0.5).minutes.do(prueba_jorge)

while True:
    schedule.run_pending()
    time.sleep(1)
