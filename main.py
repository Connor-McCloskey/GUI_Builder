"""
Checking out CustomTKinter and PyInstaller!
@author Connor McCloskey

To produce executable:
pyinstaller --onefile -w -F main.py
--OR--
pyinstaller GuiBuilder.spec
"""
import customtkinter as ctk
from tkinter import filedialog


class App(ctk.CTk):

    assets: list
    font: ctk.CTkFont

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.font = ctk.CTkFont("Calibri", 14)
        self.assets = []

        # Init app state
        self.geometry("700x500")
        self.title("Evil Pear Productions GUI Tool")
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self.side_frame = ctk.CTkFrame(self)
        self.side_frame.grid(row=0, column=0, sticky="ns")

        # Create buttons
        self.button = ctk.CTkButton(self.side_frame, text="Open File", command=self.button_func, font=self.font)
        self.button.grid(row=0, column=0, padx=20, pady=20)

        self.load_button = ctk.CTkButton(self.side_frame, text="Load Configuration", font=self.font)
        self.load_button.grid(row=1, column=0, padx=20, pady=10)

        self.save_button = ctk.CTkButton(self.side_frame, text="Save Configuration", font=self.font)
        self.save_button.grid(row=2, column=0, padx=20, pady=10)

        self.button_b = ctk.CTkButton(self, text="Draggable", font=self.font)
        self.button_b.place(x=200, y=20)
        self.register_draggable(self.button_b)

        self.add_button = ctk.CTkButton(self.side_frame, text="+", font=self.font, command=self.new_button)
        self.add_button.grid(row=3, column=0, padx=20, pady=10)

        # Get current state and bind a state check function to the window's configure event
        self.current_state = self.wm_state()
        self.bind("<Configure>", self.state_check)

        # Loading up a list of all assets in the scene
        self.assets.append(self.button)
        self.assets.append(self.save_button)
        self.assets.append(self.button_b)

    def state_check(self, _event):
        if self.current_state != self.wm_state():
            self.current_state = self.wm_state()
            self.bounds_check(self.button_b)

    # noinspection PyMethodMayBeStatic
    def button_func(self) -> None:
        # path = filedialog.askdirectory()
        path2 = filedialog.askopenfile()
        print(path2)

    def bounds_check(self, widget) -> None:
        width = widget.winfo_width()
        height = widget.winfo_height()
        if widget.winfo_x() + width > self.winfo_width():
            x = self.winfo_width() - width
            widget.place(x=x)
        if widget.winfo_x() <= 0:
            widget.place(x=0)
        if widget.winfo_y() + height > self.winfo_height():
            y = self.winfo_height() - height
            widget.place(y=y)
        if widget.winfo_y() <= 0:
            widget.place(y=0)

    # noinspection PyMethodMayBeStatic
    def on_drag_start(self, event) -> None:
        widget = event.widget.master
        widget.drag_start_x = event.x
        widget.drag_start_y = event.y

    # noinspection PyMethodMayBeStatic
    def on_drag_motion(self, event) -> None:
        widget = event.widget.master
        x = widget.winfo_x() - widget.drag_start_x + event.x
        y = widget.winfo_y() - widget.drag_start_y + event.y
        widget.place(x=x, y=y)

    def on_drag_release(self, event) -> None:
        self.bounds_check(event.widget.master)

    # noinspection PyMethodMayBeStatic
    def register_draggable(self, widget) -> None:
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.bind("<ButtonRelease-1>", self.on_drag_release)

    def new_button(self) -> None:
        new_button = ctk.CTkButton(self, text="New Button", font=self.font)
        self.assets.append(new_button)
        new_button.place(x=200, y=50)
        self.register_draggable(new_button)


def main():
    app = App()
    app.after(3, app.wm_state, 'zoomed')
    app.mainloop()


if __name__ == '__main__':
    main()
