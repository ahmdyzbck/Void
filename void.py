#!/usr/bin/env python3

import json
import os
import tkinter as tk
from pathlib import Path
from tkinter import (
    filedialog,
    messagebox,
    simpledialog,
)

APP_NAME = "VOID"
CONFIG_FILE = Path.home() / ".void_config.json"


class VoidEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a1a")

        # Editor state
        self.current_file = None
        self.modified = False
        self.last_directory = Path.home()

        self.load_settings()

        self.create_editor()
        self.create_status_bar()
        self.create_menu()
        self.bind_shortcuts()

        self.text.edit_modified(False)

        self.text.bind("<<Modified>>", self.on_modified)
        self.text.bind("<KeyRelease>", self.update_status)
        self.text.bind("<ButtonRelease>", self.update_status)

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.exit_editor,
        )

        self.update_title()
        self.update_status()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def create_editor(self):
        self.text = tk.Text(
            self.root,
            bg="#1a1a1a",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            relief="flat",
            bd=0,
            wrap="word",
            undo=True,
            padx=60,
            pady=40,
            font=("JetBrains Mono", 13),
            highlightthickness=0,
            selectbackground="#404040",
            spacing3=4,
        )

        scrollbar = tk.Scrollbar(
            self.root,
            command=self.text.yview,
        )

        self.text.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.text.pack(
            fill="both",
            expand=True,
        )

        self.text.focus_set()

    def create_status_bar(self):
        self.status = tk.Label(
            self.root,
            text="",
            anchor="w",
            bg="#202020",
            fg="#bdbdbd",
            padx=10,
            pady=4,
            font=("Segoe UI", 9),
        )

        self.status.pack(
            side="bottom",
            fill="x",
        )

    def create_menu(self):
        menu = tk.Menu(self.root)

        file_menu = tk.Menu(
            menu,
            tearoff=False,
        )

        file_menu.add_command(
            label="New",
            accelerator="Ctrl+N",
            command=self.new_file,
        )

        file_menu.add_command(
            label="Open...",
            accelerator="Ctrl+O",
            command=self.open_file,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Save",
            accelerator="Ctrl+S",
            command=self.save_file,
        )

        file_menu.add_command(
            label="Save As...",
            accelerator="Ctrl+Shift+S",
            command=self.save_as,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.exit_editor,
        )

        menu.add_cascade(
            label="File",
            menu=file_menu,
        )

        edit_menu = tk.Menu(
            menu,
            tearoff=False,
        )

        edit_menu.add_command(
            label="Undo",
            accelerator="Ctrl+Z",
            command=lambda: self.text.event_generate("<<Undo>>"),
        )

        edit_menu.add_command(
            label="Redo",
            accelerator="Ctrl+Y",
            command=lambda: self.text.event_generate("<<Redo>>"),
        )

        edit_menu.add_separator()

        edit_menu.add_command(
            label="Cut",
            accelerator="Ctrl+X",
            command=lambda: self.text.event_generate("<<Cut>>"),
        )

        edit_menu.add_command(
            label="Copy",
            accelerator="Ctrl+C",
            command=lambda: self.text.event_generate("<<Copy>>"),
        )

        edit_menu.add_command(
            label="Paste",
            accelerator="Ctrl+V",
            command=lambda: self.text.event_generate("<<Paste>>"),
        )

        edit_menu.add_separator()

        edit_menu.add_command(
            label="Select All",
            accelerator="Ctrl+A",
            command=self.select_all,
        )

        edit_menu.add_command(
            label="Find",
            accelerator="Ctrl+F",
            command=self.find_text,
        )

        menu.add_cascade(
            label="Edit",
            menu=edit_menu,
        )

        self.root.config(menu=menu)

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def update_title(self):
        if self.current_file:
            name = Path(self.current_file).name
        else:
            name = "Untitled"

        if self.modified:
            self.root.title(f"{APP_NAME} - {name} *")
        else:
            self.root.title(f"{APP_NAME} - {name}")

    def update_status(self, event=None):
        cursor = self.text.index("insert")

        line, column = cursor.split(".")

        content = self.text.get(
            "1.0",
            "end-1c",
        )

        words = len(content.split())
        chars = len(content)

        self.status.config(
            text=(
                f"Ln {line}, Col {int(column)+1}"
                f"     Words: {words}"
                f"     Characters: {chars}"
            )
        )

    def on_modified(self, event=None):
        if self.text.edit_modified():
            self.modified = True
            self.update_title()
            self.text.edit_modified(False)

    def select_all(self):
        self.text.tag_add(
            "sel",
            "1.0",
            "end",
        )
        return "break"

    # --------------------------------------------------
    # Settings
    # --------------------------------------------------

    def load_settings(self):
        if CONFIG_FILE.exists():
            try:
                with open(
                    CONFIG_FILE,
                    "r",
                    encoding="utf-8",
                ) as f:
                    data = json.load(f)

                self.last_directory = Path(
                    data.get(
                        "last_directory",
                        str(Path.home()),
                    )
                )

            except Exception:
                pass

    def save_settings(self):
        try:
            with open(
                CONFIG_FILE,
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    {
                        "last_directory":
                        str(self.last_directory)
                    },
                    f,
                    indent=4,
                )

        except Exception:
            pass

    # --------------------------------------------------
    # Keyboard shortcuts
    # --------------------------------------------------

    def bind_shortcuts(self):
        self.root.bind(
            "<Control-n>",
            self.new_file,
        )

        self.root.bind(
            "<Control-o>",
            self.open_file,
        )

        self.root.bind(
            "<Control-s>",
            self.save_file,
        )

        self.root.bind(
            "<Control-S>",
            self.save_as,
        )

        self.root.bind(
            "<Control-f>",
            self.find_text,
        )

        self.root.bind(
            "<Control-a>",
            lambda e: self.select_all(),
        )

        self.root.bind(
            "<Control-z>",
            lambda e:
            self.text.event_generate("<<Undo>>"),
        )

        self.root.bind(
            "<Control-y>",
            lambda e:
            self.text.event_generate("<<Redo>>"),
        )

    # --------------------------------------------------
    # Remaining methods
    # (Implemented in Part 2)
    # --------------------------------------------------

    def new_file(self, event=None):
        pass

    def open_file(self, event=None):
        pass

    def save_file(self, event=None):
        pass

    def save_as(self, event=None):
        pass

    def find_text(self, event=None):
        pass

    def confirm_unsaved(self):
        pass

    def exit_editor(self):
        pass


        # --------------------------------------------------
    # File Operations
    # --------------------------------------------------

    def new_file(self, event=None):
        if not self.confirm_unsaved():
            return "break"

        self.text.delete("1.0", "end")

        self.current_file = None
        self.modified = False

        self.text.edit_modified(False)

        self.update_title()
        self.update_status()
        self.text.focus_set()

        return "break"

    def open_file(self, event=None):
        if not self.confirm_unsaved():
            return "break"

        file_path = filedialog.askopenfilename(
            title="Open File",
            initialdir=self.last_directory,
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("Python files", "*.py"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            self.text.focus_set()
            return "break"

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as f:
                content = f.read()

        except Exception as e:
            messagebox.showerror(
                "Open Error",
                f"Could not open file.\n\n{e}",
            )
            return "break"

        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)

        self.current_file = file_path
        self.last_directory = Path(file_path).parent

        self.modified = False

        self.text.edit_modified(False)

        self.save_settings()

        self.update_title()
        self.update_status()

        self.text.focus_set()

        return "break"

    def save_file(self, event=None):
        if self.current_file is None:
            return self.save_as()

        try:
            with open(
                self.current_file,
                "w",
                encoding="utf-8",
            ) as f:
                f.write(
                    self.text.get(
                        "1.0",
                        "end-1c",
                    )
                )

        except Exception as e:
            messagebox.showerror(
                "Save Error",
                f"Could not save file.\n\n{e}",
            )
            return "break"

        self.modified = False
        self.text.edit_modified(False)

        self.update_title()
        self.update_status()

        self.text.focus_set()

        return "break"

    def save_as(self, event=None):
        file_path = filedialog.asksaveasfilename(
            title="Save File",
            initialdir=self.last_directory,
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("Python files", "*.py"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            self.text.focus_set()
            return "break"

        self.current_file = file_path
        self.last_directory = Path(file_path).parent

        self.save_settings()

        return self.save_file()

    # --------------------------------------------------
    # Find
    # --------------------------------------------------

    def find_text(self, event=None):
        search = simpledialog.askstring(
            "Find",
            "Find:",
            parent=self.root,
        )

        if not search:
            self.text.focus_set()
            return "break"

        self.text.tag_remove(
            "find",
            "1.0",
            "end",
        )

        start = "1.0"
        count = 0

        while True:
            pos = self.text.search(
                search,
                start,
                stopindex="end",
                nocase=True,
            )

            if not pos:
                break

            end = f"{pos}+{len(search)}c"

            self.text.tag_add(
                "find",
                pos,
                end,
            )

            start = end
            count += 1

        self.text.tag_config(
            "find",
            background="#5b4a00",
            foreground="#ffffff",
        )

        if count:
            first = self.text.tag_ranges("find")[0]
            self.text.see(first)
            self.text.mark_set(
                "insert",
                first,
            )
        else:
            messagebox.showinfo(
                "Find",
                "No matches found.",
            )

        self.text.focus_set()

        return "break"

    # --------------------------------------------------
    # Unsaved Changes
    # --------------------------------------------------

    def confirm_unsaved(self):
        if not self.modified:
            return True

        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "Save changes before continuing?",
        )

        if answer is None:
            return False

        if answer:
            result = self.save_file()

            if self.modified:
                return False

        return True
    

        # --------------------------------------------------
    # Exit
    # --------------------------------------------------

    def exit_editor(self):
        if not self.confirm_unsaved():
            return

        self.save_settings()
        self.root.destroy()

    # --------------------------------------------------
    # Run
    # --------------------------------------------------

    def run(self):
        self.text.focus_set()
        self.root.mainloop()


# ------------------------------------------------------
# Entry Point
# ------------------------------------------------------

def main():
    editor = VoidEditor()
    editor.run()


if __name__ == "__main__":
    main()
    