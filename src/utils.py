from datetime import datetime, timedelta
import tkinter as tk

def final_dt_str(start: datetime, seconds_to_add: int):
    final = start + timedelta(seconds=seconds_to_add)
    return final.strftime('%H:%M:%S %d-%m-%Y')

def load_icon(path: str) -> tk.PhotoImage:
    return tk.PhotoImage(file=path)