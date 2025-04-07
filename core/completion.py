from typing import List, Dict
import random


class CodeCompleter:
    def __init__(self):
        self.language_models = {
            "python": self._python_completer,
            "javascript": self._javascript_completer,
            "java": self._java_completer
        }

    def complete(self, code: str, language: str = "python", context: Dict = None) -> List[str]:
        completer = self.language_models.get(language.lower(), self._generic_completer)
        return completer(code, context)

    def _python_completer(self, code: str, context: Dict) -> List[str]:
        suggestions = []

        # Basic keyword completion
        if "import " in code:
            suggestions.extend(["numpy", "pandas", "os", "sys"])

        # Function completion
        if "def " in code and "(" in code and "):" not in code:
            suggestions.append(code.split("(")[0] + "):\n    pass")

        # List comprehension
        if "for " in code and " in " in code and "[" not in code:
            var = code.split("for ")[1].split(" in ")[0]
            suggestions.append(f"[x for x in {var}]")

        return suggestions[:3]

    def _javascript_completer(self, code: str, context: Dict) -> List[str]:
        suggestions = []

        if "function " in code and "(" in code and "){" not in code:
            suggestions.append(code.split("(")[0] + ") {\n  // TODO\n}")

        if "const " in code and "=" not in code:
            suggestions.append(code + " = null;")

        return suggestions[:3]

    def _generic_completer(self, code: str, context: Dict) -> List[str]:
        return ["// TODO: Implement this", "/* Your code here */"]