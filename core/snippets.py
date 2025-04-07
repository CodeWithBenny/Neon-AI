import json
import os
from typing import Dict, List


class SnippetGenerator:
    def __init__(self, snippets_dir="data/snippets"):
        self.snippets_dir = snippets_dir
        os.makedirs(snippets_dir, exist_ok=True)
        self.snippets = self._load_snippets()

    def _load_snippets(self) -> Dict:
        snippets = {}
        for lang_file in os.listdir(self.snippets_dir):
            if lang_file.endswith(".json"):
                lang = lang_file.split(".")[0]
                with open(os.path.join(self.snippets_dir, lang_file)) as f:
                    snippets[lang] = json.load(f)
        return snippets

    def get_snippet(self, name: str, language: str = "python") -> str:
        return self.snippets.get(language, {}).get(name, "")

    def generate_boilerplate(self, framework: str, language: str) -> str:
        if framework.lower() == "flask" and language == "python":
            return """from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run()"""

        elif framework.lower() == "express" and language == "javascript":
            return """const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})"""

        return f"// {framework} boilerplate code for {language}"