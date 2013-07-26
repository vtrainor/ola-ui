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

"""
 General control flow:

 On startup:
   - fetch the list of UIDS
   - for each UID, fetch the DEVICE_LABEL
   - add each UID & add UID (+ optional label) to the drop down

 When a UID is selected:
  - fetch supported params if we don't already have it
  - fetch device info if we don't already have it
  - call notebook.Update()
  - notebook.Update looks at the current selected tab, and then calls one of:
    - GetBasicInformation()
    - GetDmxInformation()
    - GetSensorInformation()

 Each of these send the necessary to build a dictionary (pid_info) for the tab.
 For example, GetBasicInformation() would do:
    GET PRODUCT_DETAIL_ID_LIST
    GET -PRODUCT_DETAIL_ID_LIST
    GET MANUFACTURER_LABEL
    GET SOFTWARE_VERSION_LABEL
    GET BOOT_SOFTWARE_VERSION_ID
    GET BOOT_SOFTWARE_VERSION_LABEL

  Once the dict is built, we call notebook.RenderBasicInformation(pid_info)
  which then updates all the widgets.
"""

class Controller(object):
  """The controller will act as the glue between the notebook (display) the the
     DisplayApp (data). This keeps us honest by not leaking RDM information
     into the notebook.
  """
  def __init__(self, app):
    self._app = app

  def GetBasicInformation(self):
    """
    // "DEVICE_INFO"
    "PRODUCT_DETAIL_ID_LIST"
    "DEVICE_MODEL_DESCRIPTION"
    "MANUFACTURER_LABEL"
    "DEVICE_LABEL"
    "FACTORY_DEFAULTS"
    "SOFTWARE_VERSION_LABEL"
    "BOOT_SOFTWARE_VERSION_ID"
    "BOOT_SOFTWARE_VERSION_LABEL"
    """
    print 'Getting basic info'
    # TODO: 8 Call info DisplayApp and fetch each of the following PIDs, adding
    # them to the ]uid_dict. When you have a response for all pids print out the
    # uid_dict
    # self._app.GetBasicInformation()
    self._app.GetBasicInformation()

  def RenderBasicInformation(self):
    """
    """
    print "rendering basic information"

  def GetDmxInformation(self):
    pass

  def GetSensorInformation(self):
    pass

  def SetDeviceLabel(self, index):
    pass

  def SetSetStartAddress(self, index):
    pass

  def SetPersonality(self, index):
    pass

  # Additional methods will be added later

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
    self._controller = Controller(self)
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
    #self.rdm_notebook = notebook.RDMNotebook(self.root, self._controller)
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
    # This line is going to return "DEVICE_LABEL" so you may as well skip it
    pid_key = self._pid_store.GetName("DEVICE_LABEL", uid.manufacturer_id).name
    self.dev_label.set("%s (%s)"%(self._uid_dict[uid][pid_key], uid))
    self.ola_thread.rdm_get(self.universe.get(), uid, 0, "IDENTIFY_DEVICE", 
                  lambda b, s, uid = uid:self._get_identify_complete(uid, b, s),
                  [])
    if "SUPPORTED_PARAMETERS" not in self._uid_dict[uid]:
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
        self.ola_thread.rdm_get(self.universe.get(), uid, 0, "DEVICE_LABEL", 
                             lambda b, s, uid = uid:self._add_device(uid, b, s),
                             [])

  def _add_device(self, uid, succeeded, data):
    """ callback for the rdm_get in upon_discover.
        populates self.device_menu
    """
    # self._uid_dict[uid]  =  {"label": "", "supported_params": [], ...}
    # TODO: If this fails, we should still add the device, just use the UID
    if succeeded:
      self._uid_dict.setdefault(uid, {})["DEVICE_LABEL"] = data["label"]
      self.device_menu["menu"].add_command( label = "%s (%s)"%(
                  self._uid_dict[uid]["DEVICE_LABEL"], uid), 
                  command = lambda:self.device_selected(uid))
    else:
      self._uid_dict.setdefault(uid, {})["DEVICE_LABEL"] = ""
      self.device_menu["menu"].add_command( label = "%s" % uid, 
                  command = lambda:self.device_selected(uid))
    self._uid_dict[uid]["index"] = self.device_menu["menu"].index(tk.END)
    print "index: %d" % self._uid_dict[uid]["index"]
    if self.cur_uid is None:
      self.cur_uid = uid

  def _get_pids_complete(self, uid, succeeded, params):
    """ Callback for get_supported_pids.

        Args:
          succeeded: bool,  whether or not the get was a success
          params: packed list of 16-bit pids
    """
    if not succeeded:
      return
    else:
      # TODO: 5: 
      device = self._uid_dict[uid]
      device['SUPPORTED_PARAMETERS'] = set()
      for param_id in params["params"]:
        device["SUPPORTED_PARAMETERS"].add(param_id["param_id"])

      # TODO: 6 fetch DEVICE_INFO and a call _get_device_info_complete (added
      # below)
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, 
                "DEVICE_INFO", 
                lambda b, s, uid = 
                self.cur_uid:self._get_device_info_complete(uid, b, s, params), 
                [])
      

  def _get_device_info_complete(self, uid, succeeded, value, params) :
    # TODO: 7 add this information to the _uid_dict
    self._uid_dict[uid]["DEVICE_INFO"] = value
    # at this point we now have the list of supported parameters & the device
    # info for the pid selected.

    # TODO: 8 print the uid dict here
    print "uid_dict: %s" % self._uid_dict
    # Now for testing purposes, we skip the call though the notebook and just
    # proceed straight to getting the Basic Info
    self._controller.GetBasicInformation()

    pass

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
    print "value: %s" % value
    print "rdm set complete"

  def GetBasicInformation(self):
    """
    We want the following
      "DEVICE_INFO"
      "PRODUCT_DETAIL_ID_LIST"
      "DEVICE_MODEL_DESCRIPTION"
      "MANUFACTURER_LABEL"
      "DEVICE_LABEL"
      "FACTORY_DEFAULTS"
      "SOFTWARE_VERSION_LABEL"
      "BOOT_SOFTWARE_VERSION_ID"
      "BOOT_SOFTWARE_VERSION_LABEL"
    """
    self._get_product_detail_id()

  def _get_product_detail_id(self):
    pid_key = self._pid_store.GetName("PRODUCT_DETAIL_ID_LIST")
    print "pid: %s" % pid_key.name
    print "current uid: %s" % self.cur_uid
    if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self.rdm_product_detail_id_complete(b, s))
    else:
      self._get_device_model()

  def _get_product_detail_id_complete(self, succeeded, data):
    if succeeded:
      print "got product detail ids"
      self_uid_dict[self.cur_uid]["PRODUCT_DETAIL_ID_LIST"] = data["detail_ids"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_device_model()

  def _get_device_model (self):
    pid_key = self._pid_store.GetName("DEVICE_MODEL_DESCRIPTION")
    if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_device_model_complete(b, s))
    else:
      self._get_manufacturer_label()

  def _get_device_model_complete(self, succeeded, data):
    if succeeded:
      print "got device model"
      self_uid_dict[self.cur_uid]["DEVICE_MODEL_DESCRIPTION"] = data["description"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_manufacturer_label()

  def _get_manufacturer_label(self):
    pid_key = self._pid_store.GetName("MANUFACTURER_LABEL")
    if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_manufactuer_label_complete(b, s))
    else:
      self._get_factory_defaults()

  def _get_manufacturer_label_complete(self, succeeded, data):
    if succeeded:
      print "got device model description"
      self_uid_dict[self.cur_uid]["DEVICE_MODEL_DESCRIPTION"] = data["label"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_factory_defaults()

  def _get_factory_defaults(self):
    pid_key = self._pid_store.GetName("FACTORY_DEFAULTS")
    if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_factory_defaults_complete(b, s))
    else:
      self._get_software_version()

  def _get_factory_defaults_complete(self, succeeded, data):
    if succeeded:
      print ""
      self_uid_dict[self.cur_uid]["FACTORY_DEFAULTS"] = data["using_defaults"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_software_version()

  # def _get_language_capabilities(self):
  #   pid_key = self._pid_store.GetName("LANGUAGE_CAPABILITIES")
  #   if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
  #     self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
  #           lambda b, s: self._get_language_capabilities_complete(b, s), [""])
  #   else:
  #     self._get_software_version()

  # def _get_language_capabilities_complete(self, succeeded, data):
  #   if succeeded:
  #     print ""
  #     self_uid_dict[self.cur_uid]["LANGUAGE_CAPABILITIES"] = data["languages"]
  #   else:
  #     print "failed"
  #   # store the results in the uid dict
  #   self._get_language()

  # def _get_language(self):
  #   pid_key = self._pid_store.GetName("LANGUAGE")
  #   if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
  #     self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
  #           lambda b, s: self._get_language_complete(b, s), [""])
  #   else:
  #     self._get_software_version()

  # def _get_language_complete(self, succeeded, data):
  #   if succeeded:
  #     print ""
  #     self_uid_dict[self.cur_uid]["SUPPORTED_PARAMETERS"] = data["language"]
  #   else:
  #     print "failed"
  #   # store the results in the uid dict
  #   self._get_software_version()

  def _get_software_version(self):
    pid_key = self._pid_store.GetName("SOFTWARE_VERSION_LABEL")
    if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get__complete(b, s))
    else:
      self._get_boot_version()

  def _get_software_version_complete(self, succeeded, data):
    if succeeded:
      print ""
      self_uid_dict[self.cur_uid]["SOFTWARE_VERSION_LABEL"] = data["label"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_boot_version()

  def _get_boot_version(self):
    pid_key = self._pid_store.GetName("BOOT_SOFTWARE_VERSION")
    if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get__complete(b, s))
    else:
      self._get_boot_label()

  def _get_boot_version_complete(self, succeeded, data):
    if succeeded:
      print ""
      self_uid_dict[self.cur_uid]["BOOT_SOFTWARE_VERSION"] = data["value"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_boot_label()

  def _get_boot_label(self):
    pid_key = self._pid_store.GetName("BOOT_SOFTWARE_LABEL")
    if pid_key.name in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']:
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get__complete(b, s))
    else:
      self._controller.RenderBasicInformation()

  def _get_boot_label_complete(self, succeeded, data):
    if succeeded:
      print ""
      self_uid_dict[self.cur_uid]["BOOT_SOFTWARE_LABEL"] = data["label"]
    else:
      print "failed"
    # store the results in the uid dict
    self._controller.RenderBasicInformation()


  def main(self):
    print "Entering main loop"
    self.root.mainloop()

if __name__  ==  "__main__":
  display  =  DisplayApp(800, 600)
  display.main()
