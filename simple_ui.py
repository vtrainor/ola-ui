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
    self.cur_universe = tk.IntVar(self.root)
    self.cur_universe.set(1)
    self.universe_list = [1, 2, 3, 4, 5]
    self.cur_device = None
    self.state = 0
    self._uid_dict = {}
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
    '''
    function = lambda : self.ola_thread.RunDiscovery(self.cur_universe.get(), self.uponDiscover)
    discover_button = tk.Button( self.cntrlframe, text="Discover", 
                     command=function,  width=8 )
    discover_button.grid(row=0, column=0)
    tk.Label( self.cntrlframe, width=3).grid(row=0, column=1)
    tk.Label(self.cntrlframe, text='Select\nUniverse:').grid(row=0, column=2)
    menu = tk.OptionMenu(self.cntrlframe, self.cur_universe, *self.universe_list)
    menu.config(width=1)
    menu.grid(row=0, column=3)
    tk.Label(self.cntrlframe, width=6, text='Identify').grid(row=0,column=5)
    tk.Checkbutton(self.cntrlframe).grid(row=0, column=6)
    tk.Label( self.cntrlframe, width=3).grid(row=0, column=7)
    tk.Label( self.cntrlframe, text='Automatic\nDiscovery' ).grid(row=0, column=8)
    tk.Checkbutton(self.cntrlframe).grid(row=0, column=9)
    self.device_menu = tk.OptionMenu(self.cntrlframe, self.cur_device, [])
    self.device_menu.grid(row=0, column=4)

  def discover(self):
    func = lambda: self.ola_thread._client.RunRDMDiscovery(1, True, self.uponDiscover)
    self.ola_thread.Execute(func) 
  
  def uponDiscover(self, status, uids):
    '''
    callback for client.RunRDMDiscovery
    '''
    print 'discovered'
    for uid in uids:
      self._uid_dict[uid] = {}
      self.ola_thread.RDMGet(self.cur_universe.get(), uid, 0, 0x0082, lambda x: self.addDevice(uid, x))
#       self.device_menu['menu'].insert('end', lambda : self.display_info(uid), self._uid_dict[uid.__str__()]['device label'])
    self.cur_device = self._uid_dict[uids[0]] # initial value
    
  def addDevice(self, uid, response ):
    '''
    adds device name to self.devicenames
    '''
    print 'add device'
    self._uid_dict[uid] = {'device label': response.ResponseCodeAsString()} 
        
  def display_info(self, uid):
  	print 'display info'

  def main(self):
    print 'Entering main loop'
    self.root.mainloop()  

if __name__ == '__main__':
  display = DisplayApp(600, 400)
  display.main()


  