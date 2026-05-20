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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str,
                        help="input pdf file")
    parser.add_argument("-e", "--extract", type=str,
                        help="extract a range of pages inclusive x-y")
    args = parser.parse_args()
    print(args.file)
    print(args.extract)

    root = Tk()
    app = PDFViewer(root)
    root.mainloop()

if __name__ == '__main__':
    main()
