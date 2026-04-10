# PhishGuard Configuration & Deployment

## Local Development Setup (Already Configured)

### Current Setup
- ✅ Python 3.14.3 virtual environment configured
- ✅ All dependencies installed (Flask, Flask-Cors, requests, etc.)
- ✅ Development server running on http://localhost:5000
- ✅ Debug mode enabled for live reload

### Running the Application

**Windows:**
```bash
run.bat
```

**Mac/Linux:**
```bash
./run.sh
```

**Manual:**
```bash
.venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
python app.py
```

## Environment Variables

Create a `.env` file for configuration (optional):

```python
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=52428800  # 50MB
```

## Installed Packages

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| Flask-Cors | 4.0.0 | Cross-Origin support |
| Werkzeug | 3.0.0 | WSGI utilities |
| requests | 2.31.0 | HTTP library |
| python-dotenv | 1.0.0 | Environment variables |

## Production Deployment

### Using Gunicorn (Recommended)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress

```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Using Gevent

```bash
pip install gevent gevent-websocket
gunicorn --worker-class gevent --worker-connections 1000 -b 0.0.0.0:5000 app:app
```

## Nginx Configuration

```nginx
upstream phishguard {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name phishguard.example.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://phishguard;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/phishing-detection/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

## Apache Configuration

```apache
<VirtualHost *:80>
    ServerName phishguard.example.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    <Directory /path/to/phishing-detection/static>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 30 days"
    </Directory>
</VirtualHost>
```

## Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t phishguard .
docker run -p 5000:5000 phishguard
```

## Database Setup (For Future Enhancement)

To add persistent storage, create `db_config.py`:

```python
import os
from datetime import datetime

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///phishguard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Usage in app.py:
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)
```

## Security Considerations

### HTTPS in Production
```nginx
listen 443 ssl http2;
ssl_certificate /path/to/cert.pem;
ssl_certificate_key /path/to/key.pem;
ssl_protocols TLSv1.2 TLSv1.3;
```

### Security Headers

Add to Flask app:

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/check-url', methods=['POST'])
@limiter.limit("10 per minute")
def check_url():
    # ...
```

## Monitoring

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler(
        'logs/phishguard.log',
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('PhishGuard startup')
```

## Performance Optimization

### Enable Gzip Compression

```python
from flask_compress import Compress
Compress(app)
```

### Cache Static Files

```python
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year
```

### Database Indexing
```sql
CREATE INDEX idx_url_checks ON detections(url, timestamp);
CREATE INDEX idx_risk_level ON detections(risk_level);
```

## Testing

Run tests with pytest:

```bash
pip install pytest pytest-cov
pytest
pytest --cov=. --cov-report=html
```

## Backup Strategy

### Automatic Daily Backup

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/phishguard"
DATE=$(date +%Y%m%d_%H%M%S)
sqlite3 phishguard.db ".backup '/backups/phishguard_${DATE}.db'"
```

## Systemd Service (Linux)

Create `/etc/systemd/system/phishguard.service`:

```ini
[Unit]
Description=PhishGuard Phishing Detection Service
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/phishguard
ExecStart=/opt/phishguard/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:5000 \
    --timeout 60 \
    app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable phishguard
sudo systemctl start phishguard
```

## Troubleshooting

### Port Already in Use
```bash
# Find process on port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # Mac/Linux

# Kill process
taskkill /PID <PID> /F  # Windows
kill -9 <PID>  # Mac/Linux
```

### Virtual Environment Issues
```bash
# Recreate environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Memory Issues
Check memory usage:
```bash
# Linux
free -h
ps aux | grep python

# Windows
tasklist | findstr python
```

## Support & Maintenance

- **Error Logs**: Check `logs/phishguard.log`
- **Statistics**: View `detection_stats.json`
- **Updates**: Run `pip install --upgrade -r requirements.txt`

---

For more information, see README.md for complete documentation.
