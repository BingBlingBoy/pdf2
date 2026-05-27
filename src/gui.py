from tkinter import *
import os
from tkinter import ttk
from tkinter import filedialog as fd
from src.miner import PDFMiner

CANVAS_WIDTH = 1100

class PDFViewer:
    def __init__(self, master, initial_file=None) -> None:
        self.path = None
        self.fileisopen = None
        self.author = None
        self.name = None
        self.current_page = 0 
        self.numPages = None

        # MAIN WINDOW
        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(width=True, height=True)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        # self.master.iconbitmap(self.master, 'pdf_file_icon.ico')

        self.uparrow_icon = PhotoImage(file='./assets/up-arrow.png').subsample(25)
        self.downarrow_icon = PhotoImage(file='./assets/down-arrow.png').subsample(25)

        self._init_menu()
        self._init_layout()
        self._init_control()

        if initial_file:
            self.load_pdf(initial_file)

    def _init_menu(self) -> None:
        self.menu_frame = Frame(
            self.master,
            relief="raised",
            borderwidth=1
        )
        self.menu_frame.pack(side="top", fill="x")

        self.file_menu_btn = Menubutton(
            self.menu_frame,
            text="File",
            relief="flat"
        )
        self.file_menu_btn.pack(side="left", padx=5)

        self.file_menu = Menu(self.file_menu_btn, tearoff=0)
        self.file_menu_btn.config(menu=self.file_menu)
        self.file_menu.add_command(label="Open File", command=self.prompt_open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)

        self.btn_up = Button(
            self.menu_frame,
            # text="Up",
            image=self.uparrow_icon,
            compound="left",
            command=self.previous_page,
            relief="flat",
            # bg="#f0f0f0",
            # activebackground="#cce8ff",
            borderwidth=0
        )
        self.btn_up.pack(side="left", padx=5)

        self.btn_down = Button(
            self.menu_frame,
            # text="Down",
            image=self.downarrow_icon,
            compound="left",
            command=self.next_page,
            relief="flat",
            # bg="#f0f0f0",
            # activebackground="#cce8ff",
            borderwidth=0
        )
        self.btn_down.pack(side="left", padx=5)

    def _init_layout(self) -> None:
        # TOP AND BOTTOM FRAMES
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
            width=CANVAS_WIDTH,
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

    def _bound_to_mousewheel(self, event):
        self.output.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.output.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.output.yview_scroll(int(-1*(event.delta/120)), "units")

    def _init_control(self) -> None:
        # ADDING UP, DOWN BUTTONS AND THE LABEL TO THE BOTTOM FRAME
        self.scrollx.configure(command=self.output.xview)
        # self.page_label = ttk.Label(self.bottom_frame, text='page')
        # self.page_label.grid(row=0, column=3, padx=5)

    def prompt_open_file(self) -> None:
        filepath = fd.askopenfilename(
            title='Select a PDF file', 
            initialdir=os.getcwd(), 
            filetypes=(('PDF', '*.pdf'), )
        )
        if filepath:
            self.load_pdf(filepath)

    def load_pdf(self, filepath: str) -> None:
        self.path = filepath
        filename = os.path.basename(self.path)

        self.miner = PDFMiner(self.path)
        data, numPages = self.miner.get_metadata()

        self.current_page = 0
        if numPages and isinstance(data, dict):
            self.name = data.get('title', filename[:-4])
            self.author = data.get('author', None)
            self.numPages = numPages

            self.fileisopen = True
            self.master.title(f"PDF Viewer - {self.name}")
            self.display_page()

    def display_page(self) -> None:
        if self.numPages is not None and 0 <= self.current_page < self.numPages:
            self.master.update_idletasks()

            target_width = self.output.winfo_width()
            if target_width <= 1:
                target_width = self.master.winfo_width()

            self.img_file = self.miner.get_page(self.current_page, target_width=target_width)
            self.output.delete('all')

            self.output.config(width=self.img_file.width(), height=self.img_file.height())
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)

            self.stringified_current_page = self.current_page + 1
            # self.page_label['text'] = str(self.stringified_current_page) + 'of' + str(self.numPages)

            region = self.output.bbox(ALL)
            self.output.configure(scrollregion=region)

    def next_page(self) -> None:
        if self.fileisopen:
            if self.numPages is not None and self.current_page <= self.numPages - 1:
                self.current_page += 1
                self.display_page()

    def previous_page(self) -> None:
        if self.fileisopen:
            if self.current_page > 0:
                self.current_page -= 1
                self.display_page()
