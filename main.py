import json
import random
import string
import threading
from concurrent.futures import ThreadPoolExecutor
from src import PumpFunListener, ProxyManager, SolanaWallet, PumpFunAuth, PumpFunComment, create_session, log

log.clear()

with open("config.json", "r") as f:
    config = json.load(f)

proxy_manager = ProxyManager("proxies.txt")

executor = ThreadPoolExecutor(max_workers=config.get("max_workers", 200))


def generate_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    numbers = ''.join(random.choices(string.digits, k=3))
    return f"#{letters}{numbers}"


def run_task(mint: str, task_id: int):
    wallet = SolanaWallet()

    if not wallet.is_valid():
        log.task_done(mint, False)
        return

    session = create_session(proxy_manager, task_id)
    auth = PumpFunAuth(wallet, session)
    login_result = auth.login()

    if not login_result["success"]:
        log.task_done(mint, False)
        return

    commenter = PumpFunComment(session)
    selected_text = random.choice(config["ad_messages"])
    comment_result = commenter.post(mint=mint, text=f"{selected_text} {generate_id()}")

    log.task_done(mint, comment_result["success"])


def worker(mint):
    messages_per_coin = config.get("messages_per_coin", 50)
    log.new_coin(mint, messages_per_coin)
    for i in range(messages_per_coin):
        executor.submit(run_task, mint, i)


def on_new_coin(coin):
    mint = coin.get("mint", "")
    worker(mint)


def run_listener():
    listener = PumpFunListener()
    listener.listen(callback=on_new_coin)


def main():
    log.banner("PumpFun Advertiser Made by: https://t.me/xeverbound")
    log.success(f"Loaded {proxy_manager.count()} proxies")
    log.info("Press Ctrl+C to exit")
    log.divider()

    listener_thread = threading.Thread(target=run_listener, daemon=True)
    listener_thread.start()

    try:
        listener_thread.join()
    except KeyboardInterrupt:
        log.warning("Shutting down...")


if __name__ == "__main__":
    main()
