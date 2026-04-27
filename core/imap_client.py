import imaplib
import email
from email.header import decode_header
from datetime import datetime
import os


class IMAPClient:
    def __init__(self, email_address, password, server, port=993):
        self.email_address = email_address
        self.password = password
        self.server = server
        self.port = port
        self.connection = None

    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.server, self.port)
        self.connection.login(self.email_address, self.password)
        return self

    def disconnect(self):
        if self.connection:
            self.connection.logout()

    def select_folder(self, folder='INBOX'):
        return self.connection.select(folder)

    def fetch_recent_emails(self, limit=50):
        self.select_folder('INBOX')
        
        _, message_numbers = self.connection.search(None, 'ALL')
        email_ids = message_numbers[0].split()
        email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
        email_ids.reverse()
        
        emails = []
        for email_id in email_ids:
            email_data = self._fetch_email_data(email_id)
            if email_data:
                emails.append(email_data)
        
        return emails

    def _fetch_email_data(self, email_id):
        _, msg_data = self.connection.fetch(email_id, '(RFC822)')
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                subject = self._decode_header(msg.get('Subject', ''))
                sender = self._decode_header(msg.get('From', ''))
                date_str = msg.get('Date', '')
                
                body_snippet = self._get_body_snippet(msg)
                
                email_date = self._parse_date(date_str)
                days_old = (datetime.now() - email_date).days if email_date else 0
                
                return {
                    'id': email_id.decode(),
                    'subject': subject,
                    'sender': sender,
                    'date': date_str,
                    'days_old': days_old,
                    'snippet': body_snippet
                }
        
        return None

    def _decode_header(self, header):
        if not header:
            return ''
        
        decoded_parts = decode_header(header)
        decoded_string = ''
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
            else:
                decoded_string += part
        
        return decoded_string

    def _get_body_snippet(self, msg, max_length=200):
        body = ''
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = ''
        
        body = body.strip().replace('\n', ' ').replace('\r', ' ')
        return body[:max_length] + '...' if len(body) > max_length else body

    def _parse_date(self, date_str):
        try:
            date_tuple = email.utils.parsedate_tz(date_str)
            if date_tuple:
                timestamp = email.utils.mktime_tz(date_tuple)
                return datetime.fromtimestamp(timestamp)
        except:
            pass
        return None

    def move_to_trash(self, email_id):
        self.connection.store(email_id, '+FLAGS', '\\Deleted')
        return True

    def archive_email(self, email_id):
        self.connection.store(email_id, '+FLAGS', '\\Seen')
        self.connection.copy(email_id, '[Gmail]/All Mail')
        self.connection.store(email_id, '+FLAGS', '\\Deleted')
        self.connection.expunge()
        return True

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
