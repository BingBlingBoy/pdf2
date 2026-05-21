import math
import fitz
from tkinter import PhotoImage

class PDFMiner:
    def __init__(self, filepath) -> None:
        self.filepath = filepath
        self.pdf = fitz.open(self.filepath)
        self.first_page = self.pdf.load_page(0)
        self.width, self.height = self.first_page.rect.width, self.first_page.rect.height

        # Zoom values depneding on the pdf width
        zoom_dict = {800:0.8, 700:0.6, 600:1.0, 500:1.0}
        width = int(math.floor(self.width / 100.0) * 100)
        self.zoom = zoom_dict[width]

    def get_metadata(self):
        metadata = self.pdf.metadata
        num_pages = self.pdf.page_count
        return metadata, num_pages

    def get_page(self, page_num) -> PhotoImage:
        page = self.pdf.load_page(page_num)

        if self.zoom:
            # Creates a Matrix where the zoom factor is self.zoom
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat)
        else:
            pix = page.get_pixmap()

        # Variable that holds a transparent image
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        img_data = px1.tobytes("ppm")
        return PhotoImage(data=img_data)

    def get_text(self, page_num):
        page = self.pdf.load_page(page_num)
        text = page.get_text('text')
        return text
