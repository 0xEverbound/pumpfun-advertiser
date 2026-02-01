import tls_client
from .proxy import ProxyManager

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"


def create_session(proxy_manager: ProxyManager = None, proxy_index: int = None) -> tls_client.Session:

    session = tls_client.Session(
        client_identifier="chrome_133",
        random_tls_extension_order=True
    )

    session.headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://pump.fun",
        "Referer": "https://pump.fun/",
        "User-Agent": USER_AGENT,
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
    }

    if proxy_manager and proxy_index is not None:
        try:
            proxy_dict = proxy_manager.get(proxy_index)
            if proxy_dict:
                session.proxies = proxy_dict
        except Exception:
            pass

    return session
