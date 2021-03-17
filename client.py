import secrets
import hashlib
import io


def generate_token():
    # Devolvemos un token en hexadecimal con un tamaño de 256 bits (32 bytes).
    return secrets.token_hex(32)


def hash_file(file):
    # Creamos el objeto hash, en nuestro caso usaremos Blake2. En concreto usaremos Blake2s que nos devolverá un digest con un tamaño de 256 bits.
    blake2s = hashlib.blake2s()

    # Para optimizar la lectura del fichero obtenemos el tamaño de buffer del sistema.
    buffer_size = io.DEFAULT_BUFFER_SIZE

    # Abrimos el archivo para leerlo en modo binario e iteramos con un tamaño de bloque = buffer_size actualizando nuestro objeto hash.
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b""):
            blake2s.update(chunk)

    # Devolvemos la representación del hash en formato hexadecimal.
    return blake2s.hexdigest()


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
