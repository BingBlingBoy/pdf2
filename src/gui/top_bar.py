from tkinter import *
from tkinter import ttk
from tkinter import font
import src.config as config

class TopBar(Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, height=40, relief='raised', borderwidth=1, **kwargs)
        self.controller = controller
        self.pack_propagate(False)

        self.uparrow_icon = PhotoImage(file='./assets/up-arrow.png').subsample(25)
        self.downarrow_icon = PhotoImage(file='./assets/down-arrow.png').subsample(25)
        self.zoom_in_icon = PhotoImage(file='./assets/plus.png').subsample(27)
        self.zoom_out_icon = PhotoImage(file='./assets/minus.png').subsample(25)

        self._build_widgets()

    def _build_widgets(self) -> None:
        menu_font = font.Font(family="Arial", size=14)

        # GROUPS
        self.left_group = Frame(self)
        self.left_group.pack(side="left", fill="y")
        self.right_group = Frame(self)
        self.right_group.pack(side="right", fill="y")
        self.center_group = Frame(self)
        self.center_group.pack(side="left", expand=True, fill="y")

        # FILE MENU
        self.file_menu_btn = Menubutton(
            self.left_group,
            text="File",
            relief="flat",
            font=menu_font,
        )
        self.file_menu_btn.pack(side="left", padx=(0, 80))
        self.file_menu = Menu(self.file_menu_btn, tearoff=0, font=menu_font)
        self.file_menu_btn.config(menu=self.file_menu)
        self.file_menu.add_command(label="Open File", command=self.controller.prompt_open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)

        # UP AND DOWN BUTTONS
        self.btn_up = Button(
            self.left_group,
            image=self.uparrow_icon,
            compound="left",
            command=self.controller.previous_page,
            relief="flat",
            # bg="#f0f0f0",
            # activebackground="#cce8ff",
            borderwidth=0
        )
        self.btn_up.pack(side="left", padx=5)

        self.btn_down = Button(
            self.left_group,
            image=self.downarrow_icon,
            compound="left",
            command=self.controller.next_page,
            relief="flat",
            # bg="#f0f0f0",
            # activebackground="#cce8ff",
            borderwidth=0
        )
        self.btn_down.pack(side='left', padx=5)

        # PAGE LABELS
        self.curr_page_num = Label(
            self.left_group,
            font=menu_font,
            bg='#FFFFFF',
            width=5,
            anchor='e',
            padx=5
        )
        self.curr_page_num.pack(side='left', padx=5)
        self.total_page_num = Label(self.left_group, font=menu_font)
        self.total_page_num.pack(side='left', padx=5)

        # ZOOM CONTROLS
        self.zoom_in_btn = Button(
            self.center_group,
            image=self.zoom_in_icon,
            compound='left',
            relief='flat',
            borderwidth=0,
            # command=lambda: self.display_page(self.zoom_ratio + 0.2)
            command=self.controller.zoom_in
        )
        self.zoom_in_btn.pack(side='left', padx=5)

        self.zoom_separator = ttk.Separator(self.center_group, orient='vertical')
        self.zoom_separator.pack(side='left', fill='y', padx=5)

        self.zoom_out_btn = Button(
            self.center_group,
            image=self.zoom_out_icon,
            compound='left',
            relief='flat',
            borderwidth=0,
            # command=lambda: self.display_page(self.zoom_ratio - 0.2)
            command=self.controller.zoom_out
        )
        self.zoom_out_btn.pack(side='left', padx=5)
        self.zoom_dropdown = ttk.Combobox(
            self.center_group,
            values=list(config.ZOOM_DICT.keys()),
            state='readonly',
            font=("Arial", 14)
        )
        self.zoom_dropdown.pack(side='left', padx=5)
        self.zoom_dropdown.set('Automatic Zoom')
        self.zoom_dropdown.bind("<<ComboboxSelected>>", self.controller.on_zoom_select)

    def set_zoom_text(self, text):
        self.zoom_dropdown.set(text)

    def update_page_labels(self, current, total):
        self.curr_page_num['text'] = f"{current}"
        self.total_page_num['text'] = f"of {total}"
