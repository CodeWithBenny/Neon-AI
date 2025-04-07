class TerminalManager {
    constructor() {
        this.terminal = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#1e1e1e',
                foreground: '#f8f8f8'
            }
        });
        this.socket = new WebSocket(`ws://${window.location.host}/terminal`);

        this.init();
    }

    init() {
        this.terminal.open(document.getElementById('terminal-container'));

        this.terminal.onData(data => {
            this.socket.send(JSON.stringify({
                type: 'input',
                data: data
            }));
        });

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.terminal.write(data.output);
        };

        // Fit terminal to container
        this.fitTerminal();
        window.addEventListener('resize', () => this.fitTerminal());
    }

    fitTerminal() {
        const fitAddon = new FitAddon.FitAddon();
        this.terminal.loadAddon(fitAddon);
        fitAddon.fit();
    }

    execute(command) {
        this.socket.send(JSON.stringify({
            type: 'command',
            command: command
        }));
    }
}