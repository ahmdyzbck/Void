#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog

APP_NAME = "VOID"

root = tk.Tk()
root.title(APP_NAME)
root.geometry("1000x700")
root.configure(bg="#1a1a1a")

# ── Text area ─────────────────────────────────────────────────────────────────
text_area = tk.Text(
    root,
    bg="#1a1a1a",
    fg="#e0e0e0",
    insertbackground="#e0e0e0",
    font=("JetBrains Mono", 13),
    relief="flat",
    bd=0,
    padx=60,
    pady=40,
    wrap="word",
    undo=True,
    highlightthickness=0,
    selectbackground="#3a3a3a",
    spacing3=4,
)
text_area.pack(fill="both", expand=True)
text_area.focus_set()

# ── File operations ───────────────────────────────────────────────────────────
current_file = None

def save_file(event=None):
    global current_file
    if current_file:
        with open(current_file, "w") as f:
            f.write(text_area.get("1.0", "end-1c"))
    else:
        save_as_file()

def save_as_file(event=None):
    global current_file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text files", "*.txt"),
            ("Markdown files", "*.md"),
            ("Python files", "*.py"),
            ("All files", "*.*"),
        ],
        title="Save file"
    )
    if file_path:
        current_file = file_path
        with open(current_file, "w") as f:
            f.write(text_area.get("1.0", "end-1c"))

def open_file(event=None):
    global current_file
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Text files", "*.txt"),
            ("Markdown files", "*.md"),
            ("Python files", "*.py"),
            ("All files", "*.*"),
        ],
        title="Open file"
    )
    if file_path:
        current_file = file_path
        with open(current_file, "r") as f:
            content = f.read()
        text_area.delete("1.0", "end")
        text_area.insert("1.0", content)

def new_file(event=None):
    global current_file
    text_area.delete("1.0", "end")
    current_file = None

root.bind("<Control-s>", save_file)
root.bind("<Control-s>", lambda e: save_as_file())
root.bind("<Control-o>", open_file)
root.bind("<Control-n>", new_file)

root.mainloop()