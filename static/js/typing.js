class TypingAnimation {
    constructor() {
        this.textElement = document.getElementById('typing-text');
        this.messages = [
            "Hello! I'm your AI coding assistant. I can help you with:",
            "Code completion ✨",
            "Error debugging 🐛",
            "Code explanations 📚",
            "Performance optimizations ⚡",
            "Start typing to begin..."
        ];
        this.currentMessage = 0;
        this.charIndex = 0;
        this.isDeleting = false;
        this.typingSpeed = 100;
        this.pauseBetween = 2000;

        this.init();
    }

    init() {
        setTimeout(() => this.type(), 1000);
    }

    type() {
        const currentText = this.messages[this.currentMessage];

        if (this.isDeleting) {
            this.charIndex--;
            this.textElement.textContent = currentText.substring(0, this.charIndex);

            if (this.charIndex === 0) {
                this.isDeleting = false;
                this.currentMessage = (this.currentMessage + 1) % this.messages.length;
                setTimeout(() => this.type(), this.typingSpeed);
                return;
            }
        } else {
            this.charIndex++;
            this.textElement.textContent = currentText.substring(0, this.charIndex);

            if (this.charIndex === currentText.length) {
                this.isDeleting = true;
                setTimeout(() => this.type(), this.pauseBetween);
                return;
            }
        }

        setTimeout(() => this.type(), this.typingSpeed);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new TypingAnimation();
});