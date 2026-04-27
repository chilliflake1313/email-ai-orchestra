from core.imap_client import IMAPClient
from core.rules import RuleEngine
import os
import logging


class ExecutorAgent:
    def __init__(self, email_address=None, password=None, server=None, port=993, dry_run=False):
        self.email_address = email_address or os.getenv('EMAIL_ADDRESS')
        self.password = password or os.getenv('EMAIL_PASSWORD')
        self.server = server or os.getenv('IMAP_SERVER', 'imap.gmail.com')
        self.port = int(os.getenv('IMAP_PORT', port))
        self.dry_run = dry_run
        self.rule_engine = RuleEngine()
        
        self.logger = logging.getLogger('executor')

    def execute_actions(self, classified_emails):
        results = []
        
        for item in classified_emails:
            email_data = item['email']
            category = item['category']
            
            action, rule_name = self.rule_engine.evaluate(email_data, category)
            
            result = {
                'email_id': email_data['id'],
                'subject': email_data['subject'],
                'sender': email_data['sender'],
                'category': category,
                'action': action,
                'rule': rule_name,
                'executed': False
            }
            
            if self.dry_run:
                result['executed'] = False
                result['dry_run'] = True
            else:
                executed = self._perform_action(email_data['id'], action)
                result['executed'] = executed
            
            self.logger.info(f"Email: {email_data['subject'][:50]} | Category: {category} | Action: {action} | Rule: {rule_name}")
            
            results.append(result)
        
        return results

    def _perform_action(self, email_id, action):
        if action == 'keep':
            return True
        
        try:
            with IMAPClient(self.email_address, self.password, self.server, self.port) as client:
                if action == 'delete':
                    client.move_to_trash(email_id.encode())
                elif action == 'archive':
                    client.archive_email(email_id.encode())
                return True
        except Exception as e:
            self.logger.error(f"Failed to execute action {action} on email {email_id}: {str(e)}")
            return False

    def get_summary(self, results):
        summary = {
            'total': len(results),
            'delete': 0,
            'archive': 0,
            'keep': 0,
            'executed': 0
        }
        
        for result in results:
            action = result['action']
            summary[action] = summary.get(action, 0) + 1
            if result['executed']:
                summary['executed'] += 1
        
        return summary
