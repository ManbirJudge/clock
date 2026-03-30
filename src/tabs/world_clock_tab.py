from datetime import datetime
from pathlib import Path
import time
import tkinter as tk
from typing import List
from zoneinfo import ZoneInfo, available_timezones

from dialogs import ask_select
from widgets.list_view import ListView, ListViewItem
from utils import load_icon

def get_tz_time(tz_name: str, fmt: str = '%H:%M:%S') -> str:
    if tz_name.lower() == '__local__':
        return datetime.now().astimezone().strftime(fmt)
    return datetime.now(ZoneInfo(tz_name)).strftime(fmt)

def get_rel_offset_str(tz_name: str) -> str:  # TODO: rename vars
    now = datetime.now()

    local_offset = now.astimezone().utcoffset().total_seconds()
    target_offset = now.astimezone(ZoneInfo(tz_name)).utcoffset().total_seconds()

    diff_seconds = int(target_offset - local_offset)
    if diff_seconds == 0:
        return 'Same as local'

    abs_diff = abs(diff_seconds)
    
    hours = abs_diff // 3600
    minutes = (abs_diff % 3600) // 60
    direction = 'ahead' if diff_seconds > 0 else 'behind'

    parts = []
    if hours > 0:
        parts.append(f'{hours} {'hr' if hours == 1 else 'hrs'}')
    if minutes > 0:
        parts.append(f'{minutes} {'min' if minutes == 1 else 'mins'}')
    
    return f'{' '.join(parts)} {direction}'

class ClockListItem(ListViewItem):
    def __init__(self, parent: tk.Widget, data):
        super().__init__(parent, data)

        self.config(border=1, relief='ridge')

        left = tk.Frame(self)

        self.tz_lbl  = tk.Label(left, anchor='w', font=('TkDefaultFont', 14), text=data['name'])
        self.off_lbl = tk.Label(left, anchor='w', text=data['off-str'])

        self.tz_lbl .pack(side='top', fill='x')
        self.off_lbl.pack(side='top', fill='x')
        tk.Frame(left).pack(side='top', expand=True)

        left.pack(side='left', padx=4)

        tk.Frame(self).pack(side='left', expand=True)

        self.time_lbl = tk.Label(self, text=data['time'], font=('TkDefaultFont', 16))
        self.time_lbl.pack(side='right', padx=12)

    def update_(self, data):
        self.time_lbl.config(text=data['time'])

class WorldClockTab(tk.Frame):
    tz_cfg_file_path = Path.home() / '.config' / 'jclock' / 'tracked-timezones'
    
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        
        self.all_timezones = sorted(available_timezones())
        self.tracked_timezones: List[str] = []

        self.init_icons()
        self.init_ui()

        self.load_timezones()

        self.sync_and_start()

    def init_icons(self):
        self.ic_plus = load_icon('assets/icons/plus.png')
        self.ic_dots_vertical = load_icon('assets/icons/dots-vertical.png')

    def init_ui(self):
        top_frame = tk.Frame(self)

        self.local_time_lbl = tk.Label(top_frame, text='--:--:--', font=('TkDefaultFont', 16, 'bold'))
        
        controls = tk.Frame(top_frame)

        tk.Button(
            controls,
            image=self.ic_plus,
            command=self.on_add_btn_click
        ).pack(side='top')
        tk.Button(
            controls,
            image=self.ic_dots_vertical,
            command=self.on_more_btn_click
        ).pack(side='top')

        self.local_time_lbl.pack(side='left', expand=True)
        controls.pack(side='right')

        top_frame.pack(side='top', fill='x')

        self.clocks_list = ListView(self, ClockListItem)
        self.clocks_list.pack(side='top', fill='both', expand=True)

    def load_timezones(self):
        if self.tz_cfg_file_path.exists():
            with self.tz_cfg_file_path.open('r') as tz_cfg_f:
                for tz in tz_cfg_f:
                    tz = tz.strip()
                    if tz in self.all_timezones:
                        self.tracked_timezones.append(tz)
        
        self.store_timezones()

        self.clocks_list.set_data([
            {
                'name': tz,
                'off-str': get_rel_offset_str(tz),
                'time': get_tz_time(tz, '%H:%M')
            } for tz in self.tracked_timezones
        ])

    def store_timezones(self):
        try: 
            self.tz_cfg_file_path.parent.mkdir(exist_ok=True, parents=True)
            with self.tz_cfg_file_path.open('w') as tz_cfg_f:
                tz_cfg_f.write('\n'.join(self.tracked_timezones) + '\n')

        except Exception as e:
            print(f'[ERROR] Failed to store timezones to config file:\n\t{e}')

    def sync_and_start(self):  # NOTE: we are't syncing bcz logic is embedded in each individual loop
        # now = time.time()

        # self.after(1000 - (int(now * 1000) % 1000)  , self.update_1)
        # self.after(60_000 - (int(now * 1000) % 1000), self.update_2)

        self.update_1()
        self.update_2()

    def update_1(self):
        start = time.time()

        self.local_time_lbl.config(text=get_tz_time('__local__'))  # TODO: get from system
        
        ms_to_wait = 1000 - (int(start * 1000) % 1000)
        self.after(ms_to_wait, self.update_1)

    def update_2(self):
        start = time.time()

        self.clocks_list.update_data([
            {
                'time': get_tz_time(tz, '%H:%M')
            } for tz in self.tracked_timezones
        ])
        
        ms_to_wait = 60_000 - (int(start * 1000) % 60_000)
        self.after(ms_to_wait, self.update_2)

    def on_add_btn_click(self):
        new_tz = ask_select(self, 'Select timezone', 'List of available timezones:', self.all_timezones)
        if new_tz is not None:
            if new_tz not in self.tracked_timezones:
                self.tracked_timezones.append(new_tz)
        
                self.store_timezones()

                self.clocks_list.set_data([
                    {
                        'name': tz,
                        'off-str': get_rel_offset_str(tz),
                        'time': get_tz_time(tz, '%H:%M')
                    } for tz in self.tracked_timezones
                ])
    
    def on_more_btn_click(self):
        print('H1')