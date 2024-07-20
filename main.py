import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image
import time
from datetime import datetime, timedelta
import pygame
import threading

# Color constants
FG_COLOR = "#d37b7b"
BG_COLOR = "#BA4949"
TAB_COLOR = "#BA4949"
TXT_COLOR = "#ffffff"
ENTRY_COLOR = "#ab4342"
BTN_TEXT = "#ab504f"
BTN_COLOR = "#ffffff"
BTN_HOVER = FG_COLOR
TXT_FADED ="#e3bdbc"

class App(ctk.CTk):
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('Pomodoro Timer')
        self.root.minsize(600, 400)
        self.root.resizable(False, False)
        
        self.timer_thread = None
        
        #font
        self.font_big=ctk.CTkFont("Lato", 40, "bold")
        self.font_small=ctk.CTkFont("Lato", 20)
        
        #style for notebook
        style = ttk.Style()
        style.configure('TNotebook.Tab', background=FG_COLOR, foreground="white")
        style.map('TNotebook.Tab', background=[('selected', TAB_COLOR)], relief=[('selected', 'flat')])
                
        # create notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        #main frame
        self.home_frame = ctk.CTkFrame(self.notebook, fg_color=BG_COLOR ,bg_color=FG_COLOR, corner_radius=0)
        self.notebook.add(self.home_frame, text="Timer")
        
        #time focused today
        self.total_time_label = ctk.CTkLabel(self.home_frame, text_color=TXT_FADED, text='Time focused today: 0 hours 0 minutes', font=self.font_small)
        self.total_time_label.pack(pady=10)
        
        #time frame
        self.time_frame = ctk.CTkFrame(self.home_frame, fg_color=FG_COLOR, bg_color=BG_COLOR, corner_radius=20, width=300)
        self.time_frame.pack(pady=20, ipadx=40, expand=True)
                
        #progress bar
        # self.progress_bar = ctk.CTkProgressBar(self.home_frame, height=20, width=400, progress_color="white")
        # self.progress_bar.pack(pady=20)
        
        #time label
        self.time_label = ctk.CTkLabel(self.time_frame, text_color=TXT_COLOR, text="25:00", font=self.font_big)
        self.time_label.place(relwidth=0.5, relheight=0.5, relx=0.25, rely=0.25)

        
        #buttons
        self.btn_frame = ctk.CTkFrame(self.home_frame, fg_color=BG_COLOR, bg_color=BG_COLOR)
        self.btn_frame.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(self.btn_frame, text="START", text_color=BTN_TEXT, hover_color=BTN_HOVER, fg_color=BTN_COLOR, command=self.start_timer)
        self.start_btn.pack(side="left", padx=30, ipady=5, ipadx=5)
        
        self.pause_btn = ctk.CTkButton(self.btn_frame, text="PAUSE", text_color=BTN_TEXT, hover_color=BTN_HOVER, fg_color=BTN_COLOR, command=self.pause_timer)
        self.pause_btn.pack(side="right", padx=30, ipady=5, ipadx=5)

        #task entry
        self.task_frame = ctk.CTkFrame(self.home_frame, fg_color=BG_COLOR, bg_color=BG_COLOR)
        self.task_frame.pack()

        self.task_entry = ctk.CTkEntry(self.task_frame, fg_color=FG_COLOR, bg_color=BG_COLOR, corner_radius=10, width=350, height=40, placeholder_text="Add task...", placeholder_text_color=TXT_FADED, text_color=TXT_COLOR, font=self.font_small)
        self.task_entry.pack(side="left", pady=10)
        
        #todo
        self.todo_frame = ctk.CTkFrame(self.notebook, fg_color=FG_COLOR, bg_color=BG_COLOR)
        self.notebook.add(self.todo_frame, text="TO-DOs")
        
        image = Image.open("assets/plus.png")
        image = ctk.CTkImage(image, size=(25, 25))
        
        
        self.task_button = ctk.CTkButton(self.task_frame, image=image, text="", fg_color=BG_COLOR, bg_color=BG_COLOR, hover_color=BTN_HOVER, corner_radius=6, width=25, height=25)
        self.task_button.pack(side="right", ipady=5, pady=10, padx=10)
        
        
        
        self.root.mainloop()
    
    def reset_timer(self):
        if self.time_label.cget('text') != "25:00":
            self.time_label.configure(text="25:00")
            time.sleep(1)    
        
    def start_timer(self):
        self.reset_timer()
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()
        
    def pause_timer(self):
        print("Pause was pressed!")
        pass
        
    def update_timer(self):
        time_str = self.time_label.cget('text')
        if time_str == "00:00":
            # unitialize pygame.mixed for audio
            pygame.mixer.init()
            pygame.mixer.music.load("assets/bell.wav")
            pygame.mixer.music.play()
            return
        time_obj = datetime.strptime(time_str, "%M:%S")
        
        #for now time updates every secound
        time.sleep(1)
        new_time_obj = time_obj - timedelta(minutes=1)
        new_time_str = new_time_obj.strftime("%M:%S")
        
        self.time_label.configure(text=new_time_str)
        self.time_label.update_idletasks()
        self.time_label.after(60, self.update_timer())
        

        

if __name__ == "__main__":
    app = App()