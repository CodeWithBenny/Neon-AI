from typing import List, Dict
import re


class CodeReviewer:
    def __init__(self):
        self.review_rules = {
            "python": [
                {
                    "pattern": r"except:\s*pass",
                    "message": "Bare except clause - specify exception type",
                    "severity": "high"
                },
                {
                    "pattern": r"def \w+\(\):\s*pass",
                    "message": "Empty function implementation",
                    "severity": "medium"
                }
            ],
            "javascript": [
                {
                    "pattern": r"console\.log\(",
                    "message": "Debugging statement left in code",
                    "severity": "low"
                }
            ]
        }

    def review_code(self, code: str, language: str) -> List[Dict]:
        """Analyze code for potential issues"""
        issues = []
        for rule in self.review_rules.get(language, []):
            for match in re.finditer(rule["pattern"], code):
                issues.append({
                    "line": code[:match.start()].count('\n') + 1,
                    "message": rule["message"],
                    "severity": rule["severity"],
                    "code": match.group()
                })
        return issues