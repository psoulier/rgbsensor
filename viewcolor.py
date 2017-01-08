import Tkinter as tk
import time
import rgbsensor

class App():
    def __init__(self):
        self.rgb = rgbsensor.RGBSensor()
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.update_clock()

        self.rgb.set_integration(0)
	self.rgb.set_gain_x60()
	self.rgb.led_off()
        self.root.mainloop()



    def update_clock(self):
        r,g,b,c = self.rgb.get_rgbc()
	print 'r=%d g=%d b=%d' % (r,g,b)

        color = '#%04x%04x%04x' % (r,g,b)
	print color
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.root.configure(bg=color)
        self.root.after(100, self.update_clock)

app=App()
