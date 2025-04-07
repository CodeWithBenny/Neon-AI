import subprocess
from typing import List, Optional


class VersionControl:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def git_status(self) -> List[str]:
        """Get git status"""
        return self._run_git_command(['status', '--porcelain'])

    def git_commit(self, message: str) -> bool:
        """Commit changes with message"""
        result = self._run_git_command(['commit', '-am', message])
        return "nothing to commit" not in '\n'.join(result)

    def git_diff(self) -> str:
        """Get git diff"""
        return '\n'.join(self._run_git_command(['diff']))

    def _run_git_command(self, args: List[str]) -> Optional[List[str]]:
        """Run git command and return output lines"""
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.stdout.splitlines()
        except subprocess.CalledProcessError:
            return None