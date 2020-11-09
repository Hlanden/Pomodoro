import tkinter as tk
import time
import threading
from tkinter.messagebox import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.master.resizable(False, False)
        #self.master.bind('<Control-k>', lambda x: self.generate_plots())
        self.master.bind('<Return>', lambda x: self.start_countdown())
        self.master.attributes('-topmost', True)
        self.minutes = 25
        self.seconds = 0
        self.countThread = None
        self.isPause = True
        self.isRunning = True
        self.pauseCounter = 0

        self.create_widgets()

    def create_widgets(self):
        self.timerVar = tk.StringVar()
        self.timerVar.set('00:00')
        self.labelTimerStatus = tk.Label(self.master, font=('', 40, 'bold'), textvariable=self.timerVar, fg='red',
                                         width=5)

        self.labelTimerStatus.grid(column=1, row=5)

    def start_countdown(self):
        if self.countThread is None or not self.countThread.is_alive():
            self.countThread = threading.Thread(target=self.countdown, args=(), daemon=True)
            self.countThread.start()


    def countdown(self):
        while self.isRunning:
            self.timerVar.set('{:02d}:{:02d}'.format(self.minutes, self.seconds))
            if self.minutes or self.seconds:
                time.sleep(1)
                if self.seconds == 0:
                    self.minutes -= 1
                    self.seconds += 59
                else:
                    self.seconds -= 1
            else:
                if self.isPause:
                    self.isPause = False
                    showinfo('Pause', 'Take a short break! Relax :)')
                    self.pause()
                else:
                    self.isPause = True
                    showinfo('Get back to work...', 'Be effective, a break is not far away!')
                    self.reset_counter()

    def pause(self):
        self.labelTimerStatus.configure(foreground="green")
        if self.pauseCounter != 2:
            self.minutes = 5
            self.seconds = 0
        else:
            self.pauseCounter = 0
            self.minutes = 30
            self.seconds = 0
        self.pauseCounter += 1

    def reset_counter(self):
        self.labelTimerStatus.configure(foreground="red")
        self.minutes = 25
        self.seconds = 0

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()