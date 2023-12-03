"""
A generalized GUI Builder
@author Connor McCloskey

Requirements:
Python 3.10 or later
CustomTKinter module
PyInstaller module

** To produce executable with PyInstaller **
pyinstaller --onefile -w -F main.py
--OR--
pyinstaller GuiBuilder.spec

-- TO DO --
Most of this is easy, but this is a side project of a side project of a side project, so I'm lazy.

- Create "new button" popup, ability to attach script, name it, etc.
- Make it so draggables can't go into the side frame...
- Save/load configurations with JSON
- Add a "settings" file so a user can autoload a configuration on startup
    -- or maybe this should be project-based? That would work basically the same. A project could just point to a config
- Add button grid snapping
- Add "global" script functionality for user to further modify behavior (script that autoloads on startup)
- Add button "locking" feature to toggle between "build" and "use" modes
"""
# region Imports
import customtkinter as ctk
from tkinter import filedialog, Menu
# import json     # will use JSONs to save/load configurations
# endregion


class ButtonFactory(ctk.CTkToplevel):

    parent: None
    confirm_button: ctk.CTkButton
    quit_button: ctk.CTkButton
    script_path: ctk.CTkEntry

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_button(self):
        new_button = ctk.CTkButton(self.parent, text="New Button", font=self.parent.font)
        self.parent.assets.append(new_button)
        self.parent.register_draggable(new_button)
        new_button.place(x=200, y=50)
        self.parent.bIsMakingNewButton = False
        self.destroy()

    def back_button(self):
        self.parent.bIsMakingNewButton = False
        self.destroy()

    def start(self, parent):
        self.geometry("700x500")
        self.parent = parent
        self.title("Create Your Button")

        # Confirm Button
        self.confirm_button = ctk.CTkButton(self, text="Create Button", command=self.make_button, font=parent.font)
        self.confirm_button.place(x=20, y=20)

        # Quit Button
        self.quit_button = ctk.CTkButton(self, text="Back", command=self.back_button, font=parent.font)
        self.quit_button.place(x=20, y=450)

        # Path for script
        self.script_path = ctk.CTkEntry(self, placeholder_text="Button Script")
        self.script_path.place(x=20, y=60)


# region App class
class App(ctk.CTk):
    # region Members
    assets: list
    font: ctk.CTkFont
    bIsMakingNewButton = False
    # endregion

    # region Methods
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
        self.open_file_button = ctk.CTkButton(self.side_frame, text="Open File", command=self.open_file, font=self.font)
        self.open_file_button.grid(row=0, column=0, padx=20, pady=20)

        self.load_button = ctk.CTkButton(self.side_frame, text="Load Configuration", font=self.font)
        self.load_button.grid(row=1, column=0, padx=20, pady=10)

        self.save_button = ctk.CTkButton(self.side_frame, text="Save Configuration", font=self.font)
        self.save_button.grid(row=2, column=0, padx=20, pady=10)

        self.sample_draggable = ctk.CTkButton(self, text="Sample Draggable", font=self.font)
        self.sample_draggable.place(x=200, y=20)
        self.register_draggable(self.sample_draggable)

        self.add_button = ctk.CTkButton(self.side_frame, text="+", font=self.font, command=self.new_button)
        self.add_button.grid(row=3, column=0, padx=20, pady=10)

        # Get current state and bind a state check function to the window's configure event
        self.current_state = self.wm_state()
        self.bind("<Configure>", self.state_check)

        # Loading up a list of all assets in the scene
        self.assets.append(self.open_file_button)
        self.assets.append(self.save_button)
        self.assets.append(self.load_button)
        self.assets.append(self.add_button)
        self.assets.append(self.sample_draggable)

        # Context menu
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Option1")
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Option2")
        self.bind("<Button-3>", self.create_context_menu)

    def create_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def state_check(self, _event):
        if self.current_state != self.wm_state():
            self.current_state = self.wm_state()
            # self.bounds_check(self.button_b)
            for i in self.assets:
                self.bounds_check(i)

    # noinspection PyMethodMayBeStatic
    def open_file(self) -> None:
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
        self.button_maker_window()
        # new_button = ctk.CTkButton(self, text="New Button", font=self.font)
        # self.assets.append(new_button)
        # new_button.place(x=200, y=50)
        # self.register_draggable(new_button)

    # In progress, but CTkToplevel is broken maybe?
    def button_maker_window(self) -> None:
        if self.bIsMakingNewButton is True:
            return
        self.bIsMakingNewButton = True
        button_maker = ButtonFactory()
        button_maker.start(self)
        button_maker.after(201, button_maker.focus)     # Stupid hack found on GitHub, CTK repo, issue 1219

    # noinspection PyMethodMayBeStatic
    def run_script(self, script: str) -> None:
        # Ensure the string is a valid Python file
        if script[-2:] != "py":
            return
        exec(open(script).read())

    def save_configuration(self):
        pass

    def load_configuration(self):
        pass
    # endregion
# endregion


# region Main
def main():
    app = App()
    app.after(3, app.wm_state, 'zoomed')
    app.mainloop()


if __name__ == '__main__':
    main()
# endregion
