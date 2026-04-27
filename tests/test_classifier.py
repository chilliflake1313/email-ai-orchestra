import unittest
from unittest.mock import patch, Mock
from agents.classifier import ClassifierAgent


class TestClassifierAgent(unittest.TestCase):
    
    def setUp(self):
        self.classifier = ClassifierAgent()
    
    def test_build_prompt(self):
        prompt = self.classifier._build_prompt(
            'Order Confirmed',
            'no-reply@amazon.com',
            'Your order has been confirmed'
        )
        
        self.assertIn('Order Confirmed', prompt)
        self.assertIn('amazon', prompt)
        self.assertIn('ecommerce', prompt)
    
    def test_parse_response_valid(self):
        response = "Based on the content, this is: ecommerce"
        category = self.classifier._parse_response(response)
        self.assertEqual(category, 'ecommerce')
    
    def test_parse_response_direct(self):
        response = "spam"
        category = self.classifier._parse_response(response)
        self.assertEqual(category, 'spam')
    
    def test_parse_response_invalid(self):
        response = "This is something else"
        category = self.classifier._parse_response(response)
        self.assertEqual(category, 'unknown')
    
    @patch('agents.classifier.requests.post')
    def test_classify_success(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {'response': 'ecommerce'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        email_data = {
            'subject': 'Order Update',
            'sender': 'shop@example.com',
            'snippet': 'Your order is on the way'
        }
        
        category = self.classifier.classify(email_data)
        self.assertEqual(category, 'ecommerce')
    
    @patch('agents.classifier.requests.post')
    def test_classify_error(self, mock_post):
        mock_post.side_effect = Exception('Connection error')
        
        email_data = {
            'subject': 'Test',
            'sender': 'test@example.com',
            'snippet': 'Test content'
        }
        
        category = self.classifier.classify(email_data)
        self.assertEqual(category, 'unknown')


if __name__ == '__main__':
    unittest.main()
