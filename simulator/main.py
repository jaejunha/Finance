from tkinter import *

class Simulator:
	def __init__(self, master):
		self.master = master
		master.title("Simulator")

		self.label_hello = Label(master, text = "Hello World!")
		self.label_hello.pack()

if __name__ == "__main__":
	window = Tk()
	simulator = Simulator(window)
	window.mainloop()
