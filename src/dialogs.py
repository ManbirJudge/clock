import tkinter as tk
from tkinter import ttk
from typing import List

def ask_select(
    parent: tk.Widget,
    title: str,
    prompt: str,
    options: List[str]
) -> str | None:
    did_select = False
    
    top = tk.Toplevel(parent)

    top.title(title)
    top.geometry('300x100')
    top.resizable(False, False)
    top.grab_set()

    tk.Label(top, text=prompt, anchor='w').pack(side='top', fill='x', padx=4, pady=4)

    def on_change(*_):
        nonlocal did_select
        did_select = True

    var = tk.StringVar(top)
    var.trace_add('write', on_change)

    combo = ttk.Combobox(top, textvariable=var, values=options, state='readonly')
    combo.pack(side='top', fill='x', padx=4)

    tk.Frame(top).pack(side='top', expand=True)

    def on_cancel():
        nonlocal did_select
        did_select = False
        top.destroy()

    tk.Button(top, text='Ok', command=lambda: top.destroy()).pack(side='right', padx=4, pady=4)
    tk.Button(top, text='Cancel', command=on_cancel).pack(side='right', pady=4)

    parent.wait_window(top)

    return var.get() if did_select else None