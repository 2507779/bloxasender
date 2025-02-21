import tkinter as tk
from gui import BloXaSenderGUI
from config import load_config, save_config

def main():
    # Загрузка или создание конфигурации
    config = load_config()
    if not config:
        config = {
            "accounts": [],  # Список аккаунтов: [{"api_id": "", "api_hash": "", "phone": ""}]
            "bot_token": "",
            "proxy": "",
            "log_file": "bloxasender.log"
        }

    # Инициализация основного окна
    root = tk.Tk()
    app = BloXaSenderGUI(root, config)
    root.mainloop()

if __name__ == "__main__":
    main()
