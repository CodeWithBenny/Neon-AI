from .completion import CodeCompleter
from .debugger import CodeDebugger
from .documentation import DocumentationGenerator
from .explainer import CodeExplainer
from .learning import LearningEngine
from .refactor import CodeRefactorer
from .snippets import SnippetGenerator
from .version_control import VersionControlHelper

class AICodingAssistant:
    def __init__(self):
        self.completer = CodeCompleter()
        self.debugger = CodeDebugger()
        self.docs = DocumentationGenerator()
        self.explainer = CodeExplainer()
        self.learner = LearningEngine()
        self.refactorer = CodeRefactorer()
        self.snippets = SnippetGenerator()
        self.vcs = VersionControlHelper()