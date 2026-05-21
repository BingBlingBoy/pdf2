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
        self.current_page = None
        self.numPages = None

        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('1080x520+440+180')
        self.master.resizable(width = 0, height = 0)
        # self.master.iconbitmap(self.master, 'pdf_file_icon.ico')

        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File")
        self.filemenu.add_command(label="Exit")

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
