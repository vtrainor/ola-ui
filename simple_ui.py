import Tkinter as tk
from ola.ClientWrapper import ClientWrapper
import time
import threading
import thread
import Queue
import olathread

class DisplayApp:
  
  def __init__(self, width, height):
    '''
    '''
    # Initialize the tk root window
    self.root = tk.Tk()
    self.init_dx = width
    self.init_dy = height
    self.root.geometry( "%dx%d+50+30" % (self.init_dx, self.init_dy) )
    self.root.title("RDM user interface version: 1.0")
    self.root.maxsize( 1600, 900 )
    self.root.lift()
    self.root.update_idletasks()
    # Assigning fields
    self.universe = tk.IntVar(self.root)
    self.universe.set(1)
    self.universe_list = [1, 2, 3, 4, 5]
    self.cur_uid = None
    self.id_state = tk.IntVar(self.root)
    self.id_state.set(0)
#     self.state = 0
    self._uid_dict = {}
    # Call initialing functions
    self.ola_thread = olathread.OLAThread()
    self.ola_thread.start()
    self.build_frames()
    self.build_cntrl()
    # Start the ola thread

    print 'currently in thread: %d' % threading.currentThread().ident
    time.sleep(1)
    print 'back from sleep'
    
  def build_frames(self):
    '''
    '''
    self.cntrl_frame = tk.PanedWindow(self.root)
    self.cntrl_frame.pack(side=tk.TOP, padx=1, pady=1, fill=tk.Y)
    self.info_frame = tk.PanedWindow(self.root)
    self.info_frame.pack(side=tk.TOP, padx=1, pady=2, fill=tk.Y)
    
  def build_cntrl(self):
    '''
    builds the top bar of the GUI where the options for the information display are
    located
    '''
    tk.Label( self.cntrl_frame, text='Select\nUniverse:').pack(side = tk.LEFT)
    menu = tk.OptionMenu(self.cntrl_frame, self.universe, *self.universe_list, command=self.set_universe)
#     menu.config(width=1)
    menu.pack(side = tk.LEFT)
    function = lambda : self.ola_thread.run_discovery(self.universe.get(), self.upon_discover)
    discover_button = tk.Button( self.cntrl_frame, text="Discover", command=function,  width=8 )
    discover_button.pack(side = tk.LEFT)
    self.dev_label = tk.StringVar(self.root)
    self.dev_label.set('Devices')
    self.device_menu = tk.OptionMenu(self.cntrl_frame, self.dev_label, [])
    self.device_menu.pack(side = tk.LEFT)
    self.id_box = tk.Checkbutton(self.cntrl_frame, text='Identify', variable=self.id_state, command=self.toggle_ident )
    self.id_box.pack(side = tk.LEFT)
    tk.Button( self.cntrl_frame, text = 'Redisplay Info', command = lambda : self.display_info(self.cur_uid) ).pack(side = tk.LEFT)
    tk.Label( self.cntrl_frame, text='Automatic\nDiscovery' ).pack(side = tk.LEFT)
    tk.Checkbutton(self.cntrl_frame).pack(side = tk.LEFT)

    
  def upon_discover(self, status, uids):
    '''
    callback for client.RunRDMDiscovery
    '''
    print 'discovered'
    self.device_menu['menu'].delete(0,'end')
    for uid in uids:
      self._uid_dict[uid] = {}
      self.ola_thread.rdm_get(self.universe.get(), uid, 0, 0x0082, lambda b, s, uid = uid: self.add_device(uid, b, s))
    self.cur_uid = uids[0] # initial value
    
  def add_device(self, uid, succeeded, data):
    '''
    adds device name to self.devicenames
    '''
    if succeeded == True:
      self._uid_dict[uid] = {'device label': data['label']}
      self.device_menu['menu'].add_command( label = '%s (%s)' %(data['label'], uid), 
                               command = lambda : self.device_selected(uid) )

  def identify(self, uid, succeeded, value):
    if succeeded:
      self.id_state.set(value['identify_state'])

  def set_universe(self, i):
    '''
    sets the int var self.universe to the value of i
    '''
    self.universe.set(i)
        
  def device_selected(self, uid):
    '''
    this function will be called by self.device_menu and will display the information for
    a particular device in the botton half of the GUI
    '''
    if uid == self.cur_uid:
      return
    self.dev_label.set('%s (%s)' %(self._uid_dict[uid]['device label'], uid))
    print 'uid: %s\ncur_uid: %s\nid_state: %d' % (uid, self.cur_uid, self.id_state.get())
    self.ola_thread.rdm_get(self.universe.get(), uid, 0, 0x1000, lambda b, s, uid = uid: self.identify(uid, b, s))
    self.cur_uid = uid
    print 'display info'
  
  def toggle_ident(self):
    print 'toggle'
    print self.cur_uid
    if self.cur_uid is None:
      return
    else:
      self.ola_thread.rdm_set(self.universe.get(), self.cur_uid, 0, 0x1000, lambda b, s, uid = self.cur_uid: self.identify(uid, b, s), [self.id_state.get()])

  def main(self):
    print 'Entering main loop'
    self.root.mainloop()  

if __name__ == '__main__':
  display = DisplayApp(800, 600)
  display.main()