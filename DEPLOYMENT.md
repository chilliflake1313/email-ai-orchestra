# Deployment Guide

## Local Development

### Quick Start

```bash
python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

### Start Ollama

```bash
ollama serve
ollama pull mistral
```

### Run the application

```bash
python app.py
```

### Dry Run Mode

```bash
python app.py --dry-run
```

---

## Docker (optional)

Example `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p logs

EXPOSE 5000

CMD ["python", "app.py"]
```

Example `docker-compose.yml`:

```yaml
version: '3.8'

services:
  email-orchestra:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./logs:/app/logs
      - ./config.json:/app/config.json
    env_file:
      - .env
    restart: unless-stopped
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

---

## Environment Variables

Required:
- `EMAIL_ADDRESS` — Your email address
- `EMAIL_PASSWORD` — App-specific password
- `IMAP_SERVER` — IMAP server address
- `IMAP_PORT` — IMAP port (default: 993)
- `OLLAMA_BASE_URL` — Ollama API URL
- `OLLAMA_MODEL` — Model name (default: mistral)

## Email Provider Setup

### Gmail
- Enable 2-Factor Authentication
- Generate an App Password (Security → 2-Step Verification → App passwords)

### Outlook / Yahoo
- Use provider IMAP settings (see `config.json` examples)

---

## Security Considerations

- Never commit `.env` with credentials
- Use app-specific passwords
- Use IMAP over SSL/TLS only
- Review whitelist regularly
- Test rules in dry-run mode first

## Performance Tuning

- Adjust fetch `limit` in the reader
- Reduce `num_predict` in classifier payload for lower latency

## Monitoring

- Check logs:

```bash
tail -f logs/actions.log
```

- Monitor Ollama:

```bash
curl http://localhost:11434/api/tags
```

## Backup

- Backup configuration:

```bash
cp config.json config.json.backup
```

- Export logs:

```bash
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

## Troubleshooting

- IMAP auth failures: verify credentials and provider settings
- Ollama timeouts: increase request timeout in `agents/classifier.py`

---

## Systemd Service (example)

Create `email-orchestra.service` (see repository root) and copy to `/etc/systemd/system/`.

```bash
sudo cp email-orchestra.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable email-orchestra
sudo systemctl start email-orchestra
sudo systemctl status email-orchestra
sudo journalctl -u email-orchestra -f
```
