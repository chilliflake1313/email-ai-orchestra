import json
from datetime import datetime


class RuleEngine:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.whitelist = self.config.get('whitelist', [])
        self.rules = self.config.get('rules', [])

    def is_whitelisted(self, email_data):
        sender = email_data.get('sender', '').lower()
        
        for whitelisted_sender in self.whitelist:
            if whitelisted_sender.lower() in sender:
                return True
        
        return False

    def evaluate(self, email_data, category=None):
        if self.is_whitelisted(email_data):
            return 'keep', 'Whitelisted sender'
        
        for rule in self.rules:
            if self._matches_rule(email_data, rule, category):
                action = rule.get('action', 'keep')
                rule_name = rule.get('name', 'Unnamed rule')
                return action, rule_name
        
        return 'keep', 'No matching rule'

    def _matches_rule(self, email_data, rule, category):
        condition = rule.get('condition', {})
        
        if 'sender_contains' in condition:
            sender = email_data.get('sender', '').lower()
            if condition['sender_contains'].lower() not in sender:
                return False
        
        if 'subject_contains' in condition:
            subject = email_data.get('subject', '').lower()
            if condition['subject_contains'].lower() not in subject:
                return False
        
        if 'category' in condition:
            if not category or category != condition['category']:
                return False
        
        if 'days_old' in condition:
            days_old = email_data.get('days_old', 0)
            if days_old < condition['days_old']:
                return False
        
        return True

    def get_action_summary(self):
        action_counts = {}
        for rule in self.rules:
            action = rule.get('action', 'keep')
            action_counts[action] = action_counts.get(action, 0) + 1
        return action_counts
