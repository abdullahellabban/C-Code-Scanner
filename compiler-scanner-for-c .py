import re
import tkinter as tk
from tkinter import scrolledtext

# Define token types with regular expressions for C language
TOKEN_SPECIFICATION = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),      # Comments (moved to the top)
    ('NUMBER', r'\b\d+(\.\d*)?\b'),           # Integer or decimal number
    ('KEYWORD', r'\b(int|float|char|double|if|else|while|for|return|void|include|main)\b'),  # C Keywords
    ('STRING', r'"([^"\\]*(\\.[^"\\]*)*)"' ), # String literals
    ('CHAR', r"'.'"),                         # Character literals
    ('OPERATOR', r'[+\-*/%=&|!<>]=?|&&|\|\|'), # Operators
    ('SEPARATOR', r'[;,{}()\[\]]'),           # Separators
    ('WHITESPACE', r'\s+'),                   # Whitespace
    ('NEWLINE', r'\n'),                       # Newline
    ('IDENTIFIER', r'\b[A-Za-z_]\w*\b'),      # Identifiers
]

# Compile the regular expressions into patterns
TOKEN_REGEX = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

# Color scheme for different token types
TOKEN_COLORS = {
    'NUMBER': 'blue',
    'IDENTIFIER': 'black',
    'KEYWORD': 'purple',
    'STRING': 'orange',
    'CHAR': 'orange',
    'OPERATOR': 'red',
    'SEPARATOR': 'green',
    'COMMENT': 'gray',
    'WHITESPACE': 'white'
}

def tokenize(code):
    """
    Tokenize the input code and return a list of tokens.
    """
    tokens = []
    line_number = 1
    
    # Iterate over matches in the code
    for match in re.finditer(TOKEN_REGEX, code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        
        # Skip whitespace
        if token_type == 'WHITESPACE':
            continue
        
        tokens.append((token_type, token_value, line_number))
        
        # Track new lines for correct line numbering
        if token_type == 'NEWLINE':
            line_number += 1

    return tokens

class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C Code Scanner")
        self.root.geometry("700x500")
        self.root.configure(bg='#f2f2f2')  # Background color
        
        # Title label
        title_label = tk.Label(root, text="C Code Scanner", font=("Arial", 16), bg='#4CAF50', fg='white')
        title_label.pack(pady=10, fill=tk.X)
        
        # Create text input for code
        self.code_input = scrolledtext.ScrolledText(root, width=80, height=10, font=("Courier", 10))
        self.code_input.pack(pady=10)
        
        # Button to scan code
        self.scan_button = tk.Button(root, text="Scan Code", font=("Arial", 12), bg='#4CAF50', fg='white', command=self.scan_code)
        self.scan_button.pack(pady=5)
        
        # Text output for tokens
        self.output = scrolledtext.ScrolledText(root, width=80, height=15, font=("Courier", 10), state='disabled')
        self.output.pack(pady=10)
        
        # Configure output tags for coloring
        for token_type, color in TOKEN_COLORS.items():
            self.output.tag_configure(token_type, foreground=color)

    def scan_code(self):
        # Get code from input
        code = self.code_input.get("1.0", tk.END)
        
        # Scan and tokenize the code
        tokens = tokenize(code)
        
        # Display tokens in the output box
        self.output.configure(state='normal')
        self.output.delete("1.0", tk.END)
        
        if tokens:
            for token in tokens:
                token_info = f"{token[0]:<10} | '{token[1]}'\n"
                self.output.insert(tk.END, token_info, token[0])
        else:
            self.output.insert(tk.END, "No tokens found.")
        
        self.output.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()
