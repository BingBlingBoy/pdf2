from tkinter import *
from tkinter import ttk
from tkinter import font
import src.config as config

class PDFViewerUI:
    def __init__(self, master, controller) -> None:

        # MAIN WINDOW
        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(width=True, height=True)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        # self.master.iconbitmap(self.master, 'pdf_file_icon.ico')

        # CONTROLLER
        self.controller = controller

        self.uparrow_icon = PhotoImage(file='./assets/up-arrow.png').subsample(25)
        self.downarrow_icon = PhotoImage(file='./assets/down-arrow.png').subsample(25)
        self.zoom_in_icon = PhotoImage(file='./assets/plus.png').subsample(27)
        self.zoom_out_icon = PhotoImage(file='./assets/minus.png').subsample(25)

        self._init_menu()
        self._init_layout()

    def _init_menu(self) -> None:
        menu_font = font.Font(family="Arial", size=14)

        # MENU FRAME
        self.menu_frame = Frame(
            self.master,
            height=40,
            relief="raised",
            borderwidth=1
        )
        self.menu_frame.pack_propagate(False)
        self.menu_frame.pack(side="top", fill="x")

        # GROUPS
        self.left_group = Frame(self.menu_frame)
        self.left_group.pack(side="left", fill="y")
        self.right_group = Frame(self.menu_frame)
        self.right_group.pack(side="right", fill="y")
        self.center_group = Frame(self.menu_frame)
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


    def _init_layout(self) -> None:
        # TOP FRAMES
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.pack(side="top", fill="both", expand=True)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky="ns")
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky="we")

        # ADDING THE CANVAS TO THE TOP FRAME
        self.output = Canvas(
            self.top_frame,
            width=config.CANVAS_WIDTH,
            bg='#ECE8F3',
            highlightthickness=0,
            borderwidth=0
        )
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0, sticky='ns')

        self.scrolly.configure(command=self.output.yview)
        self.scrollx.configure(command=self.output.xview)

        self.output.bind('<Enter>', self._bound_to_mousewheel)
        self.output.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event) -> None:
        self.output.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event) -> None:
        self.output.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event) -> None:
        self.output.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_canvas(self, img_file) -> None:
        self.output.delete('all')
        self.output.config(width=img_file.width(), height=img_file.height())
        self.output.create_image(0, 0, anchor='nw', image=img_file)

        self.curr_image = img_file

        region = self.output.bbox("all")
        self.output.configure(scrollregion=region)

    def update_page_labels(self, current, total) -> None:
        self.curr_page_num['text'] = f"{current}"
        self.total_page_num['text'] = f"of {total}"
