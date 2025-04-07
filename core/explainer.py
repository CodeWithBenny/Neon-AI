class CodeExplainer:
    def explain(self, code: str, language: str = "python") -> str:
        explanations = {
            "python": {
                "lambda": "A lambda function is a small anonymous function defined with the lambda keyword.",
                "list_comp": "List comprehension provides a concise way to create lists based on existing lists."
            },
            "javascript": {
                "=>": "Arrow functions provide a shorter syntax for writing functions and lexically bind the 'this' value."
            }
        }

        # Try to match known patterns
        for pattern, explanation in explanations.get(language, {}).items():
            if pattern in code:
                return explanation

        # Fallback explanation
        return f"This appears to be {language} code. It's performing some operations that I can't specifically identify."