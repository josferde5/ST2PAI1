import client
import file_server

token = client.generate_token()
hashfile = client.hash_file('prueba.txt')
challenge = client.challenge(token, hashfile)
print(file_server.mac_function(hashfile, token, challenge))
