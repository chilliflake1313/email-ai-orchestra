import unittest
from core.rules import RuleEngine


class TestRuleEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = RuleEngine()
    
    def test_whitelist(self):
        email_data = {
            'sender': 'important@company.com',
            'subject': 'Test',
            'days_old': 0
        }
        
        action, rule = self.engine.evaluate(email_data)
        self.assertEqual(action, 'keep')
        self.assertEqual(rule, 'Whitelisted sender')
    
    def test_sender_match(self):
        email_data = {
            'sender': 'no-reply@flipkart.com',
            'subject': 'Order Update',
            'days_old': 0
        }
        
        action, rule = self.engine.evaluate(email_data, 'ecommerce')
        self.assertEqual(action, 'delete')
    
    def test_category_match(self):
        email_data = {
            'sender': 'unknown@example.com',
            'subject': 'Test',
            'days_old': 0
        }
        
        action, rule = self.engine.evaluate(email_data, 'spam')
        self.assertEqual(action, 'delete')
    
    def test_days_old_condition(self):
        email_data = {
            'sender': 'statement@bank.com',
            'subject': 'Monthly Statement',
            'days_old': 45
        }
        
        action, rule = self.engine.evaluate(email_data, 'banking')
        self.assertEqual(action, 'archive')
    
    def test_no_match_default(self):
        email_data = {
            'sender': 'friend@example.com',
            'subject': 'Hello',
            'days_old': 0
        }
        
        action, rule = self.engine.evaluate(email_data, 'personal')
        self.assertEqual(action, 'keep')


if __name__ == '__main__':
    unittest.main()
