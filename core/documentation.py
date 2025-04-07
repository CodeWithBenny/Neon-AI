from typing import List


class DocumentationGenerator:
    def generate_docstring(self, code: str, language: str = "python") -> str:
        if language == "python":
            if code.strip().startswith("def "):
                func_name = code.split("def ")[1].split("(")[0]
                params = self._extract_parameters(code)
                return self._python_function_docstring(func_name, params)
        return "/* Documentation */"

    def _extract_parameters(self, code: str) -> List[str]:
        if "(" in code and ")" in code:
            param_str = code.split("(")[1].split(")")[0]
            return [p.strip() for p in param_str.split(",") if p.strip()]
        return []

    def _python_function_docstring(self, func_name: str, params: List[str]) -> str:
        doc = f'"""\n{func_name}\n\n'
        if params:
            doc += "Args:\n"
            for param in params:
                doc += f"    {param}: Description\n"
        doc += "\nReturns:\n    Description\n"""
        return doc