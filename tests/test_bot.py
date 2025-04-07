import unittest
from core import AICodingAssistant


class TestAICodingAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = AICodingAssistant()

    def test_code_completion(self):
        suggestions = self.assistant.completer.complete("import ", "python")
        self.assertTrue(len(suggestions) > 0)

    def test_error_debugging(self):
        analysis = self.assistant.debugger.analyze(
            "print(x)",
            "NameError: name 'x' is not defined",
            "python"
        )
        self.assertIn("define", analysis["fix"].lower())

    def test_documentation_generation(self):
        docstring = self.assistant.docs.generate_docstring(
            "def foo(bar):", "python"
        )
        self.assertIn("Args:", docstring)


if __name__ == "__main__":
    unittest.main()