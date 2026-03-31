import tkinter as tk
from tkinter import ttk
 
from tabs import StopwatchTab, TimerTab, WorldClockTab

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # current_dpi = self.winfo_fpixels('1i')
        # scaling_factor = current_dpi / 72
        # self.tk.call('tk', 'scaling', scaling_factor)

        self.title('Clock')
        self.geometry('500x400')
        self.resizable(True, True)

        self.init_ui()

    def init_ui(self):
        # --- tabs
        tabs = ttk.Notebook(self)

        alarm_tab = tk.Frame(tabs)
        world_clock_tab = WorldClockTab(tabs)
        stopwatch_tab = StopwatchTab(tabs)
        timer_tab = TimerTab(tabs) 

        tabs.add(alarm_tab, text='Alarm')
        tabs.add(world_clock_tab, text='World Clock')
        tabs.add(stopwatch_tab, text='Stopwatch')
        tabs.add(timer_tab, text='Timer')

        tabs.pack(expand=True, fill='both')

        tabs.select(2)

if __name__ == '__main__':
    wnd = MainWindow()
    wnd.mainloop()