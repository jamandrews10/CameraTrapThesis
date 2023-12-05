import os
import re
from datetime import datetime
from PySide6.QtWidgets import QTextEdit

class TextEditorWidget:
    def __init__(self):
        # Create the notes text edit area from a log file
        self.textEditor = QTextEdit()

        # Get the directory of the current script
        dirPath = os.path.dirname(os.path.realpath(__file__))

        # Create log.txt in the same directory as the current script
        self.logPath = os.path.join(dirPath, "log.txt")
        if not os.path.exists(self.logPath):
            with open(self.logPath, 'w'): pass

        # Read the file and start the editing on a newline
        with open(self.logPath, 'r') as file:
            content = file.read()
        if content and content[-1] != "\n":
            content += "\n"

        # Add timestamp to each new line
        lines = content.split("\n")
        for i in range(len(lines)):
            if lines[i] != "" and not re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}: ", lines[i]):
                lines[i] = datetime.now().strftime("%m/%d/%Y %H:%M:%S: ") + lines[i]
        content = "\n".join(lines)
        self.textEditor.setText(content)