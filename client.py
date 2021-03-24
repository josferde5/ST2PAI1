import file_server
import hashlib
import hmac
import io
import secrets
import logging

from email_module import send_alert_email
from error import NewFileException

logger = logging.getLogger(__name__)


def generate_token():
    token = secrets.token_hex(32)
    return token


def hash_file(file):
    file_hash = hashlib.blake2s()

    buffer_size = io.DEFAULT_BUFFER_SIZE

    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(buffer_size), b""):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def challenge(token, file_hash):
    token_int = int(token, base=16)
    hash_file_int = int(file_hash, base=16)

    if hash_file_int > token_int:
        return hash_file_int % token_int
    else:
        return token_int % hash_file_int


def generate_hmac(challenge_token, file_hash):
    hash_file_bytes = bytes(file_hash, encoding='UTF-8')
    challenge_bytes = bytes(challenge_token, encoding='UTF-8')
    mac = hmac.new(challenge_bytes, hash_file_bytes, hashlib.sha256)
    return mac.hexdigest()


def check_file_integrity(filepath):
    token = generate_token()
    file_hash = hash_file(filepath)
    challenge_value = challenge(token, file_hash)
    mac_file = file_server.mac_function(file_hash, token, challenge_value)
    failed_reason = 'none'

    try:
        file_hash_server, mac_file_server, verification_hash = file_server.verify_integrity(filepath, file_hash, token)
        if verification_hash and not mac_file == mac_file_server:
            logger.warning(
                "The file %s is corrupted: the MAC obtained by the client is not the same as the one obtained by the server.",
                filepath)
            failed_reason = 'mac'
        elif not verification_hash:
            failed_reason = 'hash'
            send_alert_email(filepath, 1)
    except NewFileException:
        logger.info("The file %s was not registered in the server. It has been added successfully.", filepath)
        file_hash_server = None
        verification_hash = None

    return filepath, file_hash_server, verification_hash, failed_reason
