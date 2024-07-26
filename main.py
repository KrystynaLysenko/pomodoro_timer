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
        self.font_big=ctk.CTkFont("Lato", 50, "bold")
        self.font_small=ctk.CTkFont("Lato", 20)
        
        #style for notebook
        style = ttk.Style()
        style.configure('TNotebook.Tab', background=FG_COLOR, foreground="white", font=("Lato", 12))
        style.map('TNotebook.Tab', background=[('selected', TAB_COLOR)], relief=[('selected', 'flat')])
                

        #main frame
        self.home_frame = ctk.CTkFrame(self.root, fg_color=BG_COLOR ,bg_color=FG_COLOR, corner_radius=0)
        self.home_frame.pack(fill='both', expand=True)
        
        #time focused today
        self.total_time_label = ctk.CTkLabel(self.home_frame, text_color=TXT_FADED, text='Total focused time: 00:00:00' , font=self.font_small)
        self.total_time_label.pack(pady=10)
        
        #time option
        self.time_option = ctk.CTkOptionMenu(self.home_frame, values=['25 minutes', '30 minutes', '60 minutes'], command=self.optionmenu_callback, fg_color=FG_COLOR, dropdown_fg_color=BTN_COLOR, button_color=FG_COLOR, bg_color=BG_COLOR, button_hover_color="#9c2525")
        self.time_option.pack()
        self.time_choice = "25:00"
        
        #time frame
        self.time_frame = ctk.CTkFrame(self.home_frame, fg_color=FG_COLOR, bg_color=BG_COLOR, corner_radius=20, width=300)
        self.time_frame.pack(pady=20, ipadx=60, expand=True)

        
        #time label
        self.time_label = ctk.CTkLabel(self.time_frame, text_color=TXT_COLOR, text=self.time_choice, font=self.font_big)
        self.time_label.place(relwidth=0.5, relheight=0.5, relx=0.25, rely=0.25)
        
        #buttons
        self.btn_frame = ctk.CTkFrame(self.home_frame, fg_color=BG_COLOR, bg_color=BG_COLOR)
        self.btn_frame.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(self.btn_frame, text="START", text_color=BTN_TEXT, hover_color=BTN_HOVER, fg_color=BTN_COLOR, command=self.start_timer)
        self.start_btn.pack(side="left", padx=30, pady=20, ipady=5, ipadx=5)
  
        #start the main loop
        self.root.mainloop()
        
    
    def reset_timer(self):
        if self.time_label.cget('text') != self.time_choice:
            self.time_label.configure(text=self.time_choice)
            
    
    def optionmenu_callback(self, choice):
        self.time_choice = str(choice[:2])+':00'
        self.time_label.configure(text=self.time_choice)
              
            
    def start_timer(self):
        self.reset_timer()
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()
        
        
    def update_timer(self):
        self.start_btn.configure(state='disabled')
        while self.time_label.cget('text') != "00:00":
            time_str = self.time_label.cget('text')
            if time_str == "60:00":
                time_obj = datetime.strptime("1:00:00", "%H:%M:%S")
            else:
                time_obj = datetime.strptime(time_str, "%M:%S")
    
            #for testing purposes chnage to 0.001 of a second
            time.sleep(0.001)
            new_time_obj = time_obj - timedelta(seconds=1)
            new_time_str = new_time_obj.strftime("%M:%S")
            self.time_label.configure(text=new_time_str)
            self.time_label.update_idletasks()

        # unitialize pygame.mixed for audio
        pygame.mixer.init()
        pygame.mixer.music.load("assets/bell.wav")
        pygame.mixer.music.play()
        
        #update total time
        total_time_str = self.total_time_label.cget('text')[21:]
        total_time_obj = datetime.strptime(total_time_str, "%H:%M:%S")
        new_total_time_obj = total_time_obj + timedelta(minutes=int(self.time_choice[:2]))
        new_total_time_str = new_total_time_obj.strftime("%H:%M:%S")
        self.total_time_label.configure(text=f"Total focused time: {new_total_time_str}")
        self.start_btn.configure(state='normal')
        return


        

if __name__ == "__main__":
    app = App()