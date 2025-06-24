import csv

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 15)
        self.cell(0, 10, "Отчет по активности бота", align="C", ln=True)
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def add_image(self, path):
        self.image(path, x=10, w=180)
        self.ln(10)

class Log_Info :
    def __init__(self, date, tg_id, command) :
        self.date = date
        self.tg_id = tg_id
        self.command = command

    @staticmethod
    def add_to_report(date, tg_id, command) :
        Log_Info(date, tg_id, command).save_report()

    def save_report(self):
        with open('temp/activity.csv', 'a') as csvfile:
            fieldnames = ["Date", "TelegramUserId", "Command"]
            data = {"Date" : self.date, "TelegramUserId" : self.tg_id, "Command" : self.command }
            wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
            wr.writerow(data)

    @staticmethod
    def generate_report() :
        df = pd.read_csv('temp/activity.csv')
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        total_users = len(set(df["TelegramUserId"]))
        total_commands = len(df)
        top_commands = df['Command'].value_counts().head(5)

        plt.style.use("ggplot")

        daily_activity = df.groupby('Date').size()

        plt.figure(figsize=(10, 6))
        top_commands.plot(kind='bar', color='skyblue')
        plt.title("Топ 5 команд")
        plt.xlabel("Команда")
        plt.ylabel("Количество вызовов")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{'temp/graphics'}/top_commands.png")
        plt.close()

        plt.figure(figsize=(10, 6))
        daily_activity.plot(kind='line', marker='o')
        plt.title("Активность по дням")
        plt.xlabel("Дата")
        plt.ylabel("Количество команд")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{'temp/graphics'}/daily_activity.png")
        plt.close()

        pdf = PDF(orientation="P", unit="mm", format="A4")

        pdf.add_font("DejaVu", fname="temp\\fonts\\DejaVuSans.ttf")
        pdf.add_font("DejaVu", style="B", fname="temp\\fonts\\DejaVuSans-Bold.ttf")
        pdf.add_page()

        pdf.set_font("DejaVu", size=12)

        pdf.chapter_title("Общая статистика")
        pdf.cell(0, 10, f"Дата создания отчета: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        pdf.ln(5)
        pdf.cell(0, 10, f"Уникальных пользователей: {total_users}")
        pdf.ln(5)
        pdf.cell(0, 10, f"Общее количество команд: {total_commands}")
        pdf.ln(10)

        pdf.chapter_title("Топ команд")
        for cmd, count in top_commands.items():
            pdf.cell(0, 10, f"- {cmd}: {count} раз")
            pdf.ln(5)

        pdf.add_page()
        pdf.chapter_title("Топ команд")
        pdf.add_image(f"{'temp/graphics'}/top_commands.png")

        pdf.chapter_title("Активность по дням")
        pdf.add_image(f"{'temp/graphics'}/daily_activity.png")

        pdf_output = f"temp/statistic_reports/bot_statistics_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf.output(pdf_output)

        return pdf_output