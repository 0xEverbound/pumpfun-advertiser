import time
import tls_client
from .wallet import SolanaWallet


class PumpFunAuth:
    API_BASE = "https://frontend-api-v3.pump.fun"

    def __init__(self, wallet: SolanaWallet, session: tls_client.Session):
        self.wallet = wallet
        self.session = session
        self.token = None

    def login(self) -> dict:
        try:
            if not self.wallet.is_valid():
                return {"success": False, "error": "Invalid wallet"}

            timestamp = int(time.time() * 1000)
            message = f"Sign in to pump.fun: {timestamp}"
            signature = self.wallet.sign(message)

            if not signature:
                return {"success": False, "error": "Failed to sign message"}

            payload = {
                "address": self.wallet.public_key,
                "signature": signature,
                "timestamp": timestamp
            }

            response = self.session.post(
                f"{self.API_BASE}/auth/login",
                json=payload,
                timeout_seconds=30
            )

            if response.status_code in [200, 201]:
                self.token = response.cookies.get("auth_token")
                if self.token:
                    self.session.cookies.set("auth_token", self.token, domain=".pump.fun")
                return {"success": True}

            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            error_msg = str(e).lower()
            if "proxy" in error_msg:
                return {"success": False, "error": "Proxy error"}
            elif "timeout" in error_msg:
                return {"success": False, "error": "Timeout"}
            elif "connection" in error_msg:
                return {"success": False, "error": "Connection error"}
            return {"success": False, "error": str(e)}

    def get_profile(self) -> dict:
        try:
            response = self.session.get(
                f"{self.API_BASE}/auth/my-profile",
                timeout_seconds=30
            )
            return {"success": response.status_code == 200}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def is_authenticated(self) -> bool:
        return self.token is not None
