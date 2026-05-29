from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import src.config as config

class DocumentView(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.current_image = None

        self.current_cursor = "arrow"

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # HIGHLIGHTING
        self.base_pil_image = None
        self.current_image = None
        self.canvas_image_id = None

        self.word_boxes = []
        self.start_word_idx = None
        self.selected_words = []

        self._build_widgets()

    def _build_widgets(self):
        self.scrolly = Scrollbar(self, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky="ns")
        self.scrollx = Scrollbar(self, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky="we")

        self.output = Canvas(self, width=config.CANVAS_WIDTH, bg='#ECE8F3', highlightthickness=0, borderwidth=0)
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0, sticky='ns')

        self.scrolly.configure(command=self.output.yview)
        self.scrollx.configure(command=self.output.xview)

        # EVENTS
        self.output.bind('<Enter>', self._bound_to_mousewheel)
        self.output.bind('<Leave>', self._unbound_to_mousewheel)
        self.output.bind("<Motion>", self._on_hover)
        self.output.bind("<ButtonPress-1>", self._on_press)
        self.output.bind("<B1-Motion>", self._on_drag)
        self.output.bind("<ButtonRelease-1>", self._on_release)

    def _get_word_index_at(self, x, y):
        for i, word in enumerate(self.word_boxes):
            wx0, wy0, wx1, wy1 = word["coords"]

            # THE FIX: Guarantee Top-Left to Bottom-Right orientation
            x_min = min(wx0, wx1)
            x_max = max(wx0, wx1)
            y_min = min(wy0, wy1)
            y_max = max(wy0, wy1)

            # We also add a small buffer so the user doesn't have to be pixel-perfect
            if (y_min - 5) <= y <= (y_max + 5): 
                if (x_min - 2) <= x <= (x_max + 2):
                    return i
        return None

    def _on_hover(self, event):
        cur_x = self.output.canvasx(event.x)
        cur_y = self.output.canvasy(event.y)

        # self.output.delete("debug_mouse")
        # self.output.create_oval(cur_x-4, cur_y-4, cur_x+4, cur_y+4, fill="green", tags="debug_mouse")

        # Check if we are over text
        word_index = self._get_word_index_at(cur_x, cur_y)
        is_over_text = word_index is not None

        # Use 'hand2' (pointing finger) just for this test!
        desired_cursor = "hand2" if is_over_text else "arrow"
        if self.current_cursor != desired_cursor:

            if is_over_text:
                word_text = self.word_boxes[word_index]["text"]
                print(f"Hovering over: {word_text}") # <-- DIAGNOSTIC PRINT
            else:
                print("Left text area")              # <-- DIAGNOSTIC PRINT
            self.output.config(cursor=desired_cursor)

            self.current_cursor = desired_cursor
            self.output.update_idletasks()

    def _on_press(self, event):
        cur_x = self.output.canvasx(event.x)
        cur_y = self.output.canvasy(event.y)

        self.start_word_idx = self._get_word_index_at(cur_x, cur_y)

        # Reset image if clicking in empty space
        if self.start_word_idx is None:
            self.current_image = ImageTk.PhotoImage(self.base_pil_image)
            self.output.itemconfig(self.canvas_image_id, image=self.current_image)
            self.selected_words = []

    def _on_drag(self, event):
        if self.start_word_idx is None or not self.base_pil_image or self.canvas_image_id is None:
            return

        cur_x = self.output.canvasx(event.x)
        cur_y = self.output.canvasy(event.y)
        current_word_idx = self._get_word_index_at(cur_x, cur_y)

        if current_word_idx is None:
            return

        start_idx = min(self.start_word_idx, current_word_idx)
        end_idx = max(self.start_word_idx, current_word_idx)

        overlay = Image.new('RGBA', self.base_pil_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        selection_color = (0, 120, 215, 85)

        self.selected_words = []
        merged_lines = []
        current_box = None

        for i in range(start_idx, end_idx + 1):
            word = self.word_boxes[i]
            self.selected_words.append(word["text"])

            wx0, wy0, wx1, wy1 = word["coords"]

            x_min, x_max = min(wx0, wx1), max(wx0, wx1)
            y_min, y_max = min(wy0, wy1), max(wy0, wy1)

            if current_box is None:
                current_box = [x_min, y_min, x_max, y_max]
            else:
                word_center_y = (y_min + y_max) / 2

                if (current_box[1] - 5) <= word_center_y <= (current_box[3] + 5):
                    current_box[0] = min(current_box[0], x_min)
                    current_box[2] = max(current_box[2], x_max)
                    current_box[1] = min(current_box[1], y_min)
                    current_box[3] = max(current_box[3], y_max)
                else:
                    merged_lines.append(current_box)
                    current_box = [x_min, y_min, x_max, y_max]

        if current_box:
            merged_lines.append(current_box)

        for box in merged_lines:
            draw.rectangle(box, fill=selection_color)

        blended_image = Image.alpha_composite(self.base_pil_image, overlay)

        self.current_image = ImageTk.PhotoImage(blended_image)
        self.output.itemconfig(self.canvas_image_id, image=self.current_image)

        # for i in range(start_idx, end_idx + 1):
        #     word = self.word_boxes[i]
        #     draw.rectangle(word["coords"], fill=selection_color)
        #     self.selected_words.append(word["text"])
        #
        # blended_image = Image.alpha_composite(self.base_pil_image, overlay)
        #
        # self.current_image = ImageTk.PhotoImage(blended_image)
        # self.output.itemconfig(self.canvas_image_id, image=self.current_image)

    def _on_release(self, event):
        if self.selected_words:
            final_text = " ".join(self.selected_words)
            self.controller.extract_highlighted_text(final_text)

    def _bound_to_mousewheel(self, event):
        self.output.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.output.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.output.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_canvas(self, pil_image, words):
        self.output.delete('all')
        self.base_pil_image = pil_image
        self.word_boxes = words

        self.current_image = ImageTk.PhotoImage(self.base_pil_image)
        self.output.config(width=self.base_pil_image.width, height=self.base_pil_image.height)
        self.canvas_image_id = self.output.create_image(0, 0, anchor='nw', image=self.current_image)

        # for w in self.word_boxes:
        #     x0, y0, x1, y1 = w["coords"]
        #     self.output.create_rectangle(x0, y0, x1, y1, outline="red", width=1)

        region = self.output.bbox("all")
        self.output.configure(scrollregion=region)
