import base58
from solders.keypair import Keypair


class SolanaWallet:
    def __init__(self, private_key: str = None):
        try:
            if private_key:
                private_key_bytes = base58.b58decode(private_key)
                self.keypair = Keypair.from_bytes(private_key_bytes)
            else:
                self.keypair = Keypair()

            self.public_key = str(self.keypair.pubkey())
            self.private_key = base58.b58encode(bytes(self.keypair)).decode('utf-8')
            self.error = None
        except Exception as e:
            self.keypair = None
            self.public_key = None
            self.private_key = None
            self.error = str(e)

    def sign(self, message: str) -> str:
        try:
            message_bytes = message.encode('utf-8')
            signature = self.keypair.sign_message(message_bytes)
            return base58.b58encode(bytes(signature)).decode('utf-8')
        except Exception as e:
            return None

    def to_dict(self) -> dict:
        return {
            "public_key": self.public_key,
            "private_key": self.private_key,
            "error": self.error
        }

    def is_valid(self) -> bool:
        return self.keypair is not None
