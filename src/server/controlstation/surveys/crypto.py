
import hmac
import hashlib

def verify_signature(secret,body,signed):
    if not isinstance(body, bytes):  # Python 3
        body = body.encode('latin1')  # standard encoding for HTTP
    signature = hmac.new(secret, body, digestmod=hashlib.sha512)
    signature = signature.hexdigest()

    return signature == signed
