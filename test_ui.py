import tkinter as tk
import unittest

from app import UnitConverterApp


def find_buttons(widget: tk.Misc):
    for child in widget.winfo_children():
        if isinstance(child, tk.Button):
            yield child
        yield from find_buttons(child)


class KeypadLayoutTests(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            self.skipTest(f"Tk is unavailable: {exc}")
        self.root.withdraw()
        self.app = UnitConverterApp(self.root)
        self.root.update_idletasks()

    def tearDown(self) -> None:
        self.root.destroy()

    def test_all_digits_are_on_the_expected_grid_cells(self) -> None:
        expected = {
            "7": (0, 0),
            "8": (0, 1),
            "9": (0, 2),
            "4": (1, 0),
            "5": (1, 1),
            "6": (1, 2),
            "1": (2, 0),
            "2": (2, 1),
            "3": (2, 2),
            "0": (3, 1),
        }
        buttons = {
            button.cget("text"): button
            for button in find_buttons(self.root)
        }

        for label, (row, column) in expected.items():
            self.assertIn(label, buttons)
            grid = buttons[label].grid_info()
            self.assertEqual((int(grid["row"]), int(grid["column"])), (row, column))

    def test_direction_controls_support_both_modes(self) -> None:
        labels = {button.cget("text") for button in find_buttons(self.root)}
        self.assertIn("厘米  →  米", labels)
        self.assertIn("米  →  厘米", labels)

    def test_default_conversion_still_works(self) -> None:
        self.app.input_value.set("150")
        self.app._convert()

        self.assertEqual(self.app.input_unit_value.get(), "厘米")
        self.assertEqual(self.app.result_value.get(), "1.5 米")

    def test_reverse_conversion_updates_result_and_units(self) -> None:
        self.app._set_direction("m_to_cm")
        self.app.input_value.set("1.5")
        self.app._convert()

        self.assertEqual(self.app.input_unit_value.get(), "米")
        self.assertEqual(self.app.convert_button.cget("text"), "换算为厘米")
        self.assertEqual(self.app.result_value.get(), "150 厘米")


if __name__ == "__main__":
    unittest.main()
