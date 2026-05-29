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
        width = int(math.floor(self.width / 100.0) * 100)

    def get_metadata(self):
        metadata = self.pdf.metadata
        num_pages = self.pdf.page_count
        return metadata, num_pages

    def get_page(self, page_num: int, target_width: int | None = None, zoom_ratio: float | None = None):
        page = self.pdf.load_page(page_num)

        if target_width:
            zoom_ratio = target_width / page.rect.width

        mat = fitz.Matrix(zoom_ratio, zoom_ratio)
        pix = page.get_pixmap(matrix=mat)
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        img_data = px1.tobytes("ppm")

        return [PhotoImage(data=img_data), zoom_ratio]

    def get_text(self, page_num):
        page = self.pdf.load_page(page_num)
        text = page.get_text('text')
        return text

    def get_highlighted_text(self, page_num, zoom_ratio, start_x, start_y, end_x, end_y):
        page = self.pdf.load_page(page_num)

        x0, y0 = min(start_x, end_x), min(start_y, end_y)
        x1, y1 = max(start_x, end_x), max(start_y, end_y)

        pdf_x0 = x0 / zoom_ratio
        pdf_y0 = y0 / zoom_ratio
        pdf_x1 = x1 / zoom_ratio
        pdf_y1 = y1 / zoom_ratio

        rect = fitz.Rect(pdf_x0, pdf_y0, pdf_x1, pdf_y1)
        selected_text = page.get_text("text", clip=rect).strip()
        print(f"Extracted: {selected_text}")
