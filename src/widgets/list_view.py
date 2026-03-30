import tkinter as tk
from typing import List

class ListViewItem(tk.Frame):
    def __init__(self, parent: tk.Widget, data):
        super().__init__(parent)

    def update_(self, data):
        pass

class ListView(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        item_class: type[ListViewItem]
    ):
        super().__init__(parent)

        self.item_class = item_class

        self.items: List[ListViewItem] = []

        # ------
        # ---
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
        # ---
        self.inner = tk.Frame(self.canvas)
        self.canvas_wnd = self.canvas.create_window(0, 0, window=self.inner, anchor='nw')

        # ---
        self.canvas.bind(
            '<Configure>',
            lambda e: self.canvas.itemconfig(self.canvas_wnd, width=e.width)
        )

        self.canvas.bind_all(  # TODO: this is binding to ALL widgets not just children
            '<MouseWheel>',
            lambda e: self.canvas.yview_scroll(-1 * int((e.delta / 120)), 'units')
        )
        self.canvas.bind_all(  # TODO: above
            '<Button-4>',
            lambda _: self.canvas.yview_scroll(-1, 'units')
        )
        self.canvas.bind_all(  # TODO: above
            '<Button-5>',
            lambda e: self.canvas.yview_scroll(1, 'units')
        )

        self.inner.bind(
            '<Configure>',
            lambda e: self.canvas.config(scrollregion=self.canvas.bbox('all'))
        )

    def set_data(self, data):
        y_scroll_pos = self.canvas.yview()[0]

        for item in self.items: item.destroy()
        self.items.clear()


        for item_data in data:
            item = self.item_class(self.inner, item_data)
            item.pack(fill='x', padx=4, pady=2)
            self.items.append(item)

        self.update_idletasks()
        self.canvas.yview_moveto(y_scroll_pos)

    def update_data(self, data):
        if len(data) != len(self.items):
            print('[ERROR] Can\'t update data as lenghts don\'t match. Use "set_data" instead.')
            return
        
        for item, item_data in zip(self.items, data):
            item.update_(item_data)


