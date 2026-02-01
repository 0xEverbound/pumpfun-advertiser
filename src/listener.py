import json
import ssl
import uuid
import websocket
from .auth import PumpFunAuth
from .logger import log

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"


class PumpFunListener:
    WS_URL = "wss://prod-v2.nats.realtime.pump.fun/"
    NATS_USER = "subscriber"
    NATS_PASS = "lW5a9y20NceF6AE9"

    def __init__(self, auth: PumpFunAuth = None):
        self.auth = auth
        self.seen_tokens = set()
        self.callback = None
        self.ws = None
        self.running = False
        self.user_agent = USER_AGENT

    def _generate_sentry_trace_id(self):
        return uuid.uuid4().hex

    def _get_headers(self):
        trace_id = self._generate_sentry_trace_id()
        span_id = uuid.uuid4().hex[:16]

        headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "baggage": f"sentry-environment=production,sentry-release=1.24.2,sentry-public_key=5838a5520ad44602ae46793727e49ef5,sentry-trace_id={trace_id}",
            "Cache-Control": "no-cache",
            "Origin": "https://pump.fun",
            "Pragma": "no-cache",
            "sentry-trace": f"{trace_id}-{span_id}",
            "User-Agent": self.user_agent,
        }

        if self.auth and self.auth.session.cookies:
            cookie_str = "; ".join([f"{c.name}={c.value}" for c in self.auth.session.cookies])
            if cookie_str:
                headers["Cookie"] = cookie_str

        return headers

    def _on_message(self, ws, message):
        try:
            if isinstance(message, bytes):
                message = message.decode("utf-8")

            if message.startswith("MSG "):
                lines = message.split("\r\n", 1)
                if len(lines) >= 2:
                    payload = lines[1].strip()
                    if payload:
                        coin = json.loads(payload)
                        mint = coin.get("mint")
                        if mint and mint not in self.seen_tokens:
                            self.seen_tokens.add(mint)
                            if self.callback:
                                self.callback(coin)
                            else:
                                self._print_coin(coin)

            elif message.startswith("PING"):
                ws.send("PONG\r\n")

        except json.JSONDecodeError:
            pass
        except Exception as e:
            log.error(f"Error processing message: {e}")

    def _on_error(self, ws, error):
        log.error(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        log.warning("WebSocket closed")
        self.running = False

    def _on_open(self, ws):
        log.success("Connected to pump.fun realtime feed")

        connect_msg = json.dumps({
            "no_responders": True,
            "protocol": 1,
            "verbose": False,
            "pedantic": False,
            "user": self.NATS_USER,
            "pass": self.NATS_PASS,
            "lang": "nats.ws",
            "version": "1.30.3",
            "headers": True
        })
        ws.send(f"CONNECT {connect_msg}\r\n")
        ws.send("PING\r\n")
        ws.send("SUB newCoinCreated.prod 1\r\n")
        log.success("Subscribed to newCoinCreated.prod")
        log.divider()

    def _print_coin(self, coin):
        mint = coin.get("mint", "")
        log.info(f"New coin: {mint[:8]}...{mint[-4:]}")

    def listen(self, callback=None):
        self.callback = callback
        self.running = True

        headers = self._get_headers()

        self.ws = websocket.WebSocketApp(
            self.WS_URL,
            header=headers,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )

        log.info("Starting listener...")
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()


if __name__ == "__main__":
    listener = PumpFunListener()
    try:
        listener.listen()
    except KeyboardInterrupt:
        listener.stop()
