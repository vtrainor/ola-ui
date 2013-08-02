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
import controlflow
import actions

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
    - GetDMXInformation()
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
    """
    self._app.GetBasicInformation()

  def GetDMXInformation(self):
    """
    """
    self._app.GetDMXInformation()

  def GetSensorsInformation(self):
    self._app.GetSensorsInformation()

  def GetSettingInformation(self):
    self._app.GetSettingInformation()

  def GetConfigInformation(self):
    self._app.GetConfigInformation()


  def SetDeviceLabel(self, label):
    """
    """
    self._app.set_device_label(label)

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
    self._notebook = notebook.RDMNotebook(self.root, self._controller)
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
    # self.device_menu["menu"].config(tearoff = 0)
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
      print "Already Selected"
      return
    pid_key = "DEVICE_LABEL"
    self.dev_label.set("%s (%s)"%(self._uid_dict[uid][pid_key], uid))
    self.ola_thread.rdm_get(self.universe.get(), uid, 0, "IDENTIFY_DEVICE", 
                  lambda b, s, uid = uid:self._get_identify_complete(uid, b, s))
    data = self._uid_dict[uid]
    flow = controlflow.RDMControlFlow(
                            self.universe.get(), 
                            uid, 
                            [
                            actions.GetSupportedParams(data, self.ola_thread.rdm_get),
                            actions.GetDeviceInfo(data, self.ola_thread.rdm_get)
                            ],
                            self._device_changed_complete)
    flow.Run()
    self.cur_uid = uid

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
    if len(self._uid_dict.keys()) == 0:
      self.device_menu["menu"].delete(0, "end")
    for uid in uids:
      if uid not in self._uid_dict.keys():
        self._uid_dict[uid] = {}
        self.ola_thread.rdm_get(self.universe.get(), uid, 0, "DEVICE_LABEL", 
                             lambda b, s, uid = uid:self._add_device(uid, b, s),
                             [])

  def _add_device(self, uid, succeeded, data):
    """ callback for the rdm_get in upon_discover.
        populates self.device_menu
    """
    # TODO: Bug: on discover the label in the label in the device option menu 
    #       doesn't change and if you try to select the first device it tells 
    #       you that it is already selected
    if succeeded:
      self._uid_dict.setdefault(uid, {})["DEVICE_LABEL"] = data["label"]
      self.device_menu["menu"].add_command( label = "%s (%s)"%(
                  self._uid_dict[uid]["DEVICE_LABEL"], uid), 
                  command = lambda:self.device_selected(uid))
    else:
      self._uid_dict.setdefault(uid, {})["DEVICE_LABEL"] = {"label":""}
      self.device_menu["menu"].add_command( label = "%s" % uid, 
                                    command = lambda:self.device_selected(uid))
    self._uid_dict[uid]["index"] = self.device_menu["menu"].index(tk.END)

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
    """
    if self.cur_uid is None:
    	print "you need to select a device"
    	return
    data = self._uid_dict[self.cur_uid]
    flow = controlflow.RDMControlFlow(
                  self.universe.get(), 
                  self.cur_uid, 
                  [
                  actions.GetProductDetailIds(data, self.ola_thread.rdm_get),
                  actions.GetDeviceModel(data, self.ola_thread.rdm_get),
                  actions.GetManufacturerLabel(data, self.ola_thread.rdm_get),
                  actions.GetFactoryDefaults(data, self.ola_thread.rdm_get),
                  actions.GetSoftwareVersion(data, self.ola_thread.rdm_get),
                  actions.GetBootSoftwareLabel(data, self.ola_thread.rdm_get),
                  actions.GetBootSoftwareVersion(data, self.ola_thread.rdm_get)
                  ],
                  self.UpdateBasicInformation)
    flow.Run()
  
  def GetDMXInformation(self):
    """
    """
    if self.cur_uid is None:
      print "you need to select a device."
      return
    dmx_actions = []
    data = self._uid_dict[self.cur_uid]
    dmx_actions.append(actions.GetDmxPersonality(data, self.ola_thread.rdm_get))
    for i in xrange(data["DEVICE_INFO"]["personality_count"]):
      dmx_actions.append(actions.GetPersonalityDescription(data, 
                                                  self.ola_thread.rdm_get, i + 1,))
    dmx_actions.append(actions.GetStartAddress(data, self.ola_thread.rdm_get))
    dmx_actions.append(actions.GetSlotInfo(data, self.ola_thread.rdm_get))
    dmx_actions.append(actions.GetSlotDescription(
                                                  data, 
                                                  self.ola_thread.rdm_get))
    # dmx_actions.append(actions.GetDefaultSlotValue(data, 
    #                                                 self.ola_thread.rdm_get))
    flow = controlflow.RDMControlFlow(
                self.universe.get(),
                self.cur_uid,
                dmx_actions,
                self.UpdateDmxInformation)
    flow.Run()

  def GetSensorsInformation(self):
    """
    "SENSOR_DEFINITION"
    "SENSOR_VALUE"
    "RECORD_SENSORS"
    """
    if self.cur_uid is None:
      return

  def GetSettingInformation(self):
    """
    "DEVICE_HOURS"
    "LAMP_HOURS"
    "LAMP_STRIKES"
    "LAMP_STATE"
    "LAMP_ON_MODE"
    "DEVICE_POWER_CYCLES"
    "POWER_STATE"
    """
    if self.cur_uid is None:
      return
    self._get_device_hours()

  def _get_device_hours(self):
    pid_key = self._pid_store.GetName("DEVICE_HOURS")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DEVICE_HOURS" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_device_hours_complete(b, s))
    else:
      self._get_lamp_hours()

  def _get_device_hours_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["DEVICE_HOURS"] = data["hours"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_lamp_hours()

  def _get_lamp_hours(self):
    pid_key = self._pid_store.GetName("LAMP_HOURS")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "LAMP_HOURS" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_lamp_hours_complete(b, s))
    else:
      self._get_lamp_strikes()

  def _get_lamp_hours_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["LAMP_HOURS"] = data["hours"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_lamp_strikes()

  def _get_lamp_strikes(self):
    pid_key = self._pid_store.GetName("LAMP_STRIKES")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "LAMP_STRIKES" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_lamp_strikes_complete(b, s))
    else:
      self._get_lamp_state()

  def _get_lamp_strikes_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["LAMP_STRIKES"] = data["strikes"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_lamp_state()

  def _get_lamp_state(self):
    pid_key = self._pid_store.GetName("LAMP_STATE")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "LAMP_STATE" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_lamp_state_complete(b, s))
    else:
      self._get_lamp_on_mode()

  def _get_lamp_state_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["LAMP_STATE"] = data["state"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_lamp_on_mode()

  def _get_lamp_on_mode(self):
    pid_key = self._pid_store.GetName("LAMP_ON_MODE")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "LAMP_ON_MODE" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_lamp_on_mode_complete(b, s))
    else:
      self._get_power_cycles()

  def _get_lamp_on_mode_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["LAMP_ON_MODE"] = data["mode"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_power_cycles()

  def _get_power_cycles(self):
    pid_key = self._pid_store.GetName("DEVICE_POWER_CYCLES")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DEVICE_POWER_CYCLES" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_power_cycles_complete(b, s))
    else:
      self._get_power_state()

  def _get_power_cycles_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["DEVICE_POWER_CYCLES"] = data["power_cycles"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_power_state()

  def _get_power_state(self):
    pid_key = self._pid_store.GetName("POWER_STATE")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "POWER_STATE" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_power_state_complete(b, s))
    else:
      self._notebook.RenderSettingInformation(self._uid_dict[self.cur_uid])

  def _get_power_state_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["POWER_STATE"] = data["power_state"]
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.RenderSettingInformation(self._uid_dict[self.cur_uid])

  def GetConfigInformation(self):
    """
    "LANGUAGE_CAPABILITIES"
    "LANGUAGE"
    "DISPLAY_INVERT"
    "DISPLAY_LEVEL"
    "PAN_INVERT"
    "TILT_INVERT"
    "PAN_TILT_SWAP"
    "REAL_TIME_CLOCK"
    """
    if self.cur_uid is None:
      return

  def _get_language_capabilities(self):
    pid_key = self._pid_store.GetName("LANGUAGE_CAPABILITIES")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "LANGUAGE_CAPABILITIES" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_language_capabilities_complete(b, s))
    else:
      self._get_language()

  def _get_language_capabilities_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["LANGUAGE_CAPABILITIES"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_language()

  def _get_language(self):
    pid_key = self._pid_store.GetName("LANGUAGE")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "LANGUAGE" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_language_complete(b, s))
    else:
      self._get_display_invert()

  def _get_language_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["LANGUAGE"] = data["language"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_display_invert()

  def _get_display_invert(self):
    pid_key = self._pid_store.GetName("DISPLAY_INVERT")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DISPLAY_INVERT" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_display_invert_complete(b, s))
    else:
      self._get_display_level()

  def _get_display_invert_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["DISPLAY_INVERT"] = data["invert_status"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_display_level()

  def _get_display_level(self):
    pid_key = self._pid_store.GetName("DISPLAY_LEVEL")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DISPLAY_LEVEL" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_display_level_complete(b, s))
    else:
      self._get_pan_invert()

  def _get_display_level_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["DISPLAY_LEVEL"] = data["level"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_pan_invert()

  def _get_pan_invert(self):
    pid_key = self._pid_store.GetName("PAN_INVERT")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "PAN_INVERT" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_pan_invert_complete(b, s))
    else:
      self._get_tilt_invert()

  def _get_pan_invert_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["PAN_INVERT"] = data["invert"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_tilt_invert()

  def _get_tilt_invert(self):
    pid_key = self._pid_store.GetName("TILT_INVERT")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "TILT_INVERT" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_tilt_invert_complete(b, s))
    else:
      self._get_pan_tilt_swap()

  def _get_tilt_invert_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["TILT_INVERT"] = data["invert"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_pan_tilt_swap()

  def _get_pan_tilt_swap(self):
    pid_key = self._pid_store.GetName("PAN_TILT_SWAP")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "PAN_TILT_SWAP" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_pan_tilt_swap_complete(b, s))
    else:
      self._get_real_time()

  def _get_pan_tilt_swap_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["PAN_TILT_SWAP"] = data["swap"]
    else:
      print "failed"
    # store the results in the uid dict
    self._get_real_time()

  def _get_real_time(self):
    pid_key = self._pid_store.GetName("REAL_TIME_CLOCK")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "REAL_TIME_CLOCK" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), 
                              self.cur_uid,
                              0, 
                              pid_key.name, 
                              lambda b, s: self._get_real_time_complete(b, s)
                              )
    else:
      self._notebook.RenderConfigInformation(self._uid_dict[self.cur_uid])

  def _get_real_time_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["REAL_TIME_CLOCK"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.RenderConfigInformation(self._uid_dict[self.cur_uid])

  def set_device_label(self, label):
    """
    """
    uid = self.cur_uid
    callback = lambda b, s, label = label, uid = uid:self.set_device_label_complete(uid, label, b, s)
    self.ola_thread.rdm_set(self.universe.get(), 
                                  uid,
                                  0, 
                                  "DEVICE_LABEL", 
                                  callback,
                                  [label]
                                  )

  def set_device_label_complete(self, uid, label, succeeded, data):
    """
    """
    if succeeded:
      index = self._uid_dict[self.cur_uid]["index"]
      self._uid_dict[self.cur_uid]["DEVICE_LABEL"] = label
      self.device_menu["menu"].entryconfigure(index, label = "%s (%s)"%(
                  self._uid_dict[uid]["DEVICE_LABEL"], uid))
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.Update()

  def UpdateBasicInformation(self):
    self._notebook.RenderBasicInformation(self._uid_dict[self.cur_uid])

  def UpdateDmxInformation(self):
    self._notebook.RenderDMXInformation(self._uid_dict[self.cur_uid])

  def _device_changed_complete(self):
    """
    """
    print "Device selected: %s" % self._uid_dict
    self._uid_dict[self.cur_uid]["PARAM_NAMES"] = set()
    for pid_key in self._uid_dict[self.cur_uid]["SUPPORTED_PARAMETERS"]:
      pid = self._pid_store.GetPid(pid_key)
      if pid is not None:
        self._uid_dict[self.cur_uid]["PARAM_NAMES"].add(pid.name)

    self._notebook.Update()

  def main(self):
    print "Entering main loop"
    self.root.mainloop()

if __name__  ==  "__main__":
  display  =  DisplayApp(800, 600)
  display.main()
