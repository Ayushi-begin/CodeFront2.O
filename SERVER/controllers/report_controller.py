from config.db import report_db

def save_report(report_data):
    reports = report_db["reports"]
    reports.insert_one(report_data)
    print("✅ Report stored successfully.")
