import Tkinter as tk
from ola.ClientWrapper import ClientWrapper
import time
import threading
import thread
import Queue
import olathread

class DisplayApp:
	
	def __init__(self, width, height):
		# Initialize the tk root window
		self.root = tk.Tk()
		self.initDx = width
		self.initDy = height
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )
		self.root.title("RDM user interface version: 1.0")
		self.root.maxsize( 1600, 900 )
		self.root.lift()
		self.root.update_idletasks()
		# Assigning fields
		self.curUID = tk.StringVar(self.root)
		self.curUID.set('Devices')
		self.uids = ['no items']
		self.cur_universe = tk.IntVar(self.root)
		self.cur_universe.set(1)
		self.universe_list = [1, 2, 3, 4, 5]
		self.state = 0
		self.device_menu = None
		# Call initialing functions
		self.buildFrames()
		self.buildCntrl()
		# Start the ola thread
		self.ola_thread = olathread.OLAThread()
		self.ola_thread.start()
		print 'currently in thread: %d' % threading.currentThread().ident
		time.sleep(1)
		print 'back from sleep'
		
	def buildFrames(self):
		'''
		'''
		self.cntrlframe = tk.PanedWindow(self.root)
		self.cntrlframe.pack(side=tk.TOP, padx=2, pady=2, fill=tk.Y)
		
	def buildCntrl(self):
		'''
		CHCHCH CHAAAAAANGES -David Bowie
		'''
		discover_button = tk.Button( self.cntrlframe, text="Discover", 
							   		 command=self.discover, width=8 )
		discover_button.grid(row=0, column=0)
		tk.Label( self.cntrlframe, width=3).grid(row=0, column=1)
		tk.Label(self.cntrlframe, text='Select\nUniverse:').grid(row=0, column=2)
		menu = tk.OptionMenu(self.cntrlframe, self.cur_universe, *self.universe_list)
		menu.config(width=1)
		menu.grid(row=0, column=3)
		self.initDeviceMenu(self.uids)
		tk.Label(self.cntrlframe, width=6, text='Identify').grid(row=0,column=5)
		tk.Checkbutton(self.cntrlframe).grid(row=0, column=6)
		tk.Label( self.cntrlframe, width=3).grid(row=0, column=7)
		tk.Label( self.cntrlframe, text='Automatic\nDiscovery' ).grid(row=0, column=8)
		tk.Checkbutton(self.cntrlframe).grid(row=0, column=9)
		
	def initDeviceMenu(self, list):
		if self.device_menu != None:
			self.device_menu.destroy()
		self.device_menu = tk.OptionMenu(self.cntrlframe, self.curUID, *list)
		self.device_menu.grid(row=0, column=4)

	def discover(self):
		func = lambda: self.ola_thread._client.RunRDMDiscovery(1, True, self.uponDiscover)
		self.ola_thread.Execute(func) 
	
	def uponDiscover(self, status, uids):
		print 'discovered'
		self.uids = uids
		self.curUID.set(self.uids[0]) # initial value
		self.initDeviceMenu(self.uids)
	
	def main(self):
		print 'Entering main loop'
		self.root.mainloop()	

if __name__ == '__main__':
	display = DisplayApp(600, 400)
	display.main()


	