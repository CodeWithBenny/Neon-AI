class CodeRefactorer:
    def refactor(self, code: str, language: str = "python") -> Dict:
        suggestions = []

        if language == "python":
            # Suggest list comprehension
            if "for " in code and " in " in code and "append(" in code:
                var_match = re.search(r"for (\w+) in", code)
                list_match = re.search(r"(\w+)\.append", code)
                if var_match and list_match:
                    new_var = var_match.group(1)
                    list_name = list_match.group(1)
                    suggestions.append({
                        "description": "Use list comprehension instead of append",
                        "original": code,
                        "refactored": f"[x for x in {new_var}]",
                        "confidence": 0.8
                    })

            # Suggest f-strings
            if "%" in code or ".format(" in code:
                suggestions.append({
                    "description": "Use f-strings for better readability",
                    "original": code,
                    "refactored": code.replace("%s", "{var}").replace(".format(", "f\""),
                    "confidence": 0.9
                })

        return {"suggestions": suggestions}