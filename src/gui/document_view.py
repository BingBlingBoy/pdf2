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

        self.output.bind('<Enter>', self._bound_to_mousewheel)
        self.output.bind('<Leave>', self._unbound_to_mousewheel)

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
