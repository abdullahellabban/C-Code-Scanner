import re
import tkinter as tk
from tkinter import scrolledtext

TOKEN_SPECIFICATION = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('NUMBER', r'\b\d+(\.\d*)?\b'),
    ('KEYWORD', r'\b(int|float|char|double|if|else|while|for|return|void|include|main)\b'),
    ('STRING', r'"([^"\\]*(\\.[^"\\]*)*)"' ),
    ('CHAR', r"'.'"),
    ('OPERATOR', r'[+\-*/%=&|!<>]=?|&&|\|\|'),
    ('SpecialCharacter', r'[;,{}()\[\]]'),
    ('WHITESPACE', r'\s+'),
    ('NEWLINE', r'\n'),
    ('IDENTIFIER', r'\b[A-Za-z_]\w*\b'),
]

TOKEN_REGEX = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

TOKEN_COLORS = {
    'NUMBER': 'blue',
    'IDENTIFIER': 'black',
    'KEYWORD': 'purple',
    'STRING': 'orange',
    'CHAR': 'orange',
    'OPERATOR': 'red',
    'SpecialCharacter': 'green',
    'COMMENT': 'gray',
    'WHITESPACE': 'white'
}

def tokenize(code):
    tokens = []
    line_number = 1
    
    for match in re.finditer(TOKEN_REGEX, code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        
        if token_type == 'WHITESPACE':
            continue
        
        tokens.append((token_type, token_value, line_number))
        
        if token_type == 'NEWLINE':
            line_number += 1

    return tokens

class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C Code Scanner")
        self.root.geometry("700x500")
        self.root.configure(bg='#f2f2f2')
        
        title_label = tk.Label(root, text="C Code Scanner", font=("Arial", 16), bg='#4CAF50', fg='white')
        title_label.pack(pady=10, fill=tk.X)
        
        self.code_input = scrolledtext.ScrolledText(root, width=80, height=10, font=("Courier", 10))
        self.code_input.pack(pady=10)
        
        self.scan_button = tk.Button(root, text="Scan Code", font=("Arial", 12), bg='#4CAF50', fg='white', command=self.scan_code)
        self.scan_button.pack(pady=5)
        
        self.output = scrolledtext.ScrolledText(root, width=80, height=15, font=("Courier", 10), state='disabled')
        self.output.pack(pady=10)
        
        for token_type, color in TOKEN_COLORS.items():
            self.output.tag_configure(token_type, foreground=color)

    def scan_code(self):
        code = self.code_input.get("1.0", tk.END)
        tokens = tokenize(code)
        
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
