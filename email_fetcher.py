# email_fetcher.py
import imaplib
import email
from datetime import datetime
from reminder import Reminder

class EmailFetcher:
    def __init__(self, email_user, email_pass, imap_server="imap.gmail.com"):
        self.email_user = email_user
        self.email_pass = email_pass
        self.imap_server = imap_server
        self.mail = None

    def connect(self):
        """Connect to Gmail using IMAP"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_user, self.email_pass)
            self.mail.select("inbox")
            print("[Connected to Gmail ✅]")
            return True
        except Exception as e:
            print(f"[Error] Cannot connect to mailbox: {e}")
            return False

    def get_deadline_emails(self):
        """Fetch emails mentioning deadlines or job applications"""
        if not self.mail:
            if not self.connect():
                return []

        keywords = ["deadline", "submission", "job application", "apply by", "last date"]
        results = []

        try:
            _, search_data = self.mail.search(None, "ALL")
            for num in search_data[0].split()[-10:]:  # last 10 emails
                _, data = self.mail.fetch(num, "(RFC822)")
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                subject = msg["subject"] or ""
                sender = msg["from"] or ""
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body += part.get_payload(decode=True).decode(errors="ignore")
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                for key in keywords:
                    if key.lower() in subject.lower() or key.lower() in body.lower():
                        results.append({
                            "subject": subject,
                            "sender": sender,
                            "body": body[:300],
                        })
                        break

            print(f"[EmailFetcher] Found {len(results)} relevant emails.")
        except Exception as e:
            print(f"[Error fetching emails] {e}")

        return results
