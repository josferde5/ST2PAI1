import hashlib
import hmac
import os

import client

hash_table = {}

def store_files(path : str):
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            hash_hex = client.hash_file(full_path)
            with open(full_path, 'rb') as f:
                bin_data = f.read()
                hash_table[full_path] = (bin_data, hash_hex)


def get_file_and_hash(path : str):
    return hash_table[path]


def mac_function(hash, token, challenge):
    if challenge != client.challenge(token, hash):
        return None
    else:
        msg_bytes = bytes(hash, encoding='UTF-8')
        token_bytes = bytes(token, encoding='UTF-8')
        digester = hmac.new(token_bytes, msg_bytes, hashlib.sha256)
        return digester.hexdigest()


def verify_integrity(filepath, file_hash, token):
    file_data, file_hash_stored = get_file_and_hash(filepath)
    verification_hash = file_hash == file_hash_stored
    mac_file = None
    if verification_hash:
        challenge = client.challenge(token, file_hash_stored)
        mac_file = mac_function(file_hash, token, challenge)
    else:
        print("El archivo " + filepath + " no es correcto: el hash enviado por el cliente no es igual al obtenido por el servidor.")
    
 #   update_stats(filepath, file_hash, verification_hash)
    return file_hash_stored, mac_file, verification_hash
