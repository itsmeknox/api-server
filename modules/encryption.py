from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet


import jwt
import base64
import time


class DecryptFailed(Exception):
    def __init__(self, description="Decryption failed."):
        self.description = description
        super().__init__(description)

class EncryptFailed(Exception):
    def __init__(self, description="Encryption failed."):
        self.description = description
        super().__init__(description)


class InvalidKey(Exception):
    def __init__(self, description="Invalid key."):
        self.description = description
        super().__init__(description)


class UnhandledError(Exception):
    def __init__(self, description="Unhandled error."):
        self.description = description
        super().__init__(description)

class SignatureFailed(Exception):
    def __init__(self, description="Signature failed."):
        self.description = description
        super().__init__(description)


class CryptoUtils:
    @staticmethod
    def generate_rsa_keys():
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            public_key = private_key.public_key()

            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()

            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

            return private_pem, public_pem
        except Exception as e:
            raise UnhandledError(str(e))

    @staticmethod
    def load_private_key(private_key_data: str):
        try:
            return serialization.load_pem_private_key(private_key_data.encode(), password=None)
        except Exception as e:
            raise InvalidKey(str(e))

    @staticmethod
    def load_public_key(public_key_data: str):
        try:
            return serialization.load_pem_public_key(public_key_data.encode())
        except Exception as e:
            raise InvalidKey(str(e))

    @staticmethod
    def generate_signature(message, private_key: rsa.RSAPrivateKey):
        try:
            signature_bytes = private_key.sign(
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            signature_str = base64.b64encode(signature_bytes).decode()
            return signature_str
        except Exception as e:
            raise SignatureFailed(str(e))
        

    @staticmethod
    def verify_with_public_key(signed_data: str, signed_key: bytes | str, public_key: rsa.RSAPublicKey):
        try:

            if not isinstance(signed_data, bytes):
                signed_data = signed_data.encode()
            if isinstance(signed_key, str):
                signed_key = base64.b64decode(signed_key)

            try:
                public_key.verify(
                    signature=signed_key,
                    data=signed_data,
                    padding=padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    algorithm=hashes.SHA256()
                )
                return True
            except InvalidSignature:
                return False
        except Exception as e:
            raise SignatureFailed(str(e))
        



    @staticmethod
    def encrypt_with_public_key(encrypted_data: str | bytes, public_key: rsa.RSAPublicKey):
        try:
            if not isinstance(encrypted_data, bytes):
                encrypted_data = bytes(encrypted_data, 'utf-8')

            encrypted_data = public_key.encrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_data_str = base64.b64encode(encrypted_data).decode()
            return encrypted_data_str
        except Exception as e:
            raise EncryptFailed(str(e))


    @staticmethod
    def decrypt_with_private_key(encrypted_data: str | bytes, private_key: rsa.RSAPrivateKey):
        try:
            if not isinstance(encrypted_data, bytes):
                encrypted_data = base64.b64decode(encrypted_data)

            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return decrypted_data.decode()
        except Exception as e:
            raise DecryptFailed(str(e))


class EncryptionUtils:
    
    @staticmethod
    def generate_key():
        key = Fernet.generate_key()
        return key.decode()
    
    @staticmethod
    def encrypt_message(message: str, key: str) -> str:
        try:
            fernet = Fernet(key)
            encrypted_message = fernet.encrypt(message.encode("utf-8"))
            return encrypted_message.decode()
        except Exception as e:
            raise EncryptFailed(str(e))

    @staticmethod
    def decrypt_message(encrypted_message: str, key: str) -> str:
        try:
            fernet = Fernet(key.encode())
            decrypted_message = fernet.decrypt(encrypted_message).decode()
            return decrypted_message
        except Exception as e:
            raise DecryptFailed(str(e))
        
class JwtUtils:
    @staticmethod
    def encrypt_jwt(payload, key, expire_seconds=3600):
        current_time = time.time()
        expire_time = current_time + expire_seconds
        payload['exp'] = expire_time
        return jwt.encode(payload, key, algorithm='HS256')

    @staticmethod
    def decrypt_jwt(encoded_jwt, key):
        try:
            return jwt.decode(encoded_jwt, key, algorithms=['HS256'])
        except Exception as e:
            raise DecryptFailed(str(e))

    