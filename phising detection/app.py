from flask import Flask, render_template, request, jsonify
from utils.phishing_detector import PhishingDetector
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file upload

# Initialize phishing detector
detector = PhishingDetector()

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

@app.route('/api/check-url', methods=['POST', 'GET'])
def check_url():
    """API endpoint to check if a URL is phishing.

    Accepts JSON POST (application/json), form POST (application/x-www-form-urlencoded),
    or GET query parameter `url`. Returns JSON with detector output.
    """
    try:
        url = ''

        # GET request: read from query string
        if request.method == 'GET':
            url = (request.args.get('url') or '').strip()
        else:
            # POST: prefer JSON body when present
            if request.is_json:
                data = request.get_json(silent=True) or {}
                url = (data.get('url') or '').strip()
            else:
                # form-encoded or other POST
                url = (request.form.get('url') or '').strip()

                # fallback to values (covers both form and query)
                if not url:
                    url = (request.values.get('url') or '').strip()

        if not url:
            return jsonify({'success': False, 'error': 'Please provide a URL'}), 400

        result = detector.check_url(url)
        return jsonify({'success': True, 'data': result}), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/check-email', methods=['POST'])
def check_email():
    """API endpoint to analyze email content"""
    try:
        data = request.json
        email_content = data.get('content', '').strip()
        
        if not email_content:
            return jsonify({
                'success': False,
                'error': 'Please provide email content'
            }), 400
        
        # Check email
        result = detector.check_email(email_content)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/check-text', methods=['POST'])
def check_text():
    """API endpoint to analyze plain text"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Please provide text to analyze'
            }), 400
        
        # Check text
        result = detector.check_text(text)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def statistics():
    """Get detection statistics"""
    try:
        stats = detector.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission from the simple frontend and render result page"""
    try:
        url = request.form.get('url', '').strip()
        if not url:
            return render_template('result.html', url=url, result='Error', meaning='No URL provided', confidence=0)

        res = detector.check_url(url)
        score = int(res.get('score', 0))
        risk = res.get('risk_level', 'low')

        if risk in ('critical', 'high'):
            result_text = 'Phishing URL'
            meaning = 'High risk — likely phishing. Do not interact with this site.'
        elif risk == 'medium':
            result_text = 'Suspicious URL'
            meaning = 'Potentially suspicious — exercise caution.'
        else:
            result_text = 'Legitimate URL'
            meaning = 'Low risk — appears safe.'

        return render_template('result.html', url=url, result=result_text, meaning=meaning, confidence=score)
    except Exception as e:
        return render_template('result.html', url='', result='Error', meaning=str(e), confidence=0)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


# Serve template paths used by static links (avoid frontend changes)
@app.route('/about.html')
def about_html():
    """Serve about.html when requested directly"""
    return render_template('about.html')


@app.route('/index.html')
def index_html():
    """Serve index.html when requested directly"""
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
