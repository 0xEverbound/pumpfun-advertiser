import tls_client





class PumpFunComment:
    API_BASE = "https://frontend-api-v3.pump.fun"

    def __init__(self, session: tls_client.Session):
        self.session = session

    def post(self, mint: str, text: str) -> dict:
        try:
            self.session.headers["Referer"] = f"https://pump.fun/coin/{mint}"

            payload = {
                "text": text,
                "mint": mint
            }

            response = self.session.post(
                f"{self.API_BASE}/replies",
                json=payload,
                timeout_seconds=30
            )


            if response.status_code in [200, 201]:
                return {"success": True}

            if "<!DOCTYPE" in response.text or "<html" in response.text:
                return {"success": False, "error": "Blocked by Cloudflare"}

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
