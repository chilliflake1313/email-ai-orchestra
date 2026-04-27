from flask import Flask, render_template, jsonify, request
from agents.reader import ReaderAgent
from agents.classifier import ClassifierAgent
from agents.executor import ExecutorAgent
from core.logger import setup_logger
from dotenv import load_dotenv
import os
import sys


load_dotenv()

app = Flask(__name__)

logger = setup_logger()

dry_run = '--dry-run' in sys.argv


@app.route('/')
def index():
    return render_template('index.html', dry_run=dry_run)


@app.route('/api/emails')
def get_emails():
    try:
        limit = request.args.get('limit', 50, type=int)
        
        reader = ReaderAgent()
        emails = reader.fetch_emails(limit)
        
        return jsonify({
            'success': True,
            'count': len(emails),
            'emails': emails
        })
    
    except Exception as e:
        logger.error(f"Failed to fetch emails: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/process', methods=['POST'])
def process_emails():
    try:
        data = request.json
        limit = data.get('limit', 50)
        
        logger.info("Starting email processing pipeline")
        
        reader = ReaderAgent()
        emails = reader.fetch_emails(limit)
        logger.info(f"Fetched {len(emails)} emails")
        
        classifier = ClassifierAgent()
        classified = classifier.classify_batch(emails)
        logger.info(f"Classified {len(classified)} emails")
        
        executor = ExecutorAgent(dry_run=dry_run)
        results = executor.execute_actions(classified)
        summary = executor.get_summary(results)
        
        logger.info(f"Processing complete: {summary}")
        
        return jsonify({
            'success': True,
            'results': results,
            'summary': summary,
            'dry_run': dry_run
        })
    
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/status')
def get_status():
    try:
        reader = ReaderAgent()
        count = reader.get_email_count()
        
        return jsonify({
            'success': True,
            'inbox_count': count,
            'dry_run': dry_run,
            'ollama_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            'model': os.getenv('OLLAMA_MODEL', 'mistral')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    logger.info(f"Starting Email AI Orchestra (dry_run={dry_run})")
    app.run(debug=True, host='0.0.0.0', port=5000)
