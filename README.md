# Email AI Orchestra

A fully local email automation system using IMAP, Ollama LLM, and rule-based classification.

## Features

- Local LLM classification using Ollama
- IMAP email fetching
- Rule-based action engine
- Agent-based orchestration
- Web UI for monitoring and control
- Dry-run mode for safety
- No permanent deletions

## Prerequisites

- Python 3.9+
- Ollama installed and running
- Email account with IMAP access

## Setup

### 1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
ollama serve
```

### 2. Clone and Install

```bash
git clone <repo-url>
cd email-ai-orchestra
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```
Edit `.env` with your email credentials.

For Gmail, enable 2FA and generate an app password.

### 4. Configure Rules

Edit `config.json` to customize classification rules and actions.

## Usage

### Start the Application

```bash
python app.py
```

Access the web UI at http://localhost:5000

### Dry Run Mode

```bash
python app.py --dry-run
```

Preview actions without executing them.

## Architecture

```
email-ai-orchestra/
├── app.py                 # Flask application entry point
├── agents/                # Agent layer
│   ├── reader.py          # Email reading agent
│   ├── classifier.py      # Classification agent
│   └── executor.py        # Action execution agent
├── core/                  # Core functionality
│   ├── imap_client.py     # IMAP connection handler
│   └── rules.py          # Rule engine
├── templates/             # Web UI templates
│   └── index.html
├── logs/                  # Action logs
├── config.json           # Rules and settings
└── .env                  # Credentials (not in git)
```

## Configuration

### Rule Format

Rules are evaluated in order. First match wins.

```json
{
  "rules": [
    {
      "condition": {
        "sender_contains": "flipkart"
      },
      "action": "delete"
    }
  ]
}
```

### Supported Conditions

- `sender_contains`: substring in sender email
- `subject_contains`: substring in subject
- `category`: AI classification result
- `days_old`: age threshold

### Supported Actions


## Advanced Rules

See `config.advanced.json` for complex rule examples.

## 🏗️ Architecture

```
┌─────────────┐
│   Web UI    │
│  (Flask)    │
└──────┬──────┘
  │
┌──────▼──────────────────────┐
│    Application Layer         │
│  - Routes                    │
│  - Request Handling          │
└──────┬──────────────────────┘
  │
┌──────▼──────────────────────┐
│    Agent Layer               │
│  ┌────────────────────┐     │
│  │  Reader Agent      │     │
│  │  (IMAP Fetching)   │     │
│  └────────────────────┘     │
│  ┌────────────────────┐     │
│  │  Classifier Agent  │     │
│  │  (LLM via Ollama)  │     │
│  └────────────────────┘     │
│  ┌────────────────────┐     │
│  │  Executor Agent    │     │
│  │  (Rule + Actions)  │     │
│  └────────────────────┘     │
└──────┬──────────────────────┘
  │
┌──────▼──────────────────────┐
│    Core Layer                │
│  - IMAP Client               │
│  - Rule Engine               │
│  - Logger                    │
└──────────────────────────────┘
```

## 🧪 Testing

```bash
make test

python tests/run_tests.py

python -m unittest tests/test_rules.py
```

## 📊 Monitoring

### View Logs

```bash
tail -f logs/actions.log
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Statistics

```bash
python cli.py --stats
```

## 🔒 Security

- Credentials stored in `.env` (never committed)
- App-specific passwords recommended
- SSL/TLS for IMAP connections
- No permanent deletions
- Whitelist protection
- Dry-run testing mode

## 🚀 Production Deployment

### Using Docker

```bash
docker-compose up -d
```

### Using Systemd

```bash
sudo cp email-orchestra.service /etc/systemd/system/
sudo systemctl enable email-orchestra
sudo systemctl start email-orchestra
```

See `DEPLOYMENT.md` for details.

## 🛠️ Development

### Project Structure

```
email-ai-orchestra/
├── app.py                    # Flask application
├── cli.py                    # CLI interface
├── agents/                   # Agent layer
│   ├── reader.py             # Email fetching
│   ├── classifier.py         # AI classification
│   └── executor.py           # Action execution
├── core/                     # Core functionality
│   ├── imap_client.py        # IMAP operations
│   ├── rules.py              # Rule engine
│   └── logger.py             # Logging setup
├── templates/                # Web UI
│   └── index.html
├── tests/                    # Test suite
├── scripts/                  # Utility scripts
├── logs/                     # Log files
├── config.json               # Rules configuration
├── .env                      # Credentials (gitignored)
└── requirements.txt          # Dependencies
```

### Adding New Rules

Edit `config.json`

Validate: `make validate`

Test: `make run-dry`

Deploy: `make run`

### Extending Classification

Modify `agents/classifier.py`:

```python
def _build_prompt(self, subject, sender, snippet):
    return f"""Your custom prompt here"""
```

## 📝 Makefile Commands

```bash
make help         # Show all commands
make install      # Install dependencies
make check        # Check environment
make validate     # Validate config
make test         # Run tests
make run          # Start application
make run-dry      # Start in dry-run mode
make cli          # Run CLI
make clean        # Clean temp files
```

## 🐛 Troubleshooting

### Ollama Connection Failed

```bash
ollama serve
ollama list
ollama pull mistral
```

### IMAP Authentication Error

- Check `.env` credentials
- Verify app password (for Gmail)
- Enable IMAP in email settings
- Check firewall/network

### Classification Errors

```bash
curl http://localhost:11434/api/tags
ollama run mistral "test"
```

### Memory Issues

Use a lighter model:

```bash
ollama pull mistral:7b-instruct-q4_0
```

Update `.env`:

```env
OLLAMA_MODEL=mistral:7b-instruct-q4_0
```

## 📄 License

MIT License - See `LICENSE` file.

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests
4. Submit a pull request

## 📞 Support

- Issues: GitHub Issues
- Docs: `README.md`, `DEPLOYMENT.md`
- Logs: `logs/actions.log`

## 🎯 Roadmap

- Multi-account support
- Custom LLM model fine-tuning
- Email templates for responses
- Scheduled automation (cron)
- Web UI improvements
- Export/import rules
- Email analytics dashboard
- Mobile-responsive UI

Made with love for privacy-conscious email automation.

## Safety Features

- No permanent deletion (only moves to Trash)
- Whitelist support for protected senders
- Dry-run mode for testing
- Detailed action logging

## Web UI

### Dashboard

- View recent emails
- See sender, subject, date
- Manual refresh
- Process Emails
- Click "Run Cleanup" button
- View classification results
- See proposed actions
- Execute or preview

## Logs

All actions are logged to `logs/actions.log`:

```text
2024-01-15 10:30:45 - INFO - Classified email from sender@example.com as spam
2024-01-15 10:30:46 - INFO - Action: delete (rule matched: spam)
```

## Troubleshooting

### Ollama Connection Error

Ensure Ollama is running:

```bash
ollama serve
```

### IMAP Authentication Failed

- Check credentials in `.env`
- For Gmail: enable 2FA and use app password
- For other providers: check IMAP settings

### Classification Issues

Pull the model again:

```bash
ollama pull mistral
```

## License

MIT
