<p align="center">
  <img src="https://pump.fun/_next/image?url=%2Flogo.png&w=64&q=75" alt="PumpFun Logo" width="80"/>
</p>

<h1 align="center">PumpFun Advertiser</h1>

![showcase](https://github.com/user-attachments/assets/17780813-0ec5-4358-811d-29bfdebe6b09)

<p align="center">
  <a href="https://t.me/xeverbound"><img src="https://img.shields.io/badge/Telegram-Contact-blue?style=for-the-badge&logo=telegram" alt="Telegram"></a>
</p>



## ⚡ Features

- **Real-time Detection**: Listens for new coin launches via WebSocket
- **Multi-threaded**: Supports up to 200+ concurrent workers
- **Proxy Support**: Rotate through unlimited proxies
- **Auto Wallet Generation**: Creates Solana wallets automatically
- **Customizable Messages**: Configure your own ad messages



## 📁 File Structure

```
pumpfun-advertiser/
├── main.py              # Main entry point
├── config.json          # Configuration file
├── proxies.txt          # Proxy list (one per line)
└── src/
    ├── auth.py          # PumpFun authentication
    ├── comment.py       # Comment posting logic
    ├── listener.py      # WebSocket listener
    ├── logger.py        # Console logging
    ├── proxy.py         # Proxy management
    ├── session.py       # HTTP session handler
    └── wallet.py        # Solana wallet generation
```



## ⚙️ Configuration

Edit `config.json` to customize the tool:

```json
{
    "messages_per_coin": 50,
    "max_workers": 200,
    "ad_messages": [
        "Your ad message here!",
        "Another message variant"
    ]
}
```

| Option | Description |
|--------|-------------|
| `messages_per_coin` | Number of comments to post per new coin |
| `max_workers` | Maximum concurrent threads |
| `ad_messages` | Array of messages (randomly selected) |



## 🚀 Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/0xEverbound/pumpfun-advertiser.git
   cd pumpfun-advertiser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your proxies** to `proxies.txt` (one per line)
   ```
   http://user:pass@ip:port
   http://user:pass@ip:port
   ```

4. **Configure your messages** in `config.json`

5. **Run the tool**
   ```bash
   python main.py
   ```



## 🔄 Proxy Support

For best performance, use rotating residential proxies. The tool supports:
- HTTP/HTTPS/SOCKS5 proxies
- Authenticated proxies (`user:pass@ip:port`)



## ❗ Disclaimer

- **This tool is for educational purposes only. By using it, you acknowledge that I am not liable for any consequences resulting from its use.**

---

<p align="center">
  Made by <a href="https://t.me/xeverbound">@xeverbound</a>
</p>
