import customtkinter as ctk
from tkinter import ttk
from PIL import Image
import time
from datetime import datetime, timedelta, date
import pygame
import threading
import json
import matplotlib.pyplot as plt

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
        
        #date and records
        self.current_date_obj = date.today()
        self.current_date_str = str(self.current_date_obj)
        self.records = self.load_records()
        if self.records == None:
            self.records = {}
        if self.current_date_str not in self.records.keys():
            self.records[self.current_date_str] = '00:00:00'
        
        #font
        self.font_big=ctk.CTkFont("Lato", 50, "bold")
        self.font_medium=ctk.CTkFont("Lato", 30)
        self.font_small=ctk.CTkFont("Lato", 20)
        
        #style for notebook
        style = ttk.Style()
        style.configure('TNotebook.Tab', background=FG_COLOR, foreground=TXT_COLOR, font=("Lato", 12))
        style.map('TNotebook.Tab', background=[('selected', TAB_COLOR)], relief=[('selected', 'flat')])
                
        #notebook
        self.notebook = ttk.Notebook(self.root)

        
        #main frame
        self.home_frame = ctk.CTkFrame(self.notebook, fg_color=BG_COLOR ,bg_color=FG_COLOR, corner_radius=0)
        
        #time focused today
        self.total_time_label = ctk.CTkLabel(self.home_frame, text_color=TXT_FADED, text='Total focused time: {}'.format(self.records[self.current_date_str]) , font=self.font_small)
        self.total_time_label.pack(pady=10)
        
        #time option
        self.time_option = ctk.CTkOptionMenu(self.home_frame, values=['25 minutes', '30 minutes', '45 minutes', '60 minutes'], command=self.optionmenu_callback, fg_color=FG_COLOR, dropdown_fg_color=BTN_COLOR, button_color=FG_COLOR, bg_color=BG_COLOR, button_hover_color="#9c2525")
        self.time_option.pack()
        self.time_choice = "00:25:00"
        
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
        
        #log screen
        self.log_frame = ctk.CTkFrame(self.notebook, fg_color=BG_COLOR)
        ctk.CTkLabel(self.log_frame, text="Time logs",font=self.font_medium, text_color=TXT_COLOR).pack(pady=10)
        self.log_scroll_frame = ctk.CTkScrollableFrame(self.log_frame, fg_color=FG_COLOR, corner_radius=20, scrollbar_button_color=BG_COLOR, scrollbar_button_hover_color=TXT_COLOR)
        self.log_scroll_frame.pack(fill="both", expand=True, pady=10, padx=20)
        for full_date, time in self.records.items():
            year = full_date[:4]
            month = full_date[5:7]
            day = full_date[8:]
            ctk.CTkLabel(self.log_scroll_frame, text=f"Date: {day}/{month}/{year}, time: {time[:2]} hours, {time[3:5]} minutes", font=self.font_small, text_color=TXT_COLOR).pack()
        # self.generate_line_graph(self.records)
        
        #stats screen
        # img = Image.open('line_graph.png')
        # img = ctk.CTkImage(img)
        # self.stats_frame = ctk.CTkFrame(self.notebook, fg_color=BG_COLOR)
        
        #notebook: add tabs
        self.notebook.add(self.home_frame, text="Timer")
        self.notebook.add(self.log_frame, text="Logs")
        # self.notebook.add(self.stats_frame, text="Stats")
        self.notebook.pack(fill="both", expand=True)
  
        #start the main loop
        self.root.mainloop()
        
    
    def reset_timer(self):
        if self.time_label.cget('text') != self.time_choice:
            self.time_label.configure(text=self.time_choice)
            
    
    def optionmenu_callback(self, choice):
        if str(choice[:2]) == "60":
            self.time_choice = str("01:00:00")
        else:
            self.time_choice = "00:"+ str(choice[:2]) + ":00"
        self.time_label.configure(text=self.time_choice)
              
            
    def start_timer(self):
        self.reset_timer()
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()
        
        
    def update_timer(self):
        self.start_btn.configure(state='disabled')
        time_str = self.time_choice

        while self.time_label.cget('text') != "00:00:00":
            #reading time from the label
            time_obj = datetime.strptime(time_str, "%H:%M:%S")
    
            #for testing purposes chnage to 0.001 of a second
            time.sleep(0.001)
            
            #calculating new time
            new_time_obj = time_obj - timedelta(seconds=1)
            new_time_str = new_time_obj.strftime("%H:%M:%S")
            
            #updating time on time label
            time_str = new_time_str
            time_obj = datetime.strptime(time_str, "%H:%M:%S")
            self.time_label.configure(text=time_str)
            self.time_label.update_idletasks()

        
        # unitialize pygame.mixed for audio
        pygame.mixer.init()
        pygame.mixer.music.load("assets/bell.wav")
        pygame.mixer.music.play()
        
        # update total time
        try:
            total_time_str = self.records[self.current_date_str]
        except KeyError or ValueError:
            total_time_str = "00:00:00"
        finally:
            total_time_obj = datetime.strptime(total_time_str, "%H:%M:%S")
            
        new_total_time_obj = total_time_obj + timedelta(hours=int(self.time_choice[:2]), minutes=int(self.time_choice[3:5]), seconds=int(self.time_choice[7:]))
        new_total_time_str = new_total_time_obj.strftime("%H:%M:%S")
        self.update_records(self.current_date_str, new_total_time_str)
        
        self.total_time_label.configure(text=f"Total focused time: {self.records[self.current_date_str]}")
        self.start_btn.configure(state='normal')
        
    
    def update_records(self, date, time):
        
        self.new_record = {date: time}
        
        if date in self.records.keys():
            self.records[date] = time
        else:
            self.records.update(self.new_record)
        
        try:
            with open('date_records.json', 'r') as file_read:
                time_records = json.loads(file_read)
                print(time_records)
        except:
            with open('date_records.json', 'w') as file_write:
                file_write.write("")       
        finally:
            with open('date_records.json', 'a') as file_write:
                json.dump(self.records, file_write, indent=4)

    def load_records(self):
        try:
            with open("date_records.json", 'r') as file:
                records = json.load(file)
                return records
        except Exception:
            print("No records found!")

        return None
    
    
    def generate_line_graph(self, data):
        
        current_month = self.current_date_obj.strftime("%B")

        # Convert the given times to minutes
        def time_to_minutes(time_str):
            h, m, s = map(int, time_str.split(':'))
            return h * 60 + m + s / 60

        # Create a dictionary to store the minutes for each day
        minutes_data = {date: time_to_minutes(time_str) for date, time_str in data.items()}

        # Prepare the data for plotting
        days_in_month = 31
        days = [f"2024-07-{str(day).zfill(2)}" for day in range(1, days_in_month + 1)]
        values = [minutes_data.get(day, 0) for day in days]

        # Extract day numbers for labeling
        labels = [f"{day}" for day in range(1, days_in_month + 1)]

        # Create the plot
        plt.figure(figsize=(12, 8))
        plt.plot(labels, values, marker='o', linestyle='-', color=BG_COLOR)

        # Set the x-axis labels to show every day of the month
        plt.xticks(rotation=90)
        plt.xlabel('Date')
        plt.ylabel('Time in minutes')
        plt.title(f'Focused time for {current_month} 2024')

        # Save the figure as an image
        plt.tight_layout()
        plt.savefig('line_graph.png')
            

if __name__ == "__main__":
    app = App()