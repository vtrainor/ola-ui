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
    self.universe_dict = {}
    self.cur_uid = None
    self.id_state = tk.IntVar(self.root)
    self.auto_disc = tk.BooleanVar(self.root)
    self.id_state.set(0)
#     self.state  =  0
    self._uid_dict = {}
    
    # Call initialing functions
    self.build_frames()
    self.build_cntrl()
    self._notebook = notebook.RDMNotebook(self.root, self._controller)

    self._pid_store = PidStore.GetStore()
    self.ola_thread = olathread.OLAThread(self._pid_store)
    self.ola_thread.start()


    self.auto_disc.set(False)
    self.fetch_universes(self.fetch_universes_complete)

    print "currently in thread: %d" % threading.currentThread().ident
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
    universes = self.universe_dict.keys()
    print universes
    self.universe_menu = tk.OptionMenu(self.cntrl_frame, self.universe, [])
    self.universe_menu.pack(side = tk.LEFT)
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

  def _device_changed_complete(self):
    """
    """
    self._uid_dict[self.cur_uid]["PARAM_NAMES"] = set()
    for pid_key in self._uid_dict[self.cur_uid]["SUPPORTED_PARAMETERS"]:
      pid = self._pid_store.GetPid(pid_key)
      if pid is not None:
        self._uid_dict[self.cur_uid]["PARAM_NAMES"].add(pid.name)
    print "Device selected: %s" % self._uid_dict[self.cur_uid]
    self._notebook.Update()

  def fetch_universes(self, callback):
    """
    """
    self.ola_thread.fetch_universes(self.fetch_universes_complete)

  def fetch_universes_complete(self, succeeded, universes):
    """
    """
    if succeeded:
      for universe in universes:
        self.universe_dict[universe.id] = []
        self.universe_menu["menu"].add_command(label = universe.id,
                                      command = self._set_universe(universe.id))
      self.universe.set(universes[0].id)

  def _set_universe(self, i):
    """ sets the int var self.universe to the value of i """
    self.universe.set(i)
    if not self.universe_dict[i]:
      self.discover()
    else: 
      for uid in self.universe_dict[i]:
        self._add_device(uid, True, self._uid_dict[uid]["DEVICE_LABEL"])

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
    if not uids:
      self.device_menu["menu"].delete(0, "end")
    for uid in uids:
      self.universe_dict[self.universe.get()].append(uid)
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
      dmx_actions.append(actions.GetPersonalityDescription(
                                                  data, 
                                                  self.ola_thread.rdm_get, 
                                                  i + 1))
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
    """
    if self.cur_uid is None:
      print "you need to select a device."
      return
    sensor_actions = []
    data = self._uid_dict[self.cur_uid]
    for i in xrange(data["DEVICE_INFO"]["sensor_count"]):
      sensor_actions.append(actions.GetSensorDefinition(
                                                    data, 
                                                    self.ola_thread.rdm_get,
                                                    i + 1))
      sensor_actions.append(actions.GetSensorValue(
                                                  data, 
                                                  self.ola_thread.rdm_get,
                                                  i + 1))
    flow = controlflow.RDMControlFlow(
                self.universe.get(),
                self.cur_uid,
                sensor_actions,
                self.UpdateSensorInformation)
    flow.Run()

  def GetSettingInformation(self):
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
                  actions.GetDeviceHours(data, self.ola_thread.rdm_get),
                  actions.GetLampHours(data, self.ola_thread.rdm_get),
                  actions.GetLampState(data, self.ola_thread.rdm_get),
                  actions.GetLampOnMode(data, self.ola_thread.rdm_get),
                  actions.GetPowerCycles(data, self.ola_thread.rdm_get),
                  actions.GetPowerState(data, self.ola_thread.rdm_get),
                  ],
                  self.UpdateSettingInformation)
    flow.Run()

 
  def GetConfigInformation(self):
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
                  actions.GetLanguageCapabilities(data, self.ola_thread.rdm_get),
                  actions.GetLanguage(data, self.ola_thread.rdm_get),
                  actions.GetDisplayInvert(data, self.ola_thread.rdm_get),
                  actions.GetDisplayLevel(data, self.ola_thread.rdm_get),
                  actions.GetPanInvert(data, self.ola_thread.rdm_get),
                  actions.GetTiltInvert(data, self.ola_thread.rdm_get),
                  actions.GetPanTiltSwap(data, self.ola_thread.rdm_get)
                  ],
                  self.UpdateConfigInformation)
    flow.Run()

  def UpdateBasicInformation(self):
    self._notebook.RenderBasicInformation(self._uid_dict[self.cur_uid])

  def UpdateDmxInformation(self):
    self._notebook.RenderDMXInformation(self._uid_dict[self.cur_uid])

  def UpdateSensorInformation(self):
    self._notebook.RenderSensorInformation(self._uid_dict[self.cur_uid])

  def UpdateSettingInformation(self):
    self._notebook.RenderSettingInformation(self._uid_dict[self.cur_uid])

  def UpdateConfigInformation(self):
    self._notebook.RenderConfigInformation(self._uid_dict[self.cur_uid])

  def set_device_label(self, label):
    """
    """
    uid = self.cur_uid
    callback = (lambda b, s, label = label, uid = uid:
                              self.set_device_label_complete(uid, label, b, s))
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

  def main(self):
    print "Entering main loop"
    self.root.mainloop()

if __name__  ==  "__main__":
  display  =  DisplayApp(800, 600)
  display.main()
