import Tkinter as tk
from ola.ClientWrapper import ClientWrapper
import time
import threading
import thread
import Queue
import olathread
from ola import PidStore
import ttk
import notebook

class DisplayApp:
  """ Creates the GUI for sending and receiving RDM messages through the
      ola thread. 
  """
  def __init__(self, width, height):
    """ initializes the GUI and the ola thread
    
    Args:
      width: the int value of the width of the tkinter window
      height: the int value of the height of the tkinter window
    """
    # Initialize the tk root window
    self.root = tk.Tk()
    self.init_dx = width
    self.init_dy = height
    self.root.geometry("%dx%d+50+30"%(self.init_dx, self.init_dy))
    self.root.title("RDM user interface version: 1.0")
    self.root.maxsize(1600, 900)
    self.root.lift()
    self.root.update_idletasks()
    # Assigning fields
    self.universe = tk.IntVar(self.root)
    self.universe.set(1)
    self.universe_list = [1, 2, 3, 4, 5]
    self.cur_uid = None
    self.id_state = tk.IntVar(self.root)
    self.auto_disc = tk.BooleanVar(self.root)
    self.id_state.set(0)
#     self.state  =  0
    self._uid_dict = {}
    
    # Call initialing functions
    self._pid_store = PidStore.GetStore()
    self.ola_thread = olathread.OLAThread(self._pid_store)
    self.ola_thread.start()
    self.build_frames()
    self.build_cntrl()
    #self.rdm_notebook = notebook.RDMNotebook(self.root)
    self.discover()
    self.auto_disc.set(False)

    print "currently in thread: %d"%threading.currentThread().ident
    time.sleep(1)
    print "back from sleep"

  def build_frames(self):
    """ builds the two tkinter frames that are used as parents for the
       tkinter widgets that both control and display the RDM messages.
    """
    self.cntrl_frame = tk.PanedWindow(self.root)
    self.cntrl_frame.pack(side = tk.TOP, padx = 1, pady = 1, fill = tk.Y)
    self.info_frame_1 = tk.PanedWindow(self.root)
    self.info_frame_1.pack(side = tk.TOP, padx = 1, pady = 2, fill = tk.Y)
    
  def build_cntrl(self):
    """ Builds the top bar of the GUI.

    Initializes all the general tkinter control widgets,  including:
      dev_label: tk string variable for the currently selected device
      id_box:
      device_menu:
    """
    tk.Label(self.cntrl_frame, text = "Select\nUniverse:").pack(side = tk.LEFT)
    menu = tk.OptionMenu(self.cntrl_frame, self.universe, *self.universe_list, 
                       command = self.set_universe)
    menu.pack(side = tk.LEFT)
    discover_button = tk.Button(self.cntrl_frame, text = "Discover", 
                                command = self.discover)
    discover_button.pack(side = tk.LEFT)
    self.dev_label = tk.StringVar(self.root)
    self.dev_label.set("Devices")
    self.device_menu = tk.OptionMenu(self.cntrl_frame, self.dev_label, [])
    self.device_menu.pack(side = tk.LEFT)
    self.id_box = tk.Checkbutton(self.cntrl_frame, text = "Identify", 
                                 variable = self.id_state, 
                                 command = self.identify)
    self.id_box.pack(side = tk.LEFT)
    self.auto_disc_box = tk.Checkbutton(self.cntrl_frame, 
                                        text = "Automatic\nDiscovery",
                                        variable = self.auto_disc, 
                                        command = self.discover)
    self.auto_disc_box.pack(side = tk.LEFT)

  def device_selected(self, uid):
    """ called when a new device is chosen from dev_menu.

      Args: 
        uid: the uid of the newly selected device
    """
    if uid == self.cur_uid:
      print "this device is already selected"
      return
    print "uid: %s\ncur_uid: %s\nid_state: %d"%(uid, self.cur_uid, 
                                                self.id_state.get())
    pid_key = self._pid_store.GetName("DEVICE_LABEL", uid.manufacturer_id).name
    self.dev_label.set("%s (%s)"%(self._uid_dict[uid][pid_key], uid))
    self.ola_thread.rdm_get(self.universe.get(), uid, 0, "IDENTIFY_DEVICE", 
                  lambda b, s, uid = uid:self._get_identify_complete(uid, b, s),
                  [])
    if self._uid_dict[uid]["SUPPORTED_PARAMETERS"] == []:
      self.ola_thread.rdm_get(self.universe.get(), uid, 0, 
                      "SUPPORTED_PARAMETERS", 
                      lambda b, l, uid = uid:self._get_pids_complete(uid, b, l),
                      [])
    self.cur_uid = uid
    # init callbacks

  def set_universe(self, i):
    """ sets the int var self.universe to the value of i """
    self.universe.set(i)

  def discover(self):
    """ runs discovery for the current universe. """
    self.ola_thread.run_discovery(self.universe.get(), self._upon_discover)
    if self.auto_disc.get():
      self.ola_thread.add_event(5000, self.discover)
    else: 
      print "auto_disc is off"

  def identify(self):
    """ Command is called by id_box.

        sets the value of the device"s identify field based on the value of 
        id_box.
    """
    if self.cur_uid is None:
      return
    self.ola_thread.rdm_set(self.universe.get(), self.cur_uid, 0, 
              "IDENTIFY_DEVICE", 
              lambda b, s, uid = self.cur_uid:self._rdm_set_complete(uid, b, s), 
              [self.id_state.get()])

  def _upon_discover(self, status, uids):
    """ callback for client.RunRDMDiscovery. """
    print "discovered"
    if len(self._uid_dict.keys()) == 0:
      self.device_menu["menu"].delete(0, "end")
    for uid in uids:
      if uid not in self._uid_dict.keys():
        print "adding device..."
        self._uid_dict[uid] = {}
        self._uid_dict[uid]["supported_pids"] = []
        self.ola_thread.rdm_get(self.universe.get(), uid, 0, 
                      "SUPPORTED_PARAMETERS", 
                      lambda b, l, uid = uid:self._get_pids_complete(uid, b, l),
                      [])
        self.ola_thread.rdm_get(self.universe.get(), uid, 0, "DEVICE_LABEL", 
                             lambda b, s, uid = uid:self._add_device(uid, b, s),
                             [])

  def _add_device(self, uid, succeeded, data):
    """ callback for the rdm_get in upon_discover.
        populates self.device_menu
    """
    # self._uid_dict[uid]  =  {"label": "", "supported_params": [], ...}
    if succeeded:
      self._uid_dict.setdefault(uid, {})["DEVICE_LABEL"] = data["label"]
      self.device_menu["menu"].add_command( label = "%s (%s)"%(
                  self._uid_dict[uid]["DEVICE_LABEL"], uid), 
                  command = lambda:self.device_selected(uid))
      self._uid_dict[uid]["index"] = self.device_menu["menu"].index(tk.END)
      print "index: %d" % self._uid_dict[uid]["index"]
      if self.cur_uid is None:
        self.cur_uid = uid
        self.rdm_notebook.set_callbacks(
                    lambda pid, callback: self.notebook_rdm_get(pid, callback),
                    lambda pid, data: self.notebook_rdm_set(pid, data))
        self.rdm_notebook.populate_defaults()

  def _get_pids_complete(self, uid, succeeded, params):
    """ Callback for get_supported_pids.

        Args:
          succeeded: bool,  whether or not the get was a success
          params: packed list of 16-bit pids
    """
    if not succeeded:
      return

    # TODO: 5: first add the list of supported parameters to the uid dict:
    # device = self._uid_dict[uid]
    # device['SUPPORTED_PARAMETERS'] = set( .... )

    # TODO: 6 fetch DEVICE_INFO and a call _get_device_info_complete (added
    # below)

    return

    pid_list = params["params"]
    for pid in ["DEVICE_INFO"]: # list of required pids
      self._uid_dict[uid][pid] = []
    for item in pid_list:
      try:
        pid = self._pid_store.GetPid(item["param_id"], uid.manufacturer_id).name
      except:
        print "manufactuer pid"
      if pid in ["RECORD_SENSORS", "RESET_DEVICE", "CAPTURE_PRESET"]:
        pass
      else: 
        self._uid_dict[uid][pid] = []

  def _get_device_info_complete(self, uid, succeeded, params) :
    # TODO: 7 add this information to the _uid_dict

    # at this point we now have the list of supported parameters & the device
    # info for the pid selected.

  def _get_value_complete(self, pid, succeeded, value):
    """ Callback for get_pid_value. """
    if not succeeded:
      print "did not succeed"
      return
    elif succeeded:
      print "pid: %s" % pid
      print "value: %s" % value
      self._uid_dict[self.cur_uid][pid] = value
      print self._uid_dict[self.cur_uid][pid]
      self.rdm_notebook.update_tabs(value, [pid])

  def _get_identify_complete(self, uid, succeeded, value):
    """ Callback for rdm_get in device_selected.

        Sets the checkbox"s state to that of the currently selected device
    """
    if succeeded: 
      self.id_state.set(value["identify_state"])

  def _rdm_set_complete(self, uid, succeded, value):
    """ callback for the rdm_set in identify. """
    print "value: %s" % (succeded, value)
    print "rdm set complete"

  def notebook_rdm_get(self, pid, callback):
    """
    """
    data = self._uid_dict[self.cur_uid][pid]
    self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid, 
               lambda b, s, pid = pid:self.rdm_get_complete(pid, b, s), [data])

  def notebook_rdm_set(self, pid, data):
    """
    """
    print "current uid: %s\npid: %s" % (self.cur_uid, pid)
    self._uid_dict[self.cur_uid][pid] = data
    data = self._uid_dict[self.cur_uid][pid]
    self.ola_thread.rdm_set(self.universe.get(), self.cur_uid, 0, pid, 
               lambda b, s, pid = pid:self.rdm_get_complete(pid, b, s), [data])

  def notebook_rdm_get_complete(self, pid, succeeded, value):
    """
    """
    if succeeded:
      self.self._uid_dict[self.cur_uid][pid] = value
      self.rdm_notebook.update_tabs(pid, value)
    else:
      print "!!failed message!!\npid: %s\nvalue: %s" % (pid, value)


  def notebook_rdm_set_complete(self):
    """
    """
    pass

  def main(self):
    print "Entering main loop"
    self.root.mainloop()

if __name__  ==  "__main__":
  display  =  DisplayApp(800, 600)
  display.main()
