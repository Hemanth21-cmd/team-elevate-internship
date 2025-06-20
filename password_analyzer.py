import tkinter as tk
from tkinter import messagebox
import zxcvbn
import itertools
import re

class PasswordAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Analyzer & Wordlist Generator")
        self.root.geometry("400x500")

        # Password Strength Section
        tk.Label(root, text="Enter Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(root, text="Analyze Password", command=self.analyze_password).pack(pady=5)
        self.result_label = tk.Label(root, text="", wraplength=350)
        self.result_label.pack(pady=5)

        # Wordlist Generator Section
        tk.Label(root, text="Wordlist Inputs").pack(pady=10)
        tk.Label(root, text="Name:").pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)
        tk.Label(root, text="Date (e.g., 1990):").pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)
        tk.Label(root, text="Pet Name:").pack()
        self.pet_entry = tk.Entry(root)
        self.pet_entry.pack(pady=5)
        tk.Button(root, text="Generate Wordlist", command=self.generate_wordlist).pack(pady=10)

    def analyze_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        result = zxcvbn.zxcvbn(password)
        score = result['score']
        feedback = result['feedback']['suggestions']
        feedback_text = "\n".join(feedback) if feedback else "No suggestions."
        self.result_label.config(text=f"Strength Score: {score}/4\nSuggestions:\n{feedback_text}")

    def generate_wordlist(self):
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()
        pet = self.pet_entry.get().strip()
        if not (name or date or pet):
            messagebox.showerror("Error", "Please provide at least one input")
            return

        wordlist = set()
        inputs = [name, pet] if name and pet else [name or pet]
        if date and re.match(r"^\d{4}$", date):
            inputs.append(date)

        # Add basic inputs
        for inp in inputs:
            if inp:
                wordlist.add(inp)
                wordlist.add(inp.lower())
                wordlist.add(inp.upper())
                wordlist.add(inp.capitalize())

        # Add leetspeak variations
        leet_dict = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
        for inp in inputs:
            if inp:
                for chars in itertools.product(*[(c, leet_dict.get(c.lower(), c)) for c in inp]):
                    wordlist.add(''.join(chars))

        # Add year suffixes
        if date:
            for inp in inputs:
                if inp:
                    for year in [date, str(int(date) % 100)]:
                        wordlist.add(inp + year)
                        wordlist.add(inp.lower() + year)
                        wordlist.add(inp.upper() + year)

        # Save wordlist to file
        try:
            with open("wordlist.txt", "w") as f:
                for word in sorted(wordlist):
                    f.write(word + "\n")
            messagebox.showinfo("Success", "Wordlist saved as wordlist.txt")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save wordlist: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerApp(root)
    root.mainloop()