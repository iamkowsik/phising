# Quick Start Guide for PhishGuard

## What is PhishGuard?
PhishGuard is a professional phishing detection web application with:
- **URL Phishing Detector** - Check URLs for suspicious patterns and known threats
- **Email Content Analyzer** - Scan email content for phishing indicators  
- **Text Content Scanner** - Analyze any text for phishing red flags
- **Real-time Statistics** - Track detection history
- **Professional UI** - Beautiful, responsive design

## How to Start

### Option 1: Windows (Easiest)
1. Open Command Prompt in this folder
2. Double-click `run.bat` 
3. The app will open at http://localhost:5000

### Option 2: Mac/Linux
1. Open Terminal in this folder
2. Run: `chmod +x run.sh && ./run.sh`
3. The app will open at http://localhost:5000

### Option 3: Manual Start
1. Open Command Prompt/Terminal in this folder
2. Activate virtual environment:
   - **Windows**: `.venv\Scripts\activate`
   - **Mac/Linux**: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`
5. Open browser and go to: http://localhost:5000

## Features

### URL Detection
- Detects suspicious patterns in URLs
- Identifies domain typosquatting
- Checks for known phishing domains
- Warns about missing HTTPS
- Finds suspicious keywords

### Email Analysis
- Scans for phishing keywords
- Detects urgency language
- Identifies requests for sensitive info
- Finds suspicious URLs in emails
- Checks for poor grammar

### Text Scanning
- Identifies phishing keywords
- Detects urgency indicators
- Finds URLs and email addresses
- Scores overall threat level

### Risk Scoring
- **Low (0-29%)**: Minimal indicators
- **Medium (30-49%)**: Some suspicious elements
- **High (50-69%)**: Multiple indicators
- **Critical (70-100%)**: Strong phishing signs

## Important Tips

⚠️ **Always Remember:**
- PhishGuard is an educational tool
- No tool is 100% accurate
- Always verify through official channels
- Never click suspicious links
- Check SSL certificates (HTTPS)
- Legitimate companies don't ask for passwords via email

## Project Structure
```
phising detection/
├── app.py                    # Main Flask app
├── requirements.txt          # Python packages
├── run.bat                   # Windows launcher
├── run.sh                    # Mac/Linux launcher
├── README.md                 # Full documentation
├── templates/
│   ├── index.html           # Main dashboard
│   ├── about.html           # Tips & information
│   └── 404.html             # Error page
├── static/
│   ├── css/style.css        # Styling
│   └── js/main.js           # JavaScript
└── utils/
    └── phishing_detector.py # Detection logic
```

## Troubleshooting

### App won't start?
- Make sure Python 3.8+ is installed
- Check port 5000 is available
- Run: `python --version`

### "Permission denied" on Mac/Linux?
- Run: `chmod +x run.sh`
- Then: `./run.sh`

### Need help?
- Check README.md for detailed docs
- Review the About page in the app
- Visit the features section

## API Usage

All detection functions are available via API:

```bash
# Check URL
curl -X POST http://localhost:5000/api/check-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Check Email
curl -X POST http://localhost:5000/api/check-email \
  -H "Content-Type: application/json" \
  -d '{"content": "Your email content here..."}'

# Check Text
curl -X POST http://localhost:5000/api/check-text \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here..."}'

# Get Statistics
curl http://localhost:5000/api/statistics
```

## Next Steps

1. ✅ App is running on http://localhost:5000
2. 📝 Test with some URLs or emails
3. 📊 Check the statistics
4. 📚 Read the About page for phishing tips
5. 🔒 Use it to stay safe online!

---

**Be safe. Stay vigilant. Protect yourself.** 🛡️
