from datetime import datetime
import tkinter as tk
from tkinter import messagebox as mb
from typing import Optional

from just_playback import Playback
from plyer.facades import Notification

from utils import final_dt_str

class TimerTab(tk.Frame):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        
        self.mixer = Playback()

        self.hour_var = tk.IntVar()
        self.min_var = tk.IntVar(value=10)
        self.sec_var = tk.IntVar()

        self.cd_handle: Optional[str] = None
        self.cd_dur_remaining: int = 0

        self.init_ui()

    def init_ui(self):
        # time picker
        time_picker = tk.Frame(self)

        self.hour_spin = tk.Spinbox(time_picker, from_=0, to=99, textvariable=self.hour_var)
        self.min_spin =  tk.Spinbox(time_picker, from_=0, to=59, textvariable=self.min_var )
        self.sec_spin =  tk.Spinbox(time_picker, from_=0, to=59, textvariable=self.sec_var )

        self.hour_spin.pack(side='left', fill='x', expand=True)
        tk.Label(time_picker, text=':').pack(side='left')
        self.min_spin .pack(side='left', fill='x', expand=True)
        tk.Label(time_picker, text=':').pack(side='left')
        self.sec_spin .pack(side='left', fill='x', expand=True)

        time_picker.pack(side='top', fill='x')

        # countdown labels
        self.countdown_container = tk.Frame(self)
        
        self.countdown_dur_lbl = tk.Label(self.countdown_container)
        self.countdown_lbl     = tk.Label(self.countdown_container, font=('TkDefaultFont', 16, 'bold'))
        self.countdown_end_lbl = tk.Label(self.countdown_container)
        
        self.countdown_dur_lbl.pack(side='top', expand=True)
        self.countdown_lbl    .pack(side='top', expand=True)
        self.countdown_end_lbl.pack(side='top', expand=True)
 
        # controls
        controls = tk.Frame(self)

        self.start_btn = tk.Button(controls, text='Start' , command=self.on_start_btn_click)
        self.pause_btn = tk.Button(controls, text='Pause' , command=self.on_pause_btn_click, state='disabled')
        self.dlt_btn   = tk.Button(controls, text='Delete', command=self.on_dlt_btn_click  , state='disabled')

        self.start_btn.pack(side='left')
        self.pause_btn.pack(side='left')
        self.dlt_btn  .pack(side='left')

        controls.pack(side='bottom', fill='x')

    def countdown(self, count: int):
        self.cd_dur_remaining = count

        if count > 0:  # running
            self.countdown_lbl.config(text=f'{(count // 3600):02}:{((count % 3600) // 60):02}:{(count % 60):02}')

            self.cd_handle = self.after(1000, self.countdown, count - 1)

        else:          # finished
            self.mixer.load_file('assets/alarm.mp3')
            self.mixer.loop_at_end(True)
            self.mixer.play()
            self.after(5000, lambda: self.mixer.stop())

            Notification().notify(
                title='Timer done',
                message='Your timer of <unknown> duration has finished.',
                app_name='Clock',
                timeout=10
            )

            self.hour_spin.config(state='normal')
            self.min_spin .config(state='normal')
            self.sec_spin .config(state='normal')
            self.start_btn.config(state='normal')
            self.pause_btn.config(state='disabled')
            self.dlt_btn  .config(state='disabled')
            self.countdown_container.pack_forget()

            self.cd_handle = None

    def on_start_btn_click(self):
        duration = self.hour_var.get() * 3600 + self.min_var.get() * 60 + self.sec_var.get()

        if duration == 0:
            mb.showinfo('Note', 'Can\'t start a timer with no duraiton.')            
        
        self.hour_spin.config(state='disabled')
        self.min_spin .config(state='disabled')
        self.sec_spin .config(state='disabled')
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        self.dlt_btn  .config(state='normal')
        self.countdown_container.pack(side='top', fill='x', expand=True)

        # self.countdown_dur_lbl.config(text=f'{(duration // 3600):02}:{((duration % 3600) // 60):02}:{(duration % 60):02}')
        self.countdown_end_lbl.config(text=final_dt_str(datetime.now(), duration))
         
        self.countdown(duration)

    def on_pause_btn_click(self):
        if self.cd_handle is not None:     # pause
            self.pause_btn.config(text='Resume')

            self.after_cancel(self.cd_handle)
            self.cd_handle = None
        
        elif self.cd_dur_remaining != 0:  # resume
            self.pause_btn.config(text='Pause')

            self.countdown_end_lbl.config(text=final_dt_str(datetime.now(), self.cd_dur_remaining))
            
            self.countdown(self.cd_dur_remaining)

    def on_dlt_btn_click(self):
        if self.cd_handle is not None:
            self.after_cancel(self.cd_handle)

        self.hour_spin.config(state='normal')
        self.min_spin .config(state='normal')
        self.sec_spin .config(state='normal')
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text='Pause')
        self.dlt_btn  .config(state='disabled')
        self.countdown_container.pack_forget()

        self.cd_handle = None
        self.countdown_remaining = 0
