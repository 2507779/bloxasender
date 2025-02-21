from telethon import TelegramClient
from telegram.ext import ApplicationBuilder
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

class Sender:
    def __init__(self, config):
        self.config = config
        self.clients = {}
        self.bot = None
        self.driver = None
        self.current_account = 0
        self.init_clients()

    def update_config(self, config):
        self.config = config
        self.init_clients()

    def init_clients(self):
        if self.clients:
            for client in self.clients.values():
                client.disconnect()
        if self.bot:
            self.bot = None
        if self.driver:
            self.driver.quit()

        for i, acc in enumerate(self.config.get("accounts", [])):
            proxy = self.config.get("proxy")
            if proxy:
                host, port = proxy.split(":")
                proxy_dict = {"proxy_type": "http", "addr": host, "port": int(port)}
                self.clients[i] = TelegramClient(f"session_{i}", acc["api_id"], acc["api_hash"], proxy=proxy_dict)
            else:
                self.clients[i] = TelegramClient(f"session_{i}", acc["api_id"], acc["api_hash"])
            self.clients[i].start(phone=acc["phone"])

        if self.config.get("bot_token"):
            self.bot = ApplicationBuilder().token(self.config["bot_token"]).build()

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)

    def send_message(self, recipient, message, media=None, method="api", delete_after=0):
        try:
            if method == "api" and self.clients:
                client = self.clients[self.current_account]
                msg = client.loop.run_until_complete(client.send_message(recipient, message, file=media))
                if delete_after:
                    time.sleep(delete_after)
                    client.loop.run_until_complete(client.delete_messages(recipient, [msg.id]))
            elif method == "bot" and self.bot:
                msg = self.bot.bot.send_message(chat_id=recipient, text=message)
                if media and os.path.exists(media):
                    with open(media, "rb") as f:
                        self.bot.bot.send_document(chat_id=recipient, document=f)
                if delete_after:
                    time.sleep(delete_after)
                    self.bot.bot.delete_message(chat_id=recipient, message_id=msg.message_id)
            elif method == "selenium":
                self.selenium_send(recipient, message, media)
                if delete_after:
                    time.sleep(delete_after)
                    # Логика удаления через Selenium сложнее, пропустим для простоты
        except Exception as e:
            print(f"Ошибка отправки: {e}")

    def selenium_send(self, recipient, message, media):
        self.driver.get("https://web.telegram.org")
        time.sleep(5)
        search = self.driver.find_element(By.XPATH, "//input[@placeholder='Search']")
        search.send_keys(recipient)
        search.send_keys(Keys.ENTER)
        time.sleep(2)
        input_box = self.driver.find_element(By.XPATH, "//div[@contenteditable='true']")
        input_box.send_keys(message)
        input_box.send_keys(Keys.ENTER)
        if media and os.path.exists(media):
            attach_btn = self.driver.find_element(By.XPATH, "//button[@title='Attach']")
            attach_btn.click()
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(os.path.abspath(media))
            time.sleep(2)
