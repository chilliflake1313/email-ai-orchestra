from core.imap_client import IMAPClient
import os


class ReaderAgent:
    def __init__(self, email_address=None, password=None, server=None, port=993):
        self.email_address = email_address or os.getenv('EMAIL_ADDRESS')
        self.password = password or os.getenv('EMAIL_PASSWORD')
        self.server = server or os.getenv('IMAP_SERVER', 'imap.gmail.com')
        self.port = int(os.getenv('IMAP_PORT', port))

    def fetch_emails(self, limit=50):
        with IMAPClient(self.email_address, self.password, self.server, self.port) as client:
            emails = client.fetch_recent_emails(limit)
        return emails

    def get_email_count(self):
        with IMAPClient(self.email_address, self.password, self.server, self.port) as client:
            client.select_folder('INBOX')
            _, message_numbers = client.connection.search(None, 'ALL')
            email_ids = message_numbers[0].split()
            return len(email_ids)
