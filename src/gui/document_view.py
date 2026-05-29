from tkinter import *
from tkinter import ttk
import src.config as config

class DocumentView(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.current_image = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # HIGHLIGHTING
        self.start_x = None
        self.start_y = None
        self.rect_id = None

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
        self.output.bind("<ButtonPress-1>", self._on_press)
        self.output.bind("<B1-Motion>", self._on_drag)
        self.output.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.start_x = self.output.canvasx(event.x)
        self.start_y = self.output.canvasy(event.y)

        if self.rect_id:
            self.output.delete(self.rect_id)
            self.rect_id = None
        print(f"rect_id on press: {self.rect_id}")

    def _on_drag(self, event):
        self.curr_x = self.output.canvasx(event.x)
        self.curr_y = self.output.canvasy(event.y)

        print(f"rect_id on drag: {self.rect_id}")
        if self.rect_id:
            self.output.coords(self.rect_id, self.start_x, self.start_y, self.curr_x, self.curr_y)
        else:
            self.rect_id = self.output.create_rectangle(
                self.start_x, self.start_y, self.curr_x, self.curr_y,
                outline="blue", dash=(4, 4), width=2
            )

    def _on_release(self, event):
        end_x = self.output.canvasx(event.x)
        end_y = self.output.canvasy(event.y)
        self.controller.extract_highlighted_text(self.start_x, self.start_y, end_x, end_y)

    def _bound_to_mousewheel(self, event):
        self.output.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.output.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.output.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_canvas(self, img_file):
        self.output.delete('all')
        self.output.config(width=img_file.width(), height=img_file.height())
        self.output.create_image(0, 0, anchor='nw', image=img_file)

        self.current_image = img_file

        region = self.output.bbox("all")
        self.output.configure(scrollregion=region)
