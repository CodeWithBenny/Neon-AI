import subprocess
from typing import Optional


class TerminalEmulator:
    def __init__(self):
        self.process = None

    def start(self):
        """Start a new terminal session"""
        if not self.process:
            self.process = subprocess.Popen(
                ['bash'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
                shell=True
            )
        return True

    def execute(self, command: str) -> Optional[str]:
        """Execute a command and return output"""
        if not self.process:
            self.start()

        try:
            self.process.stdin.write(command + '\n')
            self.process.stdin.flush()
            output = []
            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                output.append(line)
            return ''.join(output)
        except Exception as e:
            return f"Error: {str(e)}"

    def stop(self):
        """Terminate the terminal session"""
        if self.process:
            self.process.terminate()
            self.process = None