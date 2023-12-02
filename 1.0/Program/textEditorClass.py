import os
import re
from datetime import datetime
from PySide6.QtWidgets import QTextEdit

class TextEditorWidget:
    def __init__(self):
        # Create the notes text edit area from a log file
        self.text_editor = QTextEdit()

        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Create log.txt in the same directory as the current script
        self.log_path = os.path.join(dir_path, "log.txt")
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w'): pass

        # Read the file and start the editing on a newline
        with open(self.log_path, 'r') as file:
            content = file.read()
        if content and content[-1] != "\n":
            content += "\n"

        # Add timestamp to each new line
        lines = content.split("\n")
        for i in range(len(lines)):
            if lines[i] != "" and not re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}: ", lines[i]):
                lines[i] = datetime.now().strftime("%m/%d/%Y %H:%M:%S: ") + lines[i]
        content = "\n".join(lines)
        self.text_editor.setText(content)