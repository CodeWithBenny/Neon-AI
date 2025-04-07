class CodingAssistantApp {
    constructor() {
        this.editor = document.getElementById('editor');
        this.completeBtn = document.getElementById('complete-btn');
        this.explainBtn = document.getElementById('explain-btn');
        this.copyBtn = document.getElementById('copy-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.responseContent = document.getElementById('response-content');
        this.languageBadge = document.getElementById('language-badge');
        
        this.socket = new WebSocket(`ws://${window.location.host}/ws`);
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupSocket();
    }
    
    setupEventListeners() {
        this.completeBtn.addEventListener('click', () => this.sendCompletionRequest());
        this.explainBtn.addEventListener('click', () => this.sendExplanationRequest());
        this.copyBtn.addEventListener('click', () => this.copyResponse());
        this.clearBtn.addEventListener('click', () => this.clearResponse());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.sendCompletionRequest();
            }
        });
    }
    
    setupSocket() {
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            switch(data.type) {
                case 'suggestions':
                    this.showSuggestions(data.data, data.detected_language);
                    break;
                case 'explanation':
                    this.showExplanation(data.data, data.detected_language);
                    break;
            }
        };
        
        this.socket.onclose = () => {
            this.showError("Connection to server lost. Please refresh the page.");
        };
    }
    
    sendCompletionRequest() {
        const code = this.editor.textContent.trim();
        if (!code) return;
        
        this.showTypingIndicator();
        this.socket.send(JSON.stringify({
            action: 'complete',
            code: code
        }));
    }
    
    sendExplanationRequest() {
        const code = this.editor.textContent.trim();
        if (!code) return;
        
        this.showTypingIndicator();
        this.socket.send(JSON.stringify({
            action: 'explain',
            code: code
        }));
    }
    
    showTypingIndicator() {
        this.responseContent.innerHTML = `
            <div class="response-message">
                <div class="message-header">
                    <div class="message-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <span>AI Assistant</span>
                </div>
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        this.scrollToBottom();
    }
    
    showSuggestions(suggestions, language) {
        let html = '';
        
        suggestions.forEach((suggestion, index) => {
            html += `
                <div class="response-message">
                    <div class="message-header">
                        <div class="message-avatar">
                            <i class="fas fa-lightbulb"></i>
                        </div>
                        <span>Suggestion ${index + 1}</span>
                        <span class="language-tag" style="background: ${this.getLanguageColor(language)}">
                            ${language}
                        </span>
                    </div>
                    <div class="message-content">
                        <pre>${this.escapeHtml(suggestion)}</pre>
                        <button class="suggestion-btn" onclick="insertSuggestion('${this.escapeHtml(suggestion)}')">
                            <i class="fas fa-copy"></i> Insert Suggestion
                        </button>
                    </div>
                </div>
            `;
        });
        
        this.responseContent.innerHTML = html;
        this.scrollToBottom();
    }
    
    showExplanation(explanation, language) {
        const html = `
            <div class="response-message">
                <div class="message-header">
                    <div class="message-avatar">
                        <i class="fas fa-info-circle"></i>
                    </div>
                    <span>Code Explanation</span>
                    <span class="language-tag" style="background: ${this.getLanguageColor(language)}">
                        ${language}
                    </span>
                </div>
                <div class="message-content">
                    ${this.formatExplanation(explanation)}
                </div>
            </div>
        `;
        
        this.responseContent.innerHTML = html;
        this.scrollToBottom();
    }
    
    showError(message) {
        const html = `
            <div class="response-message error">
                <div class="message-header">
                    <div class="message-avatar">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <span>Error</span>
                </div>
                <div class="message-content">
                    ${message}
                </div>
            </div>
        `;
        
        this.responseContent.innerHTML += html;
        this.scrollToBottom();
    }
    
    formatExplanation(text) {
        // Simple formatting for code blocks
        return text.replace(/`([^`]+)`/g, '<code>$1</code>')
                  .replace(/\n/g, '<br>');
    }
    
    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
            .replace(/\n/g, "<br>");
    }
    
    getLanguageColor(lang) {
        const colors = {
            'python': '#3776ab',
            'javascript': '#f7df1e',
            'java': '#007396',
            'c': '#555555',
            'cpp': '#00599c'
        };
        return colors[lang] || '#6e48aa';
    }
    
    copyResponse() {
        const text = this.responseContent.textContent;
        navigator.clipboard.writeText(text).then(() => {
            const originalText = this.copyBtn.innerHTML;
            this.copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                this.copyBtn.innerHTML = originalText;
            }, 2000);
        });
    }
    
    clearResponse() {
        this.responseContent.innerHTML = `
            <div class="welcome-message">
                <p>Ready for your next request...</p>
            </div>
        `;
    }
    
    scrollToBottom() {
        this.responseContent.scrollTop = this.responseContent.scrollHeight;
    }
}

// Global function to insert suggestions
function insertSuggestion(suggestion) {
    const editor = document.getElementById('editor');
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    
    // Remove HTML tags from suggestion
    const cleanSuggestion = suggestion.replace(/<[^>]*>/g, '');
    
    // Insert at cursor position
    range.deleteContents();
    range.insertNode(document.createTextNode(cleanSuggestion));
    
    // Move cursor to end of inserted text
    range.setStartAfter(range.endContainer);
    range.setEndAfter(range.endContainer);
    selection.removeAllRanges();
    selection.addRange(range);
    
    editor.focus();
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CodingAssistantApp();
    
    // Make insertSuggestion available globally
    window.insertSuggestion = insertSuggestion;
});