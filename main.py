import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pyperclip
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class CodeToHtmlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code to HTML Converter")

        # Create a frame for the code input and line numbers
        code_frame = ttk.Frame(root)
        code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.code_text = tk.Text(code_frame, wrap=tk.NONE, width=50, height=20)
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.scrollbar = ttk.Scrollbar(code_frame, orient=tk.VERTICAL, command=self.code_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_text.config(yscrollcommand=self.scrollbar.set)

        self.line_numbers = tk.Text(code_frame, width=4, height=20)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame for buttons and options
        button_frame = ttk.Frame(root)
        button_frame.pack(padx=10, pady=(0, 10))

        self.convert_button = ttk.Button(button_frame, text="Convert to HTML", command=self.convert_to_html)
        self.convert_button.pack(side=tk.LEFT)

        self.copy_button = ttk.Button(button_frame, text="Copy HTML", command=self.copy_html)
        self.copy_button.pack(side=tk.LEFT)

        self.save_button = ttk.Button(button_frame, text="Save HTML", command=self.save_html)
        self.save_button.pack(side=tk.LEFT)

        self.syntax_label = ttk.Label(button_frame, text="Select Syntax:")
        self.syntax_label.pack(side=tk.LEFT)

        self.syntax_var = tk.StringVar()
        self.syntax_combobox = ttk.Combobox(button_frame, textvariable=self.syntax_var, values=[
            "python", "java", "javascript", "c", "c++", "html", "css", "php", "ruby"
        ])
        self.syntax_combobox.pack(side=tk.LEFT)
        self.syntax_combobox.set("python")

        self.copy_button["state"] = "disabled"
        self.save_button["state"] = "disabled"

    def convert_to_html(self):
        code = self.code_text.get("1.0", "end-1c")
        syntax = self.syntax_var.get()

        if not code:
            return

        lexer = get_lexer_by_name(syntax, stripall=True)
        formatter = HtmlFormatter(style='colorful', linenos=True)

        code_highlighted = highlight(code, lexer, formatter)

        self.html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .code-container {{
                    background-color: white;
                }}
                {formatter.get_style_defs('.highlight')}
            </style>
        </head>
        <body>
            <div class="code-container">
                {code_highlighted}
            </div>
        </body>
        </html>
        """

        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", "\n".join(str(i) for i in range(1, code_highlighted.count('\n') + 2)))

        self.copy_button["state"] = "active"
        self.save_button["state"] = "active"

    def copy_html(self):
        if hasattr(self, 'html_content'):
            pyperclip.copy(self.html_content)
            self.show_message("Copy", "HTML code copied to clipboard.")
        else:
            self.show_message("Warning", "No HTML code to copy.")

    def save_html(self):
        if hasattr(self, 'html_content'):
            file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.html_content)
        else:
            pass 
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeToHtmlApp(root)
    root.mainloop()
