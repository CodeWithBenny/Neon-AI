class CollaborationClient {
    constructor(roomId) {
        this.roomId = roomId;
        this.userId = crypto.randomUUID();
        this.socket = new WebSocket(`ws://${window.location.host}/collab/${roomId}`);
        this.cursors = {};

        this.init();
    }

    init() {
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        // Send cursor position updates
        document.addEventListener('mousemove', (e) => {
            const position = this.getCursorPosition();
            this.send({
                type: 'cursor',
                position: position,
                userId: this.userId
            });
        });
    }

    handleMessage(data) {
        switch(data.type) {
            case 'cursor':
                this.updateRemoteCursor(data.userId, data.position);
                break;
            case 'edit':
                this.applyRemoteEdit(data);
                break;
        }
    }

    updateRemoteCursor(userId, position) {
        if (!this.cursors[userId]) {
            this.createCursorElement(userId);
        }
        this.cursors[userId].style.left = `${position.x}px`;
        this.cursors[userId].style.top = `${position.y}px`;
    }

    createCursorElement(userId) {
        const cursor = document.createElement('div');
        cursor.className = 'remote-cursor';
        cursor.style.backgroundColor = this.getUserColor(userId);
        cursor.textContent = userId.slice(0, 2);
        document.body.appendChild(cursor);
        this.cursors[userId] = cursor;
    }

    getUserColor(userId) {
        const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'];
        const index = parseInt(userId.replace(/\D/g, ''), 10) % colors.length;
        return colors[index];
    }

    sendEdit(change) {
        this.send({
            type: 'edit',
            change: change,
            userId: this.userId
        });
    }

    send(message) {
        if (this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(message));
        }
    }
}