import re
from typing import List, Dict


class CodeDebugger:
    def __init__(self):
        self.error_patterns = {
            "python": [
                {
                    "pattern": r"NameError: name '(.+?)' is not defined",
                    "fix": "The variable '{0}' is not defined. You need to declare it first.",
                    "example": "x = 5  # Define the variable before using it"
                },
                {
                    "pattern": r"IndentationError:",
                    "fix": "Python requires consistent indentation. Check your tabs/spaces.",
                    "example": "def foo():\n    print('indented')"
                }
            ],
            "javascript": [
                {
                    "pattern": r"TypeError: Cannot read property '(.+?)' of undefined",
                    "fix": "You're trying to access property '{0}' on an undefined object.",
                    "example": "if (obj && obj.property) { /* safe access */ }"
                }
            ]
        }

    def analyze(self, code: str, error: str, language: str = "python") -> Dict:
        language_patterns = self.error_patterns.get(language, [])

        for pattern in language_patterns:
            match = re.search(pattern["pattern"], error)
            if match:
                fix = pattern["fix"].format(*match.groups())
                return {
                    "error": error,
                    "fix": fix,
                    "example": pattern.get("example", ""),
                    "confidence": 0.9
                }

        return {
            "error": error,
            "fix": "I couldn't find a specific fix for this error. Please check the documentation.",
            "confidence": 0.1
        }

    def static_analysis(self, code: str, language: str = "python") -> List[Dict]:
        issues = []

        # Unused variable detection
        if language == "python":
            vars = re.findall(r"^\s*(\w+)\s*=", code, re.MULTILINE)
            used_vars = re.findall(r"\b(" + "|".join(vars) + r")\b", code)
            unused = set(vars) - set(used_vars)
            for var in unused:
                issues.append({
                    "type": "unused_variable",
                    "message": f"Variable '{var}' is defined but never used",
                    "severity": "warning"
                })

        return issues