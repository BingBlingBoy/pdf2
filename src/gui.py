from tkinter import *
import os
from tkinter import ttk
from tkinter import filedialog as fd
from src.miner import PDFMiner

CANVAS_WIDTH = 1000

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
        # self.master.iconbitmap(self.master, 'pdf_file_icon.ico')

        self._init_menu()
        self._init_layout()
        self._init_control()

        if initial_file:
            self.load_pdf(initial_file)



    def _init_menu(self) -> None:
        # ADDING MENU
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File", command=self.prompt_open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)

    def _init_layout(self) -> None:
        # TOP AND BOTTOM FRAMES
        self.top_frame = ttk.Frame(self.master)
        self.top_frame.grid(row=0, column=0, sticky='nsew')

        # Top frame takes up all the space
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, weight=1)

        # Bottom frame is responsible for the buttons
        self.bottom_frame = ttk.Frame(self.master, height=50)
        self.bottom_frame.grid(row=1, column=0, sticky='ew')

        # VERTICAL AND HORIZONTAL SCROLLBARS
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky="ns")

        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky="we")

        # ADDING THE CANVAS TO THE TOP FRAME AND CONFIGURING ITS SCROLLBARS
        self.output = Canvas(
            self.top_frame,
            bg='#ECE8F3',
            highlightthickness=0,
            borderwidth=0
        )
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0, sticky='n')

        self.scrolly.configure(command=self.output.yview)
        self.scrollx.configure(command=self.output.xview)

    def _init_control(self) -> None:
        # ADDING UP, DOWN BUTTONS AND THE LABEL TO THE BOTTOM FRAME
        self.scrollx.configure(command=self.output.xview)
        self.uparrow_icon = PhotoImage(file='./assets/up-arrow.png')
        self.downarrow_icon = PhotoImage(file='./assets/down-arrow.png')

        self.uparrow = self.uparrow_icon.subsample(25)
        self.downarrow = self.downarrow_icon.subsample(25)

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.columnconfigure(4, weight=1)

        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow, command=self.previous_page)
        self.upbutton.grid(row=0, column=1, padx=5, pady=8)

        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow, command=self.next_page)
        self.downbutton.grid(row=0, column=2, pady=8)

        self.page_label = ttk.Label(self.bottom_frame, text='page')
        self.page_label.grid(row=0, column=3, padx=5)

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
            self.img_file = self.miner.get_page(self.current_page)
            self.output.delete('all')

            pdf_width = self.img_file.width()
            pdf_height = self.img_file.height()
            
            self.output.config(width=pdf_width, height=pdf_height)

            self.output.create_image(0, 0, anchor='nw', image=self.img_file)

            self.stringified_current_page = self.current_page + 1
            self.page_label['text'] = str(self.stringified_current_page) + 'of' + str(self.numPages)

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
