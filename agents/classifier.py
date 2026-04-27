import requests
import json
import os


class ClassifierAgent:
    def __init__(self, ollama_url=None, model=None):
        self.ollama_url = ollama_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = model or os.getenv('OLLAMA_MODEL', 'mistral')

    def classify(self, email_data):
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        snippet = email_data.get('snippet', '')
        
        prompt = self._build_prompt(subject, sender, snippet)
        
        try:
            response = self._call_ollama(prompt)
            category = self._parse_response(response)
            return category
        except Exception:
            return 'unknown'

    def _build_prompt(self, subject, sender, snippet):
        return f"""Classify this email into exactly one category: ecommerce, banking, personal, or spam.

Sender: {sender}
Subject: {subject}
Content: {snippet}

Respond with ONLY ONE WORD from this list: ecommerce, banking, personal, spam

Category:"""

    def _call_ollama(self, prompt):
        url = f"{self.ollama_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 10
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', '')

    def _parse_response(self, response):
        response = response.strip().lower()
        
        valid_categories = ['ecommerce', 'banking', 'personal', 'spam']
        
        for category in valid_categories:
            if category in response:
                return category
        
        return 'unknown'

    def classify_batch(self, emails):
        results = []
        for email_data in emails:
            category = self.classify(email_data)
            results.append({
                'email': email_data,
                'category': category
            })
        return results
