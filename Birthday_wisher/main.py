from datetime import datetime
from pathlib import Path
import pandas as pd
import random
import smtplib
from email.message import EmailMessage

MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = "YOUR PASSWORD"

def get_today_tuple():
    now = datetime.now()
    return now.month, now.day

def load_birthdays(path="birthdays.csv"):
    df = pd.read_csv(path)
    return {(row["month"], row["day"]): row for _, row in df.iterrows()}

def generate_letter(name):
    template = Path("letter_templates").joinpath(f"letter_{random.randint(1,3)}.txt")
    content = template.read_text()
    return content.replace("[NAME]", name)

def send_email(recipient, content):
    msg = EmailMessage()
    msg["Subject"] = "Happy Birthday!"
    msg["From"] = MY_EMAIL
    msg["To"] = recipient
    msg.set_content(content)

    with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as smtp:
        smtp.starttls()
        smtp.login(MY_EMAIL, MY_PASSWORD)
        smtp.send_message(msg)

def main():
    today = get_today_tuple()
    birthdays = load_birthdays()
    if today in birthdays:
        person = birthdays[today]
        letter = generate_letter(person["name"])
        send_email(person["email"], letter)

if __name__ == "__main__":
    main()
