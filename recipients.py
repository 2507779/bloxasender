import pandas as pd
import tkinter as tk
from tkinter import filedialog

class RecipientManager:
    def __init__(self):
        self.recipients = pd.DataFrame(columns=["id", "name", "tags", "group"])

    def import_from_file_gui(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.import_from_file(file_path)

    def import_from_file(self, file_path):
        if file_path.endswith(".csv"):
            self.recipients = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            self.recipients = pd.read_excel(file_path)

    def export_to_file_gui(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.export_to_file(file_path)

    def export_to_file(self, file_path):
        self.recipients.to_csv(file_path, index=False)

    def get_filtered_recipients(self, filter_str):
        if not filter_str:
            return self.recipients.to_dict("records")
        return self.recipients[
            self.recipients["tags"].str.contains(filter_str, na=False) |
            self.recipients["group"].str.contains(filter_str, na=False)
        ].to_dict("records")
