import subprocess
from typing import List, Optional


class VersionControlHelper:
    def get_git_diff(self) -> Optional[str]:
        try:
            return subprocess.check_output(["git", "diff"], text=True)
        except subprocess.CalledProcessError:
            return None

    def generate_commit_message(self, diff: str) -> str:
        if "def " in diff:
            return "Add new function"
        if "fix" in diff.lower():
            return "Fix bug"
        if "import " in diff:
            return "Add dependencies"
        return "Update code"

    def suggest_git_commands(self, action: str) -> List[str]:
        commands = {
            "undo": ["git checkout -- <file>", "git reset HEAD <file>"],
            "branch": ["git branch <name>", "git checkout -b <name>"],
            "merge": ["git merge <branch>", "git rebase <branch>"]
        }
        return commands.get(action, ["git status"])