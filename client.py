import secrets, hashlib, io, file_server

from error import NewFileException


def generate_token():
    # Devolvemos un token en hexadecimal con un tamaño de 256 bits (32 bytes).
    return secrets.token_hex(32)


def hash_file(file):
    # Creamos el objeto hash, en nuestro caso usaremos Blake2. En concreto usaremos Blake2b que nos devolverá un digest con un tamaño de 256 bits
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
    # Convertimos el token y el hash del archivo de hexadecimal a integer mediante la función auxiliar 'hex_to_int()'.
    token_int = hex_to_int(token)
    hash_file_int = hex_to_int(hash_file)

    # Para asegurarnos que la operación módulo entre ambos valores es un resultado distinto a los mismos, comprobamos que valor es mayor.
    if hash_file_int > token_int:
        return hash_file_int % token_int
    else:
        return token_int % hash_file_int


def hex_to_int(hex_value):
    int_value = int(hex_value, base=16)
    return int_value


def check_file_integrity(filepath):
    token = generate_token()
    file_hash = hash_file(filepath)
    challenge_value = challenge(token, file_hash)
    mac_file = file_server.mac_function(file_hash, token, challenge_value)

    try:
        file_hash_server, mac_file_server, verification_hash = file_server.verify_integrity(filepath, file_hash, token)
        if verification_hash:
            if mac_file == mac_file_server:
                print("El archivo " + filepath + " es correcto.")
            else:
                print(
                    "El archivo " + filepath + " no es correcto: el MAC obtenido en el cliente no es igual al obtenido en el servidor.")
    except NewFileException:
        print("El archivo " + filepath + " no estaba registrado en el sistema de archivos, y ha sido añadido correctamente.")
