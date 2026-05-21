import argparse
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
import os

class PDFViewer:
    def __init__(self, master) -> None:
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
        self.master.resizable(width=0, height=0)
        # self.master.iconbitmap(self.master, 'pdf_file_icon.ico')

        # ADDING MENU
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File")
        self.filemenu.add_command(label="Exit")

        # TOP AND BOTTOM FRAMES
        self.top_frame = ttk.Frame(self.master, width=580, height=460)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)

        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid_propagate(False)

        # VERTICAL AND HORIZONTAL SCROLLBARS
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky="ns")
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky="we")

        # ADDING THE CANVAS TO THE TOP FRAME AND CONFIGURING ITS SCROLLBARS
        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0)
        self.scrolly.configure(command=self.output.yview)
        self.scrollx.configure(command=self.output.xview)

        # ADDING UP, DOWN BUTTONS AND THE LABEL TO THE BOTTOM FRAME
        self.scrollx.configure(command=self.output.xview)
        self.uparrow_icon = PhotoImage(file='./assets/up-arrow.png')
        self.downarrow_icon = PhotoImage(file='./assets/down-arrow.png')

        self.uparrow = self.uparrow_icon.subsample(25)
        self.downarrow = self.downarrow_icon.subsample(25)

        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow)
        self.upbutton.grid(row=0, column=1, padx=(270, 5), pady=8)
        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow)
        self.downbutton.grid(row=0, column=3, pady=8)

        self.page_label = ttk.Label(self.bottom_frame, text='page')
        self.page_label.grid(row=0, column=4, padx=5)

        self.filemenu.add_command(label="Exit")
        self.filemenu.add_command(label="Exit", command=self.master.destroy)

def parse_arguments(args=None):
    parser = argparse.ArgumentParser(description="Open the PDF viewer")

    parser.add_argument(
        "file",
        type=str,
        nargs="?",
        default=None,
        help="input pdf file"
    )

    parser.add_argument(
        "-e",
        "--extract",
        type=str,
        help="extract a range of pages inclusive x-y"
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    # print(args.file)
    # print(args.extract)

    root = Tk()
    app = PDFViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
