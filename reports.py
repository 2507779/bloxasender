from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ReportGenerator:
    def generate_pdf(self, data, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, "Отчет по рассылке BloXaSender")
        c.drawString(100, 730, f"Отправлено сообщений: {data.get('sent', 0)}")
        c.save()
