import re
import requests
from urllib.parse import urlparse
from datetime import datetime
import json
import os

class PhishingDetector:
    """Main class for detecting phishing URLs, emails, and text"""
    
    def __init__(self):
        self.suspicious_keywords = [
            'verify', 'confirm', 'update', 'validate', 'authenticate',
            'urgent', 'immediately', 'act now', 'click here', 'alert',
            'problem', 'issue', 'security', 'unusual activity', 'suspended',
            'limited', 'restricted', 'action required', 'confirm identity'
        ]
        
        self.phishing_domains = [
            'paypal-update.com', 'amazon-verify.net', 'apple-id-verify.com',
            'google-account-verify.com', 'microsoft-support-services.com'
        ]
        
        self.stats_file = 'detection_stats.json'
        self.load_stats()
    
    def check_url(self, url):
        """Check if a URL is potentially phishing"""
        result = {
            'url': url,
            'risk_level': 'low',
            'score': 0,
            'indicators': [],
            'timestamp': datetime.now().isoformat()
        }
        
        risk_score = 0
        
        # Check URL format
        if not self._is_valid_url(url):
            result['indicators'].append('Invalid URL format')
            risk_score += 20
        
        # Parse URL
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check for suspicious keywords in URL
            if self._contains_suspicious_keywords(url):
                result['indicators'].append('Suspicious keywords detected in URL')
                risk_score += 25
            
            # Check for IP address usage
            if self._is_ip_address(domain):
                result['indicators'].append('Using IP address instead of domain')
                risk_score += 30
            
            # Check for known phishing domains
            if self._is_known_phishing_domain(domain):
                result['indicators'].append('Known phishing domain detected')
                risk_score += 50
            
            # Check for domain typosquatting
            if self._check_typosquatting(domain):
                result['indicators'].append('Possible domain typosquatting detected')
                risk_score += 25
            
            # Check SSL certificate (simulate)
            if not url.startswith('https'):
                result['indicators'].append('No HTTPS encryption')
                risk_score += 20
            
            # Check for suspicious path
            if self._contains_suspicious_path(parsed.path):
                result['indicators'].append('Suspicious URL path detected')
                risk_score += 15
                
        except Exception as e:
            result['indicators'].append(f'Error parsing URL: {str(e)}')
            risk_score += 10
        
        # Set risk level
        result['score'] = min(risk_score, 100)
        if result['score'] >= 70:
            result['risk_level'] = 'critical'
        elif result['score'] >= 50:
            result['risk_level'] = 'high'
        elif result['score'] >= 30:
            result['risk_level'] = 'medium'
        else:
            result['risk_level'] = 'low'
        
        self.update_stats('urls_checked')
        return result
    
    def check_email(self, content):
        """Check email content for phishing indicators"""
        result = {
            'risk_level': 'low',
            'score': 0,
            'indicators': [],
            'timestamp': datetime.now().isoformat()
        }
        
        risk_score = 0
        content_lower = content.lower()
        
        # Check for suspicious keywords
        keyword_count = sum(content_lower.count(keyword) for keyword in self.suspicious_keywords)
        if keyword_count > 0:
            result['indicators'].append(f'Found {keyword_count} suspicious keywords')
            risk_score += min(keyword_count * 10, 30)
        
        # Check for urgency indicators
        if re.search(r'\b(urgent|immediately|act now|asap)\b', content_lower):
            result['indicators'].append('Urgency language detected')
            risk_score += 20
        
        # Check for requests to click links
        if re.search(r'click.*link|click.*here|verify.*link', content_lower):
            result['indicators'].append('Suspicious link request detected')
            risk_score += 25
        
        # Check for requests to provide information
        if re.search(r'(confirm|verify|update).*password|(confirm|verify|update).*card|(confirm|verify|update).*account', content_lower):
            result['indicators'].append('Request to provide sensitive information detected')
            risk_score += 30
        
        # Check for URLs in email
        urls = re.findall(r'https?://[^\s]+', content)
        if urls:
            result['indicators'].append(f'Found {len(urls)} URL(s) in email')
            risk_score += 15
        
        # Check for poor grammar or spelling
        if self._has_poor_grammar(content):
            result['indicators'].append('Poor grammar or spelling detected')
            risk_score += 10
        
        # Set risk level
        result['score'] = min(risk_score, 100)
        if result['score'] >= 70:
            result['risk_level'] = 'critical'
        elif result['score'] >= 50:
            result['risk_level'] = 'high'
        elif result['score'] >= 30:
            result['risk_level'] = 'medium'
        else:
            result['risk_level'] = 'low'
        
        self.update_stats('emails_checked')
        return result
    
    def check_text(self, text):
        """Check plain text for phishing indicators"""
        result = {
            'risk_level': 'low',
            'score': 0,
            'indicators': [],
            'timestamp': datetime.now().isoformat()
        }
        
        risk_score = 0
        text_lower = text.lower()
        
        # Check for suspicious keywords
        keyword_count = sum(text_lower.count(keyword) for keyword in self.suspicious_keywords)
        if keyword_count > 0:
            result['indicators'].append(f'Found {keyword_count} suspicious keywords')
            risk_score += min(keyword_count * 8, 25)
        
        # Check for URLs
        urls = re.findall(r'https?://[^\s]+', text)
        if urls:
            result['indicators'].append(f'Found {len(urls)} URL(s)')
            risk_score += 15
        
        # Check for email addresses
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        if emails:
            result['indicators'].append(f'Found {len(emails)} email address(es)')
            risk_score += 10
        
        # Check for urgency language
        if re.search(r'\b(urgent|immediately|act now|asap)\b', text_lower):
            result['indicators'].append('Urgency language detected')
            risk_score += 15
        
        # Set risk level
        result['score'] = min(risk_score, 100)
        if result['score'] >= 70:
            result['risk_level'] = 'critical'
        elif result['score'] >= 50:
            result['risk_level'] = 'high'
        elif result['score'] >= 30:
            result['risk_level'] = 'medium'
        else:
            result['risk_level'] = 'low'
        
        self.update_stats('texts_checked')
        return result
    
    # Helper methods
    def _is_valid_url(self, url):
        """Check if URL format is valid"""
        url_pattern = r'^https?://[^\s]+'
        return re.match(url_pattern, url) is not None
    
    def _contains_suspicious_keywords(self, text):
        """Check if text contains suspicious keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.suspicious_keywords)
    
    def _is_ip_address(self, domain):
        """Check if domain is an IP address"""
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        return re.match(ip_pattern, domain) is not None
    
    def _is_known_phishing_domain(self, domain):
        """Check if domain is in known phishing list"""
        return domain in self.phishing_domains
    
    def _check_typosquatting(self, domain):
        """Check for common typosquatting patterns"""
        common_domains = ['paypal.com', 'amazon.com', 'apple.com', 'google.com', 'microsoft.com']
        domain_parts = domain.split('.')
        
        for common in common_domains:
            if common.replace('.', '') in domain.replace('.', '') and common not in domain:
                return True
        
        return False
    
    def _contains_suspicious_path(self, path):
        """Check if URL path contains suspicious patterns"""
        suspicious_patterns = [
            r'login|signin|account|verify|update|confirm',
            r'secure|bank|payment|billing'
        ]
        
        return any(re.search(pattern, path.lower()) for pattern in suspicious_patterns)
    
    def _has_poor_grammar(self, text):
        """Simple check for poor grammar"""
        # This is a simplified check
        return len(text) < 50 or text.count('  ') > 2
    
    def get_statistics(self):
        """Get detection statistics"""
        return self.stats
    
    def load_stats(self):
        """Load statistics from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except:
                self.stats = self._get_default_stats()
        else:
            self.stats = self._get_default_stats()
    
    def _get_default_stats(self):
        """Get default statistics"""
        return {
            'urls_checked': 0,
            'emails_checked': 0,
            'texts_checked': 0,
            'total_checks': 0,
            'threats_detected': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    def update_stats(self, check_type):
        """Update statistics"""
        if check_type in self.stats:
            self.stats[check_type] += 1
        self.stats['total_checks'] = sum(self.stats.get(k, 0) for k in ['urls_checked', 'emails_checked', 'texts_checked'])
        self.stats['last_updated'] = datetime.now().isoformat()
        
        # Save stats
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
