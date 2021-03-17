import hashlib
import hmac

import client


def mac_function(hash, token, challenge):
    if challenge != client.challenge(token, hash):
        return None
    else:
        msg_bytes = bytes(hash, encoding='UTF-8')
        token_bytes = bytes(token, encoding='UTF-8')
        digester = hmac.new(token_bytes, msg_bytes, hashlib.sha1)
        return digester.hexdigest()
