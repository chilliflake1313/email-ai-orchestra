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

- `delete`: Move to Trash folder
- `archive`: Remove from inbox
- `keep`: No action

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
