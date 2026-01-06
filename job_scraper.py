import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

EMAIL_TO = "trishulkumar246@gmail.com"
EMAIL_FROM = "your_gmail@gmail.com"
EMAIL_PASS = "YOUR_GMAIL_APP_PASSWORD"

SEARCH_URLS = [
    "https://www.indeed.com/jobs?q=entry+level+business+analyst&sort=date",
    "https://www.indeed.com/jobs?q=entry+level+supply+chain+analyst&sort=date"
]

H1B_SPONSORS = {
    "Amazon", "Google", "Microsoft", "Deloitte", "EY",
    "KPMG", "PwC", "Accenture", "Infosys", "Cognizant",
    "Capgemini", "IBM", "Oracle"
}

def scrape():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in SEARCH_URLS:
        soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
        for card in soup.select(".job_seen_beacon"):
            title = card.select_one("h2 span")
            company = card.select_one(".companyName")
            location = card.select_one(".companyLocation")
            link = card.select_one("h2 a")

            if not all([title, company, location, link]):
                continue

            if company.text.strip() not in H1B_SPONSORS:
                continue

            jobs.append(
                f"{title.text.strip()}\n"
                f"{company.text.strip()} — {location.text.strip()}\n"
                f"https://www.indeed.com{link['href']}\n"
            )

    return jobs

def send_email(jobs):
    body = "\n\n".join(jobs) if jobs else "No new H1-B eligible roles found today."
    msg = MIMEText(body)
    msg["Subject"] = f"Daily H1B Job List – {datetime.today().strftime('%Y-%m-%d')}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    send_email(scrape())



