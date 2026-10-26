import tkinter as tk
from tkinter import messagebox

from converter import centimeters_to_meters, format_meters


BACKGROUND = "#000000"
DISPLAY_BACKGROUND = "#111111"
TEXT = "#ffffff"
MUTED = "#8e8e93"
DIGIT_KEY = "#333333"
DIGIT_KEY_ACTIVE = "#484848"
FUNCTION_KEY = "#a5a5a5"
FUNCTION_KEY_ACTIVE = "#d4d4d4"
ACTION_KEY = "#ff9f0a"
ACTION_KEY_ACTIVE = "#ffb340"


class UnitConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.input_value = tk.StringVar(value="0")
        self.result_value = tk.StringVar(value="等待换算")

        self._configure_window()
        self._build_display()
        self._build_keypad()
        self._bind_keyboard_shortcuts()

    def _configure_window(self) -> None:
        self.root.title("厘米换算器")
        self.root.configure(bg=BACKGROUND)
        self.root.geometry("390x680")
        self.root.minsize(360, 620)

    def _build_display(self) -> None:
        display = tk.Frame(
            self.root,
            bg=DISPLAY_BACKGROUND,
            padx=24,
            pady=20,
        )
        display.pack(fill="x", padx=18, pady=(18, 10))

        tk.Label(
            display,
            text="厘米  →  米",
            bg=DISPLAY_BACKGROUND,
            fg=MUTED,
            font=("Microsoft YaHei UI", 13),
            anchor="e",
        ).pack(fill="x")

        self.input_entry = tk.Entry(
            display,
            textvariable=self.input_value,
            bg=DISPLAY_BACKGROUND,
            fg=TEXT,
            insertbackground=TEXT,
            justify="right",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 44),
        )
        self.input_entry.pack(fill="x", pady=(12, 4), ipady=4)
        self.input_entry.focus_set()
        self.input_entry.select_range(0, "end")

        tk.Label(
            display,
            text="厘米",
            bg=DISPLAY_BACKGROUND,
            fg=MUTED,
            font=("Microsoft YaHei UI", 12),
            anchor="e",
        ).pack(fill="x")

        tk.Frame(display, bg="#2c2c2e", height=1).pack(fill="x", pady=12)

        tk.Label(
            display,
            textvariable=self.result_value,
            bg=DISPLAY_BACKGROUND,
            fg=TEXT,
            font=("Segoe UI", 22),
            anchor="e",
        ).pack(fill="x")

    def _build_keypad(self) -> None:
        keypad = tk.Frame(self.root, bg=BACKGROUND)
        keypad.pack(fill="both", expand=True, padx=12, pady=(0, 14))

        for column in range(3):
            keypad.grid_columnconfigure(column, weight=1, uniform="keys")

        key_rows = (
            ("7", "8", "9"),
            ("4", "5", "6"),
            ("1", "2", "3"),
            ("C", "0", "."),
        )
        for row_index, row in enumerate(key_rows[:3]):
            for column_index, label in enumerate(row):
                self._add_key(
                    keypad,
                    row_index,
                    column_index,
                    label,
                    lambda value=label: self._append_value(value),
                )

        self._add_key(
            keypad,
            3,
            0,
            "C",
            self._clear,
            key_type="function",
        )
        self._add_key(
            keypad,
            3,
            1,
            "0",
            lambda: self._append_value("0"),
        )
        self._add_key(
            keypad,
            3,
            2,
            ".",
            lambda: self._append_value("."),
        )

        self._add_key(
            keypad,
            4,
            0,
            "DEL",
            self._backspace,
            key_type="function",
        )
        convert_button = self._add_key(
            keypad,
            4,
            1,
            "换算为米",
            self._convert,
            key_type="action",
            columnspan=2,
        )
        convert_button.configure(font=("Microsoft YaHei UI", 17, "bold"))

    def _add_key(
        self,
        parent: tk.Frame,
        row: int,
        column: int,
        label: str,
        command,
        *,
        key_type: str = "digit",
        columnspan: int = 1,
    ) -> tk.Button:
        palettes = {
            "digit": (DIGIT_KEY, DIGIT_KEY_ACTIVE, TEXT),
            "function": (FUNCTION_KEY, FUNCTION_KEY_ACTIVE, BACKGROUND),
            "action": (ACTION_KEY, ACTION_KEY_ACTIVE, TEXT),
        }
        background, active_background, foreground = palettes[key_type]

        button = tk.Button(
            parent,
            text=label,
            command=command,
            bg=background,
            fg=foreground,
            activebackground=active_background,
            activeforeground=foreground,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            font=("Segoe UI", 20),
            takefocus=True,
        )
        button.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="nsew",
            padx=6,
            pady=6,
        )
        return button

    def _bind_keyboard_shortcuts(self) -> None:
        self.root.bind("<Return>", lambda _event: self._convert())
        self.root.bind("<KP_Enter>", lambda _event: self._convert())
        self.root.bind("<Escape>", lambda _event: self._clear())

    def _append_value(self, value: str) -> None:
        current = self.input_value.get()

        if value == "." and "." in current:
            return
        if current == "0" and value != ".":
            current = ""
        if current == "0" and value == ".":
            current = "0"

        self.input_value.set(f"{current}{value}")
        self.input_entry.icursor("end")
        self.input_entry.focus_set()

    def _clear(self) -> None:
        self.input_value.set("0")
        self.result_value.set("等待换算")
        self.input_entry.focus_set()
        self.input_entry.select_range(0, "end")

    def _backspace(self) -> None:
        current = self.input_value.get()
        self.input_value.set(current[:-1] if len(current) > 1 else "0")
        self.input_entry.icursor("end")
        self.input_entry.focus_set()

    def _convert(self) -> None:
        try:
            meters = centimeters_to_meters(self.input_value.get())
        except ValueError as exc:
            messagebox.showerror("输入有误", str(exc), parent=self.root)
            self.input_entry.focus_set()
            return

        self.result_value.set(f"{format_meters(meters)} 米")


def main() -> None:
    root = tk.Tk()
    UnitConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
