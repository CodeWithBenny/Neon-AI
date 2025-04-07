class ThemeSwitcher {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.currentTheme = localStorage.getItem('theme') || 'dark';

        this.init();
    }

    init() {
        this.setTheme(this.currentTheme);

        this.themeToggle.addEventListener('click', () => {
            this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
            this.setTheme(this.currentTheme);
            localStorage.setItem('theme', this.currentTheme);
        });
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);

        // Update toggle icon
        const icon = this.themeToggle.querySelector('i');
        icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ThemeSwitcher();
});