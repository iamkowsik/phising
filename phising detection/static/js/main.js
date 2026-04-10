// Main JavaScript for PhishGuard

// Check URL for phishing
function checkURL() {
    const url = document.getElementById('urlInput').value.trim();
    const resultDiv = document.getElementById('urlResult');
    
    if (!url) {
        showError(resultDiv, 'Please enter a URL');
        return;
    }
    
    resultDiv.style.display = 'none';
    const originalText = document.querySelector('button[onclick="checkURL()"]').innerHTML;
    document.querySelector('button[onclick="checkURL()"]').innerHTML = '<i class="fas fa-spinner"></i> Checking...';
    document.querySelector('button[onclick="checkURL()"]').disabled = true;
    
    fetch('/api/check-url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('button[onclick="checkURL()"]').innerHTML = originalText;
        document.querySelector('button[onclick="checkURL()"]').disabled = false;
        
        if (data.success) {
            displayURLResult(resultDiv, data.data);
            document.getElementById('urlInput').value = '';
        } else {
            showError(resultDiv, data.error);
        }
    })
    .catch(error => {
        document.querySelector('button[onclick="checkURL()"]').innerHTML = originalText;
        document.querySelector('button[onclick="checkURL()"]').disabled = false;
        showError(resultDiv, 'Error: ' + error.message);
    });
}

// Check Email for phishing
function checkEmail() {
    const content = document.getElementById('emailInput').value.trim();
    const resultDiv = document.getElementById('emailResult');
    
    if (!content) {
        showError(resultDiv, 'Please enter email content');
        return;
    }
    
    resultDiv.style.display = 'none';
    const originalText = document.querySelector('button[onclick="checkEmail()"]').innerHTML;
    document.querySelector('button[onclick="checkEmail()"]').innerHTML = '<i class="fas fa-spinner"></i> Analyzing...';
    document.querySelector('button[onclick="checkEmail()"]').disabled = true;
    
    fetch('/api/check-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: content })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('button[onclick="checkEmail()"]').innerHTML = originalText;
        document.querySelector('button[onclick="checkEmail()"]').disabled = false;
        
        if (data.success) {
            displayResult(resultDiv, data.data);
            document.getElementById('emailInput').value = '';
        } else {
            showError(resultDiv, data.error);
        }
    })
    .catch(error => {
        document.querySelector('button[onclick="checkEmail()"]').innerHTML = originalText;
        document.querySelector('button[onclick="checkEmail()"]').disabled = false;
        showError(resultDiv, 'Error: ' + error.message);
    });
}

// Check Text for phishing
function checkText() {
    const text = document.getElementById('textInput').value.trim();
    const resultDiv = document.getElementById('textResult');
    
    if (!text) {
        showError(resultDiv, 'Please enter text to scan');
        return;
    }
    
    resultDiv.style.display = 'none';
    const originalText = document.querySelector('button[onclick="checkText()"]').innerHTML;
    document.querySelector('button[onclick="checkText()"]').innerHTML = '<i class="fas fa-spinner"></i> Scanning...';
    document.querySelector('button[onclick="checkText()"]').disabled = true;
    
    fetch('/api/check-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector('button[onclick="checkText()"]').innerHTML = originalText;
        document.querySelector('button[onclick="checkText()"]').disabled = false;
        
        if (data.success) {
            displayResult(resultDiv, data.data);
            document.getElementById('textInput').value = '';
        } else {
            showError(resultDiv, data.error);
        }
    })
    .catch(error => {
        document.querySelector('button[onclick="checkText()"]').innerHTML = originalText;
        document.querySelector('button[onclick="checkText()"]').disabled = false;
        showError(resultDiv, 'Error: ' + error.message);
    });
}

// Display URL result
function displayURLResult(resultDiv, data) {
    const riskClass = getRiskClass(data.risk_level);
    const riskIcon = getRiskIcon(data.risk_level);
    
    let html = `
        <div class="result-header ${riskClass}">
            ${riskIcon}
            <span>${data.risk_level.toUpperCase()}</span>
        </div>
        <div class="risk-score">
            <span>Risk Score:</span>
            <div class="risk-score-bar">
                <div class="risk-score-fill risk-${data.risk_level}" style="width: ${data.score}%"></div>
            </div>
            <span>${data.score}%</span>
        </div>
    `;
    
    if (data.indicators && data.indicators.length > 0) {
        html += '<h4 style="margin-top: 1rem;">Detected Issues:</h4><ul class="indicators-list">';
        data.indicators.forEach(indicator => {
            html += `<li><i class="fas fa-exclamation-circle"></i>${indicator}</li>`;
        });
        html += '</ul>';
    } else {
        html += '<p style="margin-top: 1rem;"><i class="fas fa-check-circle"></i> No phishing indicators detected.</p>';
    }
    
    resultDiv.innerHTML = html;
    resultDiv.style.display = 'block';
}

// Display general result
function displayResult(resultDiv, data) {
    const riskClass = getRiskClass(data.risk_level);
    const riskIcon = getRiskIcon(data.risk_level);
    
    let html = `
        <div class="result-header ${riskClass}">
            ${riskIcon}
            <span>${data.risk_level.toUpperCase()}</span>
        </div>
        <div class="risk-score">
            <span>Risk Score:</span>
            <div class="risk-score-bar">
                <div class="risk-score-fill risk-${data.risk_level}" style="width: ${data.score}%"></div>
            </div>
            <span>${data.score}%</span>
        </div>
    `;
    
    if (data.indicators && data.indicators.length > 0) {
        html += '<h4 style="margin-top: 1rem;">Detected Issues:</h4><ul class="indicators-list">';
        data.indicators.forEach(indicator => {
            html += `<li><i class="fas fa-exclamation-circle"></i>${indicator}</li>`;
        });
        html += '</ul>';
    } else {
        html += '<p style="margin-top: 1rem;"><i class="fas fa-check-circle"></i> No phishing indicators detected.</p>';
    }
    
    resultDiv.innerHTML = html;
    resultDiv.style.display = 'block';
}

// Show error message
function showError(resultDiv, message) {
    resultDiv.innerHTML = `
        <div class="result-header result-danger">
            <i class="fas fa-times-circle"></i>
            <span>ERROR</span>
        </div>
        <p>${message}</p>
    `;
    resultDiv.style.display = 'block';
}

// Get risk class for styling
function getRiskClass(riskLevel) {
    switch(riskLevel) {
        case 'critical':
        case 'high':
            return 'result-danger';
        case 'medium':
            return 'result-warning';
        case 'low':
            return 'result-success';
        default:
            return 'result-success';
    }
}

// Get risk icon
function getRiskIcon(riskLevel) {
    switch(riskLevel) {
        case 'critical':
        case 'high':
            return '<i class="fas fa-skull-crossbones"></i>';
        case 'medium':
            return '<i class="fas fa-exclamation-triangle"></i>';
        case 'low':
            return '<i class="fas fa-check-circle"></i>';
        default:
            return '<i class="fas fa-check-circle"></i>';
    }
}

// Load statistics
function loadStatistics() {
    const btn = document.querySelector('.refresh-btn');
    btn.classList.add('loading');
    
    fetch('/api/statistics', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        btn.classList.remove('loading');
        
        if (data.success) {
            document.getElementById('urlsChecked').textContent = data.data.urls_checked || 0;
            document.getElementById('emailsChecked').textContent = data.data.emails_checked || 0;
            document.getElementById('textsChecked').textContent = data.data.texts_checked || 0;
            document.getElementById('totalChecks').textContent = data.data.total_checks || 0;
        }
    })
    .catch(error => {
        btn.classList.remove('loading');
        console.error('Error:', error);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Handle mobile menu
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        });
    }
    
    // Load statistics on page load
    loadStatistics();
    
    // Refresh statistics every 30 seconds
    setInterval(loadStatistics, 30000);
    
    // Allow Enter key to submit
    document.getElementById('urlInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') checkURL();
    });
    
    document.getElementById('emailInput').addEventListener('keypress', function(e) {
        if (e.key === 'Ctrl+Enter' || (e.metaKey && e.key === 'Enter')) checkEmail();
    });
    
    document.getElementById('textInput').addEventListener('keypress', function(e) {
        if (e.key === 'Ctrl+Enter' || (e.metaKey && e.key === 'Enter')) checkText();
    });
});
