import sys
from .logger import log


class ProxyManager:
    def __init__(self, filepath: str = "proxies.txt"):
        self.proxies = []
        self.errors = []
        self.filepath = filepath
        self._load_and_validate(filepath)

    def _load_and_validate(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            log.error(f"{filepath} not found")
            log.info("Create proxies.txt with your proxies (see proxies.example.txt)")
            sys.exit(1)

        for i, line in enumerate(lines, 1):
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            parsed = self._parse_proxy(line, i)
            if parsed:
                self.proxies.append(parsed)

        if self.errors:
            log.error("Invalid proxy format detected:")
            for err in self.errors:
                log.error(f"  {err}")
            log.info("See proxies.example.txt for supported formats")
            sys.exit(1)

    def _parse_proxy(self, proxy: str, line_num: int) -> dict:
        original = proxy
        protocol = "http"

        if proxy.startswith("socks5://"):
            protocol = "socks5"
            proxy = proxy[9:]
        elif proxy.startswith("http://"):
            protocol = "http"
            proxy = proxy[7:]
        elif proxy.startswith("https://"):
            protocol = "http"
            proxy = proxy[8:]

        try:
            if '@' in proxy:
                auth, hostport = proxy.rsplit('@', 1)
                if ':' not in hostport:
                    self.errors.append(f"Line {line_num}: Missing port in '{original}'")
                    return None
                host, port = hostport.rsplit(':', 1)
                if ':' not in auth:
                    self.errors.append(f"Line {line_num}: Invalid auth format in '{original}'")
                    return None
                user, pwd = auth.split(':', 1)
                formatted = f"{protocol}://{user}:{pwd}@{host}:{port}"

            elif proxy.count(':') == 3:
                parts = proxy.split(':')
                host, port, user, pwd = parts[0], parts[1], parts[2], parts[3]
                formatted = f"{protocol}://{user}:{pwd}@{host}:{port}"

            elif proxy.count(':') == 1:
                host, port = proxy.split(':')
                formatted = f"{protocol}://{host}:{port}"

            else:
                self.errors.append(f"Line {line_num}: Invalid format '{original}'")
                return None

            if not port.isdigit():
                self.errors.append(f"Line {line_num}: Port must be numeric in '{original}'")
                return None

            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                self.errors.append(f"Line {line_num}: Port must be 1-65535 in '{original}'")
                return None

            if not host or host.isspace():
                self.errors.append(f"Line {line_num}: Invalid host in '{original}'")
                return None

            return {
                "http": formatted,
                "https": formatted,
                "raw": original
            }

        except Exception as e:
            self.errors.append(f"Line {line_num}: Failed to parse '{original}'")
            return None

    def get(self, index: int) -> dict:
        if not self.proxies:
            return None
        proxy = self.proxies[index % len(self.proxies)]
        return {"http": proxy["http"], "https": proxy["https"]}

    def get_raw(self, index: int) -> str:
        if not self.proxies:
            return None
        return self.proxies[index % len(self.proxies)]["raw"]

    def count(self) -> int:
        return len(self.proxies)
