import tkinter as tk
import customtkinter as ctk
from sender import Sender
from scheduler import Scheduler
from templates import TemplateManager
from recipients import RecipientManager
from reports import ReportGenerator
from config import save_config
import logging

class BloXaSenderGUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.root.title("BloXaSender")
        self.root.geometry("1400x800")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        # Настройка логирования
        logging.basicConfig(filename=self.config.get("log_file", "bloxasender.log"), level=logging.INFO)

        # Инициализация компонентов
        self.sender = Sender(config)
        self.scheduler = Scheduler(self.sender)
        self.templates = TemplateManager()
        self.recipients = RecipientManager()
        self.reports = ReportGenerator()

        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Создание интерфейса
        self.create_settings_panel()
        self.create_recipients_panel()
        self.create_templates_panel()
        self.create_scheduler_panel()
        self.create_chains_panel()
        self.create_reports_panel()
        self.create_send_panel()
        self.create_instructions_panel()  # Новая вкладка с инструкцией

    def create_settings_panel(self):
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.pack(side="left", fill="y", padx=5)

        ctk.CTkLabel(settings_frame, text="Настройки").pack(pady=5)

        self.account_list = ctk.CTkOptionMenu(settings_frame, values=[f"Аккаунт {i+1}" for i in range(len(self.config["accounts"]))] or ["Нет аккаунтов"])
        self.account_list.pack(pady=5)
        self.api_id_entry = ctk.CTkEntry(settings_frame, placeholder_text="API ID")
        self.api_id_entry.pack(pady=5)
        self.api_hash_entry = ctk.CTkEntry(settings_frame, placeholder_text="API Hash")
        self.api_hash_entry.pack(pady=5)
        self.phone_entry = ctk.CTkEntry(settings_frame, placeholder_text="Phone")
        self.phone_entry.pack(pady=5)
        ctk.CTkButton(settings_frame, text="Добавить аккаунт", command=self.add_account).pack(pady=5)

        self.bot_token_entry = ctk.CTkEntry(settings_frame, placeholder_text="Bot Token")
        self.bot_token_entry.insert(0, self.config.get("bot_token", ""))
        self.bot_token_entry.pack(pady=5)
        self.proxy_entry = ctk.CTkEntry(settings_frame, placeholder_text="Proxy (host:port)")
        self.proxy_entry.insert(0, self.config.get("proxy", ""))
        self.proxy_entry.pack(pady=5)

        ctk.CTkButton(settings_frame, text="Сохранить", command=self.save_settings).pack(pady=10)

    def create_recipients_panel(self):
        rec_frame = ctk.CTkFrame(self.main_frame)
        rec_frame.pack(side="left", fill="y", padx=5)

        ctk.CTkLabel(rec_frame, text="Получатели").pack(pady=5)
        self.import_btn = ctk.CTkButton(rec_frame, text="Импорт", command=self.recipients.import_from_file_gui)
        self.import_btn.pack(pady=5)
        self.export_btn = ctk.CTkButton(rec_frame, text="Экспорт", command=self.recipients.export_to_file_gui)
        self.export_btn.pack(pady=5)
        self.filter_entry = ctk.CTkEntry(rec_frame, placeholder_text="Фильтр (тег или группа)")
        self.filter_entry.pack(pady=5)
        self.recipients_list = ctk.CTkTextbox(rec_frame, height=200)
        self.recipients_list.pack(pady=5)

    def create_templates_panel(self):
        temp_frame = ctk.CTkFrame(self.main_frame)
        temp_frame.pack(side="left", fill="y", padx=5)

        ctk.CTkLabel(temp_frame, text="Шаблоны").pack(pady=5)
        self.template_name = ctk.CTkEntry(temp_frame, placeholder_text="Название шаблона")
        self.template_name.pack(pady=5)
        self.template_content = ctk.CTkTextbox(temp_frame, height=100)
        self.template_content.pack(pady=5)
        ctk.CTkButton(temp_frame, text="Добавить", command=self.add_template).pack(pady=5)

    def create_scheduler_panel(self):
        sched_frame = ctk.CTkFrame(self.main_frame)
        sched_frame.pack(side="left", fill="y", padx=5)

        ctk.CTkLabel(sched_frame, text="Планировщик").pack(pady=5)
        self.schedule_time = ctk.CTkEntry(sched_frame, placeholder_text="HH:MM")
        self.schedule_time.pack(pady=5)
        self.schedule_days = ctk.CTkOptionMenu(sched_frame, values=["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс", "Ежедневно"])
        self.schedule_days.pack(pady=5)
        ctk.CTkButton(sched_frame, text="Запланировать", command=self.schedule_message).pack(pady=5)

    def create_chains_panel(self):
        chain_frame = ctk.CTkFrame(self.main_frame)
        chain_frame.pack(side="left", fill="y", padx=5)

        ctk.CTkLabel(chain_frame, text="Цепочки").pack(pady=5)
        self.chain_name = ctk.CTkEntry(chain_frame, placeholder_text="Название цепочки")
        self.chain_name.pack(pady=5)
        self.chain_delay = ctk.CTkEntry(chain_frame, placeholder_text="Задержка (сек)")
        self.chain_delay.pack(pady=5)
        ctk.CTkButton(chain_frame, text="Добавить в цепочку", command=self.add_to_chain).pack(pady=5)

    def create_reports_panel(self):
        rep_frame = ctk.CTkFrame(self.main_frame)
        rep_frame.pack(side="left", fill="y", padx=5)

        ctk.CTkLabel(rep_frame, text="Отчеты").pack(pady=5)
        ctk.CTkButton(rep_frame, text="Сгенерировать PDF", command=self.generate_report).pack(pady=5)

    def create_send_panel(self):
        send_frame = ctk.CTkFrame(self.main_frame)
        send_frame.pack(side="top", fill="x", pady=10)

        self.message_content = ctk.CTkTextbox(send_frame, height=100)
        self.message_content.pack(pady=5)
        self.media_path = ctk.CTkEntry(send_frame, placeholder_text="Путь к медиа")
        self.media_path.pack(pady=5)
        self.delete_after = ctk.CTkEntry(send_frame, placeholder_text="Удалить через (сек)")
        self.delete_after.pack(pady=5)
        self.method_var = ctk.CTkOptionMenu(send_frame, values=["API", "Bot", "Selenium"])
        self.method_var.pack(pady=5)
        ctk.CTkButton(send_frame, text="Тест", command=self.test_message).pack(pady=5)
        ctk.CTkButton(send_frame, text="Отправить", command=self.send_message).pack(pady=5)

    def create_instructions_panel(self):
        inst_frame = ctk.CTkFrame(self.main_frame)
        inst_frame.pack(side="left", fill="y", padx=5)

        ctk.CTkLabel(inst_frame, text="Инструкция").pack(pady=5)
        instructions_text = ctk.CTkTextbox(inst_frame, height=400, width=300)
        instructions_text.pack(pady=5)
        instructions_text.insert("1.0", self.get_instructions())
        instructions_text.configure(state="disabled")  # Только для чтения

    def get_instructions(self):
        return """
        Инструкция по установке и использованию BloXaSender

        === УСТАНОВКА НА WINDOWS ===

        1. УСТАНОВКА PYTHON
        - Перейдите на сайт https://www.python.org/downloads/.
        - Скачайте последнюю версию Python (рекомендуется 3.9 или выше).
        - Запустите установочный файл (.exe).
        - В установщике отметьте галочку "Add Python to PATH" и выберите "Install Now".
        - После установки откройте командную строку (cmd) и введите `python --version`, чтобы проверить установку.

        2. СКАЧИВАНИЕ ПРОГРАММЫ
        - Сохраните все файлы программы (main.py, gui.py, sender.py и т.д.) в одну папку, например, "C:\\BloXaSender".
        - Убедитесь, что файл requirements.txt тоже в этой папке.

        3. УСТАНОВКА ЗАВИСИМОСТЕЙ
        - Откройте командную строку (Win + R, введите "cmd", нажмите Enter).
        - Перейдите в папку программы: `cd C:\\BloXaSender`.
        - Установите зависимости: `pip install -r requirements.txt`.
        - Дождитесь завершения установки всех библиотек.

        4. УСТАНОВКА CHROMEDRIVER (ДЛЯ SELENIUM)
        - Библиотека `chromedriver-autoinstaller` автоматически установит подходящий chromedriver.
        - Убедитесь, что Google Chrome установлен на вашем компьютере (скачать можно с https://www.google.com/chrome/).

        5. ПРОВЕРКА УСТАНОВКИ
        - В командной строке в папке программы введите: `python main.py`.
        - Если окно программы открылось, установка прошла успешно.

        === ИСПОЛЬЗОВАНИЕ ===

        1. НАСТРОЙКА
        - В разделе "Настройки" добавьте Telegram-аккаунты:
          * API ID и API Hash: получите на https://my.telegram.org.
          * Phone: номер телефона аккаунта (например, +79991234567).
          * Нажмите "Добавить аккаунт".
        - Укажите Bot Token (получите через @BotFather), если используете Bot API.
        - Введите прокси (host:port), если требуется.
        - Нажмите "Сохранить".

        2. ПОЛУЧАТЕЛИ
        - Нажмите "Импорт" и выберите CSV-файл (колонки: id, name, tags, group).
        - Используйте "Фильтр" для выбора получателей по тегам или группам.
        - Экспортируйте список через "Экспорт".

        3. ШАБЛОНЫ
        - Введите название и текст шаблона (например, "Привет, {name}! Теги: {tags}").
        - Нажмите "Добавить". Шаблон "default" используется для персонализации.

        4. ПЛАНИРОВЩИК
        - Укажите время (HH:MM) и день недели.
        - Нажмите "Запланировать" для отложенной рассылки.

        5. ЦЕПОЧКИ
        - Введите название цепочки и задержку (в секундах).
        - Добавьте сообщение в цепочку через "Добавить в цепочку".

        6. ОТПРАВКА
        - Напишите сообщение или выберите шаблон.
        - Укажите путь к файлу (фото, видео, документ) в "Путь к медиа".
        - Задайте время удаления (в секундах) в "Удалить через".
        - Выберите метод (API, Bot, Selenium).
        - Нажмите "Тест" для проверки на своем аккаунте.
        - Нажмите "Отправить" для рассылки.

        7. ОТЧЕТЫ
        - Нажмите "Сгенерировать PDF" для создания отчета.

        Примечания:
        - Логи сохраняются в bloxasender.log.
        - Для Selenium нужен Chrome и chromedriver.
        """

    def add_account(self):
        account = {
            "api_id": self.api_id_entry.get(),
            "api_hash": self.api_hash_entry.get(),
            "phone": self.phone_entry.get()
        }
        self.config["accounts"].append(account)
        self.account_list.configure(values=[f"Аккаунт {i+1}" for i in range(len(self.config["accounts"]))])
        self.save_settings()

    def save_settings(self):
        self.config["bot_token"] = self.bot_token_entry.get()
        self.config["proxy"] = self.proxy_entry.get()
        self.sender.update_config(self.config)
        save_config(self.config)
        logging.info("Настройки сохранены")

    def add_template(self):
        name = self.template_name.get()
        content = self.template_content.get("1.0", tk.END).strip()
        self.templates.add_template(name, content)
        logging.info(f"Добавлен шаблон: {name}")

    def schedule_message(self):
        time = self.schedule_time.get()
        day = self.schedule_days.get()
        message = self.message_content.get("1.0", tk.END).strip()
        recipients = self.recipients.get_filtered_recipients(self.filter_entry.get())
        for recipient in recipients:
            self.scheduler.add_job(recipient["id"], message, time, day)
        logging.info(f"Запланирована рассылка на {time} ({day})")

    def add_to_chain(self):
        chain_name = self.chain_name.get()
        delay = int(self.chain_delay.get() or 0)
        message = self.message_content.get("1.0", tk.END).strip()
        self.scheduler.add_chain(chain_name, message, delay)
        logging.info(f"Добавлено в цепочку {chain_name}: задержка {delay} сек")

    def test_message(self):
        message = self.message_content.get("1.0", tk.END).strip()
        media = self.media_path.get() or None
        self.sender.send_message("me", message, media=media, method=self.method_var.get().lower())
        logging.info("Тестовое сообщение отправлено")

    def send_message(self):
        message = self.message_content.get("1.0", tk.END).strip()
        media = self.media_path.get() or None
        delete_after = int(self.delete_after.get() or 0)
        method = self.method_var.get()
        recipients = self.recipients.get_filtered_recipients(self.filter_entry.get())
        for recipient in recipients:
            personalized_msg = self.templates.get_randomized_message("default", recipient) if "default" in self.templates else message
            self.sender.send_message(recipient["id"], personalized_msg, media=media, method=method.lower(), delete_after=delete_after)
        logging.info(f"Рассылка выполнена: {len(recipients)} получателей")

    def generate_report(self):
        self.reports.generate_pdf({"sent": len(self.recipients.recipients)}, "report.pdf")
        logging.info("Отчет сгенерирован")
