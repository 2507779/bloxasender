import schedule
import time
import threading

class Scheduler:
    def __init__(self, sender):
        self.sender = sender
        self.jobs = []
        self.chains = {}
        self.running = False

    def add_job(self, recipient, message, schedule_time, day="Ежедневно"):
        if day == "Ежедневно":
            job = schedule.every().day.at(schedule_time).do(self.sender.send_message, recipient, message)
        else:
            days = {"Пн": schedule.every().monday, "Вт": schedule.every().tuesday, "Ср": schedule.every().wednesday,
                    "Чт": schedule.every().thursday, "Пт": schedule.every().friday, "Сб": schedule.every().saturday,
                    "Вс": schedule.every().sunday}
            job = days[day].at(schedule_time).do(self.sender.send_message, recipient, message)
        self.jobs.append(job)
        if not self.running:
            self.run()

    def add_chain(self, chain_name, message, delay):
        if chain_name not in self.chains:
            self.chains[chain_name] = []
        self.chains[chain_name].append((message, delay))

    def run_chain(self, chain_name, recipient):
        for message, delay in self.chains.get(chain_name, []):
            self.sender.send_message(recipient, message)
            time.sleep(delay)

    def run(self):
        self.running = True
        def run_pending():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        thread = threading.Thread(target=run_pending)
        thread.start()
