import secrets, hashlib, io, file_server, hmac
from error import NewFileException


def generate_token():
    # Devolvemos un token en hexadecimal con un tamaño de 256 bits (32 bytes).
    token = secrets.token_hex(32)
    return token

def hash_file(file):
    # Creamos el objeto hash, en nuestro caso usaremos Blake2. En concreto usaremos Blake2s que nos devolverá un digest con un tamaño de 256 bits
    hash_file = hashlib.blake2s()

    # Para optimizar la lectura del fichero obtenemos el tamaño de buffer del sistema.
    buffer_size = io.DEFAULT_BUFFER_SIZE

    # Abrimos el archivo para leerlo en modo binario e iteramos con un tamaño de bloque = buffer_size actualizando nuestro objeto hash.
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b""):
            hash_file.update(chunk)

    # Devolvemos la representación del hash en formato hexadecimal.
    return hash_file.hexdigest()


def challenge(token, hash_file):
    # Convertimos el token y el hash del archivo de hexadecimal a integer.
    token_int = int(token, base=16)
    hash_file_int = int(hash_file, base=16)

    # Para asegurarnos que la operación módulo entre ambos valores es un resultado distinto a los mismos, comprobamos que valor es mayor.
    if hash_file_int > token_int:
        return hash_file_int % token_int
    else:
        return token_int % hash_file_int

def generate_hmac(challenge, hash_file):
    hash_file_bytes = bytes(hash, encoding='UTF-8')
    challenge_bytes = bytes(challenge, encoding='UTF-8')
    mac = hmac.new(challenge_bytes, hash_file_bytes, hashlib.sha256)
    return mac.hexdigest()

def check_integrity_file(filepath, hmac, hmac_server):
    integrity = hmac.compare_digest(hmac, hmac_server)
    try:
        if integrity:
            print("El archivo " + filepath + " es correcto.")
        else:
            print("El archivo " + filepath + " no es correcto: el MAC obtenido en el cliente no es igual al obtenido en el servidor.")
    except NewFileException:
        print("El archivo " + filepath + " no estaba registrado en el sistema de archivos, y ha sido añadido correctamente.")

