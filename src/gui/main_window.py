from tkinter import *
from src.gui.top_bar import TopBar
from src.gui.document_view import DocumentView

class PDFViewerUI:
    def __init__(self, master, controller) -> None:
        self.master = master
        self.controller = controller

        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(width=True, height=True)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.top_bar = TopBar(self.master, self.controller)
        self.top_bar.pack(side="top", fill="x")

        self.doc_view = DocumentView(self.master, self.controller)
        self.doc_view.pack(side="top", fill="both", expand=True)

    def update_canvas(self, img_file, words) -> None:
        self.doc_view.update_canvas(img_file, words)

    def update_page_labels(self, current, total) -> None:
        self.top_bar.update_page_labels(current, total)

    def set_zoom_dropdown_text(self, text) -> None:
        self.top_bar.set_zoom_text(text)

    def get_scrollbar_width(self) -> int:
        return self.doc_view.scrolly.winfo_width()
