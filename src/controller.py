import os
from tkinter import filedialog as fd
import src.config as config 
from src.miner import PDFMiner
from src.gui.main_window import PDFViewerUI

class AppController:
    def __init__(self, root, initial_file=None):
        self.root = root

        # State Variables
        self.path = None
        self.fileisopen = False
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None

        self.zoom_ratio = 1
        self.default_page_zoom = None
        self.miner = None

        self.view = PDFViewerUI(self.root, self)

        if initial_file:
            self.load_pdf(initial_file)

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
            self.root.title(f"PDF Viewer - {self.name}")
            self.display_page()

    def decimal_to_percentage(self, zoom_ratio: float):
        return f"{int(zoom_ratio * 100)} %"

    def display_page(self, zoom_ratio: float | None = None) -> None:
        if self.miner is None:
            return

        if self.numPages is not None and 0 <= self.current_page < self.numPages:
            if zoom_ratio:
                self.zoom_ratio = round(zoom_ratio, 1)
                if self.zoom_ratio < 0.1:
                    self.zoom_ratio = 0.1

            self.root.update_idletasks()

            target_width = (self.root.winfo_width() - self.view.get_scrollbar_width()) / 2
            if target_width <= 50:
                target_width = config.CANVAS_WIDTH

            if not zoom_ratio:
                self.view.set_zoom_dropdown_text("Automatic Zoom")
                img_file, self.zoom_ratio, words = self.miner.get_page(
                    self.current_page, target_width=target_width
                )
                self.default_page_zoom = self.zoom_ratio
            else:
                self.view.set_zoom_dropdown_text(self.decimal_to_percentage(self.zoom_ratio))
                img_file, self.zoom_ratio, words = self.miner.get_page(
                    self.current_page, zoom_ratio=self.zoom_ratio
                )

            # Update the View
            self.view.update_canvas(img_file, words)
            self.view.update_page_labels(self.current_page + 1, self.numPages)

    def extract_highlighted_text(self, text: str) -> None:
        if not text:
            return
        print(f"Extracted: {text}")

    def next_page(self) -> None:
        if self.fileisopen:
            if self.numPages is not None and self.current_page < self.numPages - 1:
                self.current_page += 1
                self.display_page(zoom_ratio=self.zoom_ratio)

    def previous_page(self) -> None:
        if self.fileisopen:
            if self.current_page > 0:
                self.current_page -= 1
                self.display_page(zoom_ratio=self.zoom_ratio)

    def on_zoom_select(self, ev):
        selected_value = ev.widget.get()
        self.display_page(zoom_ratio=config.ZOOM_DICT[selected_value])

    def zoom_in(self):
        self.display_page(self.zoom_ratio + 0.2)

    def zoom_out(self):
        self.display_page(self.zoom_ratio - 0.2)
