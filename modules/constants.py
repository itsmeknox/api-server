import json
from cryptography.hazmat.primitives import serialization

class ServerConfig:
    def __init__(self):
        with open("data/server_config.json", "r") as f:
            self.config = json.load(f)  

        self.PRIVATE_KEY_1_STR: str = self.config["private_key_1"]
        self.PUBLIC_KEY_1_STR: str = self.config["public_key_1"]
        
        self.PUBLIC_KEY_2_STR: str = self.config["public_key_2"]
        self.PRIVATE_KEY_2_STR: str = self.config["private_key_2"]

        self.MASTER_KEY_1 = self.config["master_key_1"]
        self.MASTER_KEY_2 = self.config["master_key_2"]

        self.JWT_SECRET_1 = self.config["jwt_secret_1"]
        self.JWT_SECRET_2 = self.config["jwt_secret_2"] 

        self.HC_ENCRYPTION_KEY = self.config["hc_encryption_key"]
        self.load_rsa_keys()


    def load_rsa_keys(self):
        self.PRIVATE_KEY_1 = serialization.load_pem_private_key(self.PRIVATE_KEY_1_STR.encode(), password=None)
        self.PUBLIC_KEY_1 = serialization.load_pem_public_key(self.PUBLIC_KEY_1_STR.encode())

        self.PRIVATE_KEY_2 = serialization.load_pem_private_key(self.PRIVATE_KEY_2_STR.encode(), password=None)
        self.PUBLIC_KEY_2 = serialization.load_pem_public_key(self.PUBLIC_KEY_2_STR.encode())


with open("data/config.json") as f:
    config = json.load(f)

