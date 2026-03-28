#!/bin/python

from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk

from just_playback import Playback
from plyer import notification

def final_dt_str(start, seconds_to_add):
    final = start + timedelta(seconds=seconds_to_add)
    return final.strftime('%H:%M:%S %d-%m-%Y')

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        current_dpi = self.winfo_fpixels('1i')
        scaling_factor = current_dpi / 72
        print(current_dpi, scaling_factor)
        self.tk.call('tk', 'scaling', scaling_factor)

        self.title('Clock')
        self.geometry('500x400')
        self.resizable(True, True)

        self.hour_var = tk.IntVar()
        self.min_var = tk.IntVar(value=10)
        self.sec_var = tk.IntVar()
        self.timer_countdown_handle = None
        self.timer_countdown_remaining = 0

        self.mixer = Playback()

        self.init_ui()

    def init_ui(self):
        # --- tabs
        tabs = ttk.Notebook(self)

        alarm_tab = tk.Frame(tabs)
        world_clock_tab = tk.Frame(tabs)
        stopwatch_tab = tk.Frame(tabs)
        timer_tab = tk.Frame(tabs)

        tabs.add(alarm_tab, text='Alarm')
        tabs.add(world_clock_tab, text='World Clock')
        tabs.add(stopwatch_tab, text='Stopwatch')
        tabs.add(timer_tab, text='Timer')

        tabs.pack(expand=True, fill='both')

        # --- timer
        # time picker
        time_picker = tk.Frame(timer_tab)

        self.hour_spin = tk.Spinbox(time_picker, from_=0, to_=99, textvariable=self.hour_var)
        self.min_spin =  tk.Spinbox(time_picker, from_=0, to_=59, textvariable=self.min_var )
        self.sec_spin =  tk.Spinbox(time_picker, from_=0, to_=59, textvariable=self.sec_var )

        self.hour_spin.pack(side='left', fill='x', expand=True)
        tk.Label(time_picker, text=':').pack(side='left')
        self.min_spin.pack(side='left', fill='x', expand=True)
        tk.Label(time_picker, text=':').pack(side='left')
        self.sec_spin.pack(side='left', fill='x', expand=True)

        time_picker.pack(side='top', fill='x')

        # countdown labels
        self.countdown_container = tk.Frame(timer_tab)
        
        self.countdown_dur_lbl = tk.Label(
            self.countdown_container,
            text='Duration'
        )
        self.countdown_lbl = tk.Label(
            self.countdown_container,
            text='If you are seeing this, something isn\'t right',
            font=('TkDefaultFont', 16, 'bold')
        )
        self.countdown_end_lbl = tk.Label(
            self.countdown_container,
            text='Ends at'
        )
        
        self.countdown_dur_lbl.pack(side='top', expand=True)
        self.countdown_lbl.pack(side='top', expand=True)
        self.countdown_end_lbl.pack(side='top', expand=True)
 
        # controls
        controls = tk.Frame(timer_tab)

        self.start_btn = tk.Button(controls, text='Start' , command=self.on_timer_start_btn_click)
        self.pause_btn = tk.Button(controls, text='Pause' , command=self.on_timer_pause_btn_click, state='disabled')
        self.dlt_btn   = tk.Button(controls, text='Delete', command=self.on_timer_dlt_btn_click  , state='disabled')

        self.start_btn.pack(side='left')
        self.pause_btn.pack(side='left')
        self.dlt_btn  .pack(side='left')

        controls.pack(side='bottom', fill='x')

    def countdown(self, count):
        self.timer_countdown_remaining = count
        if count > 0:
            self.timer_countdown_handle = self.after(1000, self.countdown, count - 1)
            
            countdown_txt = f'{(count // 3600):02}:{((count % 3600) // 60):02}:{(count % 60):02}'
            self.countdown_lbl.config(text=countdown_txt)
        else:
            self.mixer.load_file('assets/alarm.mp3')
            self.mixer.loop_at_end(True)
            self.mixer.play()
            self.after(5000, lambda: self.mixer.stop())

            notification.notify(
                title='Timer done',
                message='Your timer of <unknown> duration has finished.',
                app_name='Clock',
                timeout=10
            )

            self.start_btn.config(state='normal')
            self.pause_btn.config(state='disabled')
            self.dlt_btn  .config(state='disabled')

            self.hour_spin.config(state='normal')
            self.min_spin .config(state='normal')
            self.sec_spin .config(state='normal')

            self.countdown_container.pack_forget()
            self.timer_countdown_handle = None

    def on_timer_start_btn_click(self):
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        self.dlt_btn  .config(state='normal')

        self.hour_spin.config(state='disabled')
        self.min_spin .config(state='disabled')
        self.sec_spin .config(state='disabled')
        
        duration = self.hour_var.get() * 3600 + self.min_var.get() * 60 + self.sec_var.get()

        countdown_txt = f'{(duration // 3600):02}:{((duration % 3600) // 60):02}:{(duration % 60):02}'
        self.countdown_dur_lbl.config(text=countdown_txt)

        self.countdown_end_lbl.config(text=final_dt_str(datetime.now(), duration))

        if duration == 0:
            mb.showinfo('Note', 'Can\'t start a timer with no duraiton.')            
        
        self.countdown_container.pack(side='top', fill='x', expand=True)
         
        self.countdown(duration)

    def on_timer_pause_btn_click(self):
        if self.timer_countdown_handle is not None:
            self.after_cancel(self.timer_countdown_handle)
            self.timer_countdown_handle = None

            self.pause_btn.config(text='Resume')
        
        elif self.timer_countdown_remaining != -1:
            self.countdown_end_lbl.config(text=final_dt_str(datetime.now(), self.timer_countdown_remaining))
             
            self.countdown(self.timer_countdown_remaining)

            self.pause_btn.config(text='Pause')

    def on_timer_dlt_btn_click(self):
        if self.timer_countdown_handle is not None:
            self.after_cancel(self.timer_countdown_handle)
        
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text='Pause')
        self.dlt_btn  .config(state='disabled')

        self.hour_spin.config(state='normal')
        self.min_spin .config(state='normal')
        self.sec_spin .config(state='normal')

        self.countdown_container.pack_forget()

        self.timer_countdown_handle = None
        self.timer_countdown_remaingin = 0

if __name__ == '__main__':
    wnd = MainWindow()
    wnd.mainloop()
