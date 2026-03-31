import time
import tkinter as tk
from tkinter import ttk

import pyperclip

from utils import load_icon

def fmt_elapsed(elapsed_ms: int) -> str:
    return f'{elapsed_ms // 60_000:02} : {(elapsed_ms % 60_000) // 1000:02} . {(elapsed_ms % 1000) // 10:02}'

class StopwatchTab(tk.Frame):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)

        self.is_running = False
        self.is_paused  = False
        self.is_lapping = False

        self.n_laps = 0

        self.time = 0
        self.last_lap_time = 0

        self.sw_tick_handle = ''

        self.init_icons()
        self.init_ui()

    def init_icons(self):
        self.ic_copy = load_icon('assets/icons/copy.png')

    def init_ui(self):
        # ---
        self.sw_lbl = tk.Label(self, text=fmt_elapsed(0), font=('TkDefaultFont', 16, 'bold'))
        self.sw_lbl.pack(side='top', expand=True)

        # ---
        lap_table_columns = ['lap', 'lap_time', 'overall_time']

        self.lap_table = ttk.Treeview(self, columns=lap_table_columns, show='headings')

        self.lap_table.heading('lap',          text='Lap')
        self.lap_table.heading('lap_time',     text='Lap Time')
        self.lap_table.heading('overall_time', text='Overall Time')

        # ---
        controls = tk.Frame(self)

        self.sec_btn  = tk.Button(controls, text='Lap'  , command=self.on_sec_btn_click , state='disabled')
        self.main_btn = tk.Button(controls, text='Start', command=self.on_main_btn_click)
        self.copy_btn = tk.Button(controls, image=self.ic_copy, command=self.on_copy_btn_click, state='disabled')  # TODO: height doesn't match with other buttons

        tk.Frame(controls).pack(side='left', expand=True, padx=1)
        self.sec_btn .pack(side='left', padx=2)
        self.main_btn.pack(side='left', padx=2)
        tk.Frame(controls).pack(side='left', expand=True, padx=1)
        self.copy_btn.pack(side='right', padx=4)

        controls.pack(side='bottom', pady=4, fill='x')

    def sw_tick(self):
        start = time.time()

        self.time += 10
        self.sw_lbl.config(text=fmt_elapsed(self.time))

        self.sw_tick_handle = self.after(10 - (int(start * 1000) % 10), self.sw_tick)

    def on_main_btn_click(self):
        if not self.is_running:   # start
            self.sec_btn .config(text='Lap', state='normal')
            self.main_btn.config(text='Stop')
            
            self.sw_tick()

            self.is_running = True
            self.is_paused  = False
            self.is_lapping = False

        elif not self.is_paused:  # stop
            self.sec_btn .config(text='Reset' )
            self.main_btn.config(text='Resume')

            self.is_paused = True

            self.after_cancel(self.sw_tick_handle)

        else:                     # resume
            self.sec_btn .config(text='Lap' )
            self.main_btn.config(text='Stop')

            self.is_paused = False

            self.sw_tick()
    
    def on_sec_btn_click(self):
        if not self.is_running: return

        if not self.is_paused:  # lap
            if not self.is_lapping:  # first lap
                self.lap_table.pack(side='top', expand=True)
                self.copy_btn.config(state='normal')

                self.is_lapping = True

            self.n_laps += 1

            self.lap_table.insert('', 'end', values=[
                f'{self.n_laps:02}',
                fmt_elapsed(self.time - self.last_lap_time).replace(' ', ''),
                fmt_elapsed(self.time).replace(' ', '')
            ])

            self.last_lap_time = self.time

        else:                   # reset
            self.sw_lbl  .config(text=fmt_elapsed(0))

            self.sec_btn .config(text='Lap', state='disabled')
            self.main_btn.config(text='Start')
            self.copy_btn.config(state='disabled')

            self.lap_table.delete(*self.lap_table.get_children())
            self.lap_table.pack_forget()
            
            self.after_cancel(self.sw_tick_handle)

            self.is_running = False
            self.is_paused  = False
            self.is_lapping = False

            self.n_laps = 0

            self.time = 0
            self.last_lap_time = 0

    def on_copy_btn_click(self):
        if not self.is_running: return
        if not self.is_lapping: return

        out_str = ''

        for _id in self.lap_table.get_children():
            _vals = self.lap_table.item(_id)['values']
            out_str += f'{_vals[0]}  {_vals[1]}  {_vals[2]}\n'

        pyperclip.copy(out_str)