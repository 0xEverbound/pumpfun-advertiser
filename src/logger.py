import os
import sys
import threading
from datetime import datetime

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CLEAR_LINE = "\033[2K\r"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"


class Logger:
    def __init__(self):
        self._enable_windows_ansi()
        self.coin_stats = {}
        self.current_coin = None
        self.lock = threading.Lock()

    def _enable_windows_ansi(self):
        if sys.platform == "win32":
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception:
                pass

    def _timestamp(self):
        return datetime.now().strftime("%H:%M:%S")

    def info(self, msg):
        ts = self._timestamp()
        print(f"{Colors.DIM}{ts}{Colors.RESET} {Colors.BLUE}│{Colors.RESET} {msg}")

    def success(self, msg):
        ts = self._timestamp()
        print(f"{Colors.DIM}{ts}{Colors.RESET} {Colors.GREEN}✓{Colors.RESET} {msg}")

    def error(self, msg):
        ts = self._timestamp()
        print(f"{Colors.DIM}{ts}{Colors.RESET} {Colors.RED}✗{Colors.RESET} {Colors.RED}{msg}{Colors.RESET}")

    def warning(self, msg):
        ts = self._timestamp()
        print(f"{Colors.DIM}{ts}{Colors.RESET} {Colors.YELLOW}!{Colors.RESET} {Colors.YELLOW}{msg}{Colors.RESET}")

    def new_coin(self, mint, target):
        with self.lock:
            self.current_coin = mint
            self.coin_stats[mint] = {"success": 0, "failed": 0, "target": target, "done": False}
            self._render_current()

    def task_done(self, mint, success):
        with self.lock:
            if mint not in self.coin_stats:
                return

            stats = self.coin_stats[mint]
            if stats["done"]:
                return

            if success:
                stats["success"] += 1
            else:
                stats["failed"] += 1

            if stats["success"] + stats["failed"] >= stats["target"]:
                stats["done"] = True
                self._print_completed(mint)
            elif mint == self.current_coin:
                self._render_current()

    def _render_current(self):
        line = f"{Colors.DIM}{self._timestamp()}{Colors.RESET} {Colors.MAGENTA}◆{Colors.RESET} {Colors.CYAN}{self.current_coin}{Colors.RESET} {Colors.DIM}(commenting in progress){Colors.RESET}"
        print(f"{Colors.CLEAR_LINE}{line}", end="", flush=True)

    def _print_completed(self, mint):
        stats = self.coin_stats[mint]
        success = stats["success"]
        failed = stats["failed"]
        target = stats["target"]

        status = f"{Colors.GREEN}{success}{Colors.RESET}/{Colors.DIM}{target}{Colors.RESET}"
        if failed >= 10:
            status += f" {Colors.RED}({failed} failed){Colors.RESET}"

        url = f"https://pump.fun/coin/{mint}"
        completed_line = f"{Colors.DIM}{self._timestamp()}{Colors.RESET} {Colors.GREEN}✓{Colors.RESET} {Colors.CYAN}{url}{Colors.RESET} {status}"
        padding = " " * 50

        if self.current_coin and not self.coin_stats[self.current_coin]["done"]:
            progress_line = f"{Colors.DIM}{self._timestamp()}{Colors.RESET} {Colors.MAGENTA}◆{Colors.RESET} {Colors.CYAN}{self.current_coin}{Colors.RESET} {Colors.DIM}(commenting in progress){Colors.RESET}"
            print(f"\r{completed_line}{padding}\n{progress_line}", end="", flush=True)
        else:
            print(f"\r{completed_line}{padding}")

    def banner(self, msg):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{msg}{Colors.RESET}\n")

    def divider(self):
        print(f"{Colors.DIM}{'─' * 50}{Colors.RESET}")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


log = Logger()
