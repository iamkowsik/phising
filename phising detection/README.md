# PhishGuard - Advanced Phishing Detection Tool

A professional web-based application for detecting phishing URLs, analyzing suspicious emails, and scanning text for phishing indicators. Built with Flask backend and modern HTML/CSS/JavaScript frontend.

## Features

- **URL Phishing Detection**: Analyze URLs for suspicious patterns, domain typosquatting, and known phishing domains
- **Email Content Analysis**: Scan email content for phishing keywords, urgency language, and suspicious requests
- **Text Content Scanner**: Check any text for phishing indicators and suspicious patterns
- **Risk Scoring**: Get detailed risk assessment with scores from 0-100%
- **Real-time Statistics**: Track detection history and viewing usage statistics
- **Professional UI**: Modern, responsive design that works on desktop and mobile devices
- **Detailed Indicators**: See exactly what made content suspicious with comprehensive analysis

## Tech Stack

### Backend
- **Flask**: Python web framework
- **Flask-Cors**: Cross-Origin Resource Sharing support
- **Python 3.8+**: Programming language

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icon library

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   cd "d:\phising detection"
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`
   - The application will be fully functional and ready to use

## Usage

### Checking URLs
1. Navigate to the URL Phishing Detector section
2. Enter a URL (must start with http:// or https://)
3. Click "Check URL" button
4. Review the risk assessment and detected indicators

### Analyzing Emails
1. Go to Email Content Analyzer section
2. Paste your email content
3. Click "Analyze Email" button
4. Review the analysis and detected phishing indicators

### Scanning Text
1. Navigate to Text Content Scanner section
2. Paste your text to analyze
3. Click "Scan Text" button
4. View the results and risk assessment

### Viewing Statistics
- Statistics are automatically loaded on page load
- Click "Refresh Stats" button to update statistics
- Statistics include:
  - Total URLs checked
  - Total emails analyzed
  - Total text scanned
  - Overall checks performed

## Phishing Detection Indicators

The tool checks for:
- **URL-based threats**:
  - IP addresses instead of domain names
  - Suspicious keywords in URL
  - Known phishing domains
  - Domain typosquatting
  - Lack of HTTPS encryption
  - Suspicious URL paths

- **Email threats**:
  - Suspicious keywords
  - Urgency language
  - Requests to click links
  - Requests for sensitive information
  - Poor grammar or spelling
  - Embedded URLs

- **Text threats**:
  - Phishing keywords
  - Urgency language
  - URLs and email addresses
  - Suspicious patterns

## Risk Levels

| Risk Level | Score Range | Description |
|-----------|------------|-------------|
| Low | 0-29% | Minimal phishing indicators |
| Medium | 30-49% | Some suspicious elements |
| High | 50-69% | Multiple phishing indicators |
| Critical | 70-100% | Strong phishing indicators |

## Project Structure

```
phising detection/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── detection_stats.json        # Statistics data (created at runtime)
├── templates/
│   ├── index.html             # Main dashboard
│   ├── about.html             # About page with tips
│   └── 404.html               # Error page
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # Frontend JavaScript
└── utils/
    └── phishing_detector.py   # Phishing detection logic
```

## API Endpoints

### POST /api/check-url
Check a URL for phishing indicators
- **Request**: `{ "url": "https://example.com" }`
- **Response**: Risk assessment with indicators

### POST /api/check-email
Analyze email content
- **Request**: `{ "content": "Email content here..." }`
- **Response**: Risk assessment with detected issues

### POST /api/check-text
Scan text content
- **Request**: `{ "text": "Text to analyze..." }`
- **Response**: Risk assessment with indicators

### GET /api/statistics
Get detection statistics
- **Response**: Usage statistics and detection history

## Important Notes

### Disclaimer
PhishGuard is an **educational tool** designed to raise awareness about phishing attacks. While we strive for accuracy:
- No tool can guarantee 100% detection of all phishing attempts
- Always verify suspicious messages through official channels
- This should be used as part of a comprehensive security strategy

### Best Practices
1. **Never click links in suspicious emails** - Navigate to official websites independently
2. **Always verify through official channels** - Contact companies directly if unsure
3. **Look for HTTPS** - Verify SSL certificates on sensitive sites
4. **Check sender addresses carefully** - Phishers often use similar-looking addresses
5. **Be suspicious of urgency** - Legitimate companies rarely demand immediate action

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed: `python --version`
- Check all dependencies are installed: `pip install -r requirements.txt`
- Ensure port 5000 is available

### Module not found errors
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### CORS errors
- Flask-Cors is included in requirements.txt
- Ensure it's installed: `pip install Flask-Cors`

## Performance Tips

- The application stores statistics in `detection_stats.json`
- Statistics are updated automatically with each check
- Clear `detection_stats.json` to reset statistics

## Security Considerations

- Always use HTTPS in production
- Validate and sanitize all user inputs
- Never store sensitive information about detected phishing
- Consider implementing rate limiting for API endpoints
- Use environment variables for sensitive configuration

## Future Enhancements

Potential features for future versions:
- Machine learning-based phishing detection
- Email header analysis
- Attachment risk scanning
- Browser extension integration
- API rate limiting
- User accounts and detection history
- Advanced reporting features

## Support & Feedback

For issues, suggestions, or to report false positives, please consider:
- Reviewing the about page for common phishing tactics
- Checking the documentation and tips provided
- Verifying with official sources

## License

This project is provided as an educational tool for cybersecurity awareness.

## Disclaimer

This tool is for educational purposes only. It should not be relied upon as the sole means of phishing detection. Always exercise caution online and follow best security practices.

---

**Stay safe and vigilant against phishing attacks!** 🛡️
