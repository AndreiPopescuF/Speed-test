import tkinter as tk
import time
import threading
import random


class SpeedTest:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speed test")
        self.root.geometry("1280x800")

        self.texts = open("text.txt", "r").read().split("\n")

        self.frame = tk.Frame(self.root)

        # Create a label to display a random sample text
        self.sample_lable = tk.Label(self.frame,text = random.choice(self.texts),font=("Arial",18))
        self.sample_lable.grid(row=0,column=0,columnspan=2,padx=5,pady=10)
        
        # Create an entry widget for user input
        self.input_entry = tk.Entry(self.frame,width=40,font=("Arial",24))
        self.input_entry.grid(row=1,column=0,columnspan=2,padx=5,pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)

        # Create a label to display typing speed statistics
        self.speed_lable = tk.Label(self.frame,text = "Speed: \n0.00 Characters Per Second\n0.00 Characters Per Minute\n0.00 Words Per Second\n0.00 Words Per Minute",font=("Arial",18))
        self.speed_lable.grid(row=2,column=0,columnspan=2,padx=5,pady=10)

        # Create a button to reset the test
        self.reset_button = tk.Button(self.frame,text = "Reset", command=self.reset,font=("Arial",24),fg="red")
        self.reset_button.grid(row=3,column=0,columnspan=2,padx=5,pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False

        self.root.mainloop()

    def start(self,event):
        if not self.running:
            # Check if the typing test is not already running and start a new thread
            if not event.keycode in [16,17,18]: # Ignore Shift, Ctrl, and Alt keycodes
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        # Check if the entered text matches the sample text and change text color accordingly
        if not self.sample_lable.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        # Check if the entered text matches the sample text completely
        if self.input_entry.get() == self.sample_lable.cget('text'):
            # If matched, stop the test, change text color to green
            self.running = False
            self.input_entry.config(fg="green")

    # Method to calculate typing speed statistics
    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            # Calculate characters per second, characters per minute, words per second, and words per minute
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed_lable.config(text=f"Speed: \n{cps:.2f} Characters Per Second\n{cpm:.2f} Characters Per Minute\n{wps:.2f} Words Per Second\n{wpm:.2f} Words Per Minute")

    # Method to reset the typing speed test
    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_lable.config(text="Speed: \n0.00 Characters Per Second\n0.00 Characters Per Minute\n0.00 Words Per Second\n0.00 Words Per Minute")
        self.sample_lable.config(text=random.choice(self.texts))
        self.input_entry.delete(0,tk.END)


SpeedTest()

