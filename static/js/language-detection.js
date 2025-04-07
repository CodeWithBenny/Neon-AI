class LanguageDetector {
    constructor() {
        this.editor = document.getElementById('editor');
        this.languageBadge = document.getElementById('language-badge');
        this.languageName = document.getElementById('language-name');
        this.languageMap = {
            'python': { name: 'Python', color: '#3776ab' },
            'javascript': { name: 'JavaScript', color: '#f7df1e' },
            'java': { name: 'Java', color: '#007396' },
            'c': { name: 'C', color: '#555555' },
            'cpp': { name: 'C++', color: '#00599c' }
        };
        this.lastLanguage = null;

        this.init();
    }

    init() {
        this.editor.addEventListener('input', this.detectLanguage.bind(this));
    }

    detectLanguage() {
        const code = this.editor.textContent;
        if (!code.trim()) {
            this.setLanguage('auto', 'Detecting...');
            return;
        }

        // Simple pattern matching
        let detectedLang = 'python'; // default

        if (code.includes('function') && (code.includes('{') || code.includes('=>'))) {
            detectedLang = 'javascript';
        } else if (code.includes('#include') || code.includes('printf(') || code.includes('->')) {
            detectedLang = 'c';
        } else if (code.includes('public class') || code.includes('System.out.print')) {
            detectedLang = 'java';
        } else if (code.includes('using namespace') || code.includes('std::')) {
            detectedLang = 'cpp';
        } else if (code.includes('def ') || code.includes('import ') || code.includes('lambda ')) {
            detectedLang = 'python';
        }

        if (detectedLang !== this.lastLanguage) {
            this.setLanguage(detectedLang, this.languageMap[detectedLang].name);
            this.lastLanguage = detectedLang;
        }
    }

    setLanguage(langCode, langName) {
        if (langCode === 'auto') {
            this.languageBadge.textContent = 'Auto';
            this.languageBadge.style.background = 'linear-gradient(135deg, #6e48aa, #4776e6)';
            this.languageName.textContent = langName;
            return;
        }

        const langInfo = this.languageMap[langCode];
        this.languageBadge.textContent = langCode;
        this.languageBadge.style.background = langInfo.color;
        this.languageName.textContent = langInfo.name;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LanguageDetector();
});