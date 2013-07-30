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
    """
    self._app.GetBasicInformation()

  def GetDmxInformation(self):
    """
    """
    self._app.GetDmxInformation()

  def SetDeviceLabel(self, label):
    """
    """
    self._app.set_device_label(label)

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
    # This line is going to return "DEVICE_LABEL" so you may as well skip it
    pid_key = "DEVICE_LABEL"
    self.dev_label.set("%s (%s)"%(self._uid_dict[uid][pid_key]["label"], uid))
    self.ola_thread.rdm_get(self.universe.get(), uid, 0, "IDENTIFY_DEVICE", 
                  lambda b, s, uid = uid:self._get_identify_complete(uid, b, s))
    if self.cur_uid is None:
      self.cur_uid = uid
      self._controller.GetBasicInformation()
      return
    if "SUPPORTED_PARAMETERS" not in self._uid_dict[uid]:
      print "error 4:"
      return
    if "DEVICE_INFO" not in self._uid_dict[uid]:
      "error 3"
      self.cur_uid = uid
      self._controller.GetBasicInformation()
      return
    self._notebook.Update(self._uid_dict[uid], 0)

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
      self._uid_dict.setdefault(uid, {})["DEVICE_LABEL"] = data
      self.device_menu["menu"].add_command( label = "%s (%s)"%(
                  self._uid_dict[uid]["DEVICE_LABEL"]["label"], uid), 
                  command = lambda:self.device_selected(uid))
    else:
      self._uid_dict.setdefault(uid, {})["DEVICE_LABEL"] = {"label":""}
      self.device_menu["menu"].add_command( label = "%s" % uid, 
                                    command = lambda:self.device_selected(uid))
    self._uid_dict[uid]["index"] = self.device_menu["menu"].index(tk.END)
    if "SUPPORTED_PARAMETERS" not in self._uid_dict[uid]:
      self.ola_thread.rdm_get(self.universe.get(), uid, 0, 
                      "SUPPORTED_PARAMETERS", 
                    lambda b, l, uid = uid:self._get_pids_complete(uid, b, l),)
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
      if self.cur_uid is None:
        self._controller.GetBasicInformation()
      device = self._uid_dict[uid]
      device['SUPPORTED_PARAMETERS'] = set(p['param_id']
                                                     for p in params['params'])

      # TODO: 6 fetch DEVICE_INFO and a call _get_device_info_complete (added
      # below)
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, 
                "DEVICE_INFO", 
                lambda b, s, uid = 
                self.cur_uid:self._get_device_info_complete(uid, b, s))
      

  def _get_device_info_complete(self, uid, succeeded, value) :
    self._uid_dict[uid]["DEVICE_INFO"] = value
    # at this point we now have the list of supported parameters & the device
    # info for the pid selected.
    print "uid_dict: %s" % self._uid_dict
    # Now for testing purposes, we skip the call though the notebook and just
    # proceed straight to getting the Basic Info
    self._controller.GetBasicInformation()

    pass

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
    if self.cur_uid is None:
      return
    self._get_product_detail_id()

  def _get_product_detail_id(self):
    pid_key = self._pid_store.GetName("PRODUCT_DETAIL_ID_LIST")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
      and "PRODUCT_DETAIL_ID_LIST" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_product_detail_id_complete(b, s))
    else:
      self._get_device_model()

  def _get_product_detail_id_complete(self, succeeded, data):
    if succeeded:
      print "got product detail ids"
      self._uid_dict[self.cur_uid]["PRODUCT_DETAIL_ID_LIST"] = set(
                            value['detail_id'] for value in data['detail_ids'])
    else:
      print "failed"
    # store the results in the uid dict
    self._get_device_model()

  def _get_device_model (self):
    pid_key = self._pid_store.GetName("DEVICE_MODEL_DESCRIPTION")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
            and "DEVICE_MODEL_DESCRIPTION" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_device_model_complete(b, s))
    else:
      self._get_manufacturer_label()

  def _get_device_model_complete(self, succeeded, data):
    if succeeded:
      print "got device model"
      self._uid_dict[self.cur_uid]["DEVICE_MODEL_DESCRIPTION"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_manufacturer_label()

  def _get_manufacturer_label(self):
    pid_key = self._pid_store.GetName("MANUFACTURER_LABEL")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
      and "MANUFACTURER_LABEL" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(),
                      self.cur_uid, 
                      0, 
                      pid_key.name, 
                      lambda b, s: self._get_manufacturer_label_complete(b, s))
    else:
      self._get_factory_defaults()

  def _get_manufacturer_label_complete(self, succeeded, data):
    if succeeded:
      print "got device model description"
      self._uid_dict[self.cur_uid]["MANUFACTURER_LABEL"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_factory_defaults()

  def _get_factory_defaults(self):
    pid_key = self._pid_store.GetName("FACTORY_DEFAULTS")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
                    and "FACTORY_DEFAULTS" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_factory_defaults_complete(b, s))
    else:
      self._get_software_version()

  def _get_factory_defaults_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["FACTORY_DEFAULTS"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_software_version()

  def _get_software_version(self):
    pid_key = self._pid_store.GetName("SOFTWARE_VERSION_LABEL")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "SOFTWARE_VERSION_LABEL" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), 
                          self.cur_uid, 
                          0, 
                          pid_key.name, 
                          lambda b, s: self._get_software_version_complete(b, s)
                          )
    else:
      self._get_boot_version()

  def _get_software_version_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["SOFTWARE_VERSION_LABEL"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_boot_version()

  def _get_boot_version(self):
    pid_key = self._pid_store.GetName("BOOT_SOFTWARE_VERSION")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
              and "BOOT_SOFTWARE_VERSION" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), 
                              self.cur_uid, 
                              0, 
                              pid_key.name, 
                              lambda b, s: self._get_boot_version_complete(b, s)
                              )
    else:
      self._get_boot_label()

  def _get_boot_version_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["BOOT_SOFTWARE_VERSION"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_boot_label()

  def _get_boot_label(self):
    pid_key = self._pid_store.GetName("BOOT_SOFTWARE_LABEL")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
                and "BOOT_SOFTWARE_LABEL" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_boot_label_complete(b, s))
    else:
      self._notebook.RenderBasicInformation(self._uid_dict[self.cur_uid])

  def _get_boot_label_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["BOOT_SOFTWARE_LABEL"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.RenderBasicInformation(self._uid_dict[self.cur_uid])

  def GetDMXInformation(self):
    """
    // "DEVICE_INFO"
    "DMX_PERSONALITY"
    "DMX_PERSONALITY_DESCRIPTION"
    "DMX_START_ADDRESS"
    "SLOT_INFO"
    "SLOT_DESCRIPTION"
    "DEFAULT_SLOT_VALUE"
    """
    if self.cur_uid is None:
      return
    self._get_dmx_personality()

  def _get_dmx_personality(self):
    pid_key = self._pid_store.GetName("DMX_PERSONALITY")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DMX_PERSONALITY" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_dmx_personality_complete(b, s))
    else:
      self._get_personality_decription()

  def _get_dmx_personality_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["BOOT_SOFTWARE_LABEL"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_personality_description()

  def _get_personality_description(self):
    data = [self._uid_dict[self.cur_uid]["DMX_PERSONALITY"]["personality"]]
    pid_key = self._pid_store.GetName("DMX_PERSONALITY_DESCRIPTION")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DMX_PERSONALITY" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_personality_description_complete(b, s), data)
    else:
      self._get_start_address()

  def _get_personality_description_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["DMX_PERSONALITY_DESCRIPTION"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_start_address()

  def _get_start_address(self):
    pid_key = self._pid_store.GetName("DMX_START_ADDRESS")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DMX_START_ADDRESS" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_start_address_complete(b, s))
    else:
      self._get_slot_info()

  def _get_start_address_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["DMX_START_ADDRESS"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_slot_info()

  def _get_slot_info(self):
    pid_key = self._pid_store.GetName("SLOT_INFO")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "SLOT_INFO" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_slot_info_complete(b, s))
    else:
      self._get_slot_description()

  def _get_slot_info_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["SLOT_DESCRIPTION"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_slot_description()

  def _get_slot_description(self):
    pid_key = self._pid_store.GetName("SLOT_DESCRIPTION")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "SLOT_DESCRIPTION" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_slot_description_complete(b, s))
    else:
      self._get_default_slot_value()

  def _get_slot_description_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["SLOT_DESCRIPTION"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_defalut_slot_value()

  def _get_defalut_slot_value(self):
    pid_key = self._pid_store.GetName("DEFAULT_SLOT_VALUE")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "DEFAULT_SLOT_VALUE" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_default_value_complete(b, s))
    else:
      self._notebook.RenderDMXInformation(self._uid_dict[self.cur_uid])

  def _get_default_slot_value_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["DEFAULT_SLOT_VALUE"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.RenderDMXInformation(self._uid_dict[self.cur_uid])

  def GetSensorsInformation():
    """
    "SENSOR_DEFINITION"
    "SENSOR_VALUE"
    "RECORD_SENSORS"
    """
    if self.cur_uid is None:
      return

  def _get_sensor_definition(self):
    pid_key = self._pid_store.GetName("SENSOR_DEFINITION")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "SENSOR_DEFINITION" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_sensor_definition_complete(b, s))
    else:
      self._get_sensor_value()

  def _get_sensor_definition_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["SENSOR_DEFINITION"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._get_sensor_value()

  def _get_sensor_value(self):
    pid_key = self._pid_store.GetName("SENSOR_VALUE")
    if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
          and "SENSOR_VALUE" not in self._uid_dict[self.cur_uid]):
      self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
            lambda b, s: self._get_sensor_value_complete(b, s))
    else:
      self._notebook.RenderSensorInformation()
      # do I need to do anything with record sensors here?

  def _get_sensor_value_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["SENSOR_VALUE"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.RenderSensorInformation()

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
      self._uid_dict[self.cur_uid]["DEVICE_HOURS"] = data
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
      self._uid_dict[self.cur_uid]["LAMP_HOURS"] = data
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
      self._uid_dict[self.cur_uid]["LAMP_STRIKES"] = data
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
      self._uid_dict[self.cur_uid]["LAMP_STATE"] = data
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
      self._uid_dict[self.cur_uid]["LAMP_ON_MODE"] = data
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
      self._uid_dict[self.cur_uid]["DEVICE_POWER_CYCLES"] = data
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
      self._notebook.RenderSettingInformation

  def _get_power_state_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["POWER_STATE"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.RenderSettingInformation()

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
      self._uid_dict[self.cur_uid]["LANGUAGE"] = data
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
      self._uid_dict[self.cur_uid]["DISPLAY_INVERT"] = data
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
      self._uid_dict[self.cur_uid]["DISPLAY_LEVEL"] = data
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
      self._uid_dict[self.cur_uid]["PAN_INVERT"] = data
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
      self._uid_dict[self.cur_uid]["TILT_INVERT"] = data
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
      self._uid_dict[self.cur_uid]["PAN_TILT_SWAP"] = data
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
      self._notebook.RenderConfigInformation()

  def _get_real_time_complete(self, succeeded, data):
    if succeeded:
      print ""
      self._uid_dict[self.cur_uid]["REAL_TIME_CLOCK"] = data
    else:
      print "failed"
    # store the results in the uid dict
    self._notebook.RenderConfigInformation()

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
      self._uid_dict[self.cur_uid]["DEVICE_LABEL"]["label"] = label
      self.device_menu["menu"].entryconfigure(index, label = "%s (%s)"%(
                  self._uid_dict[uid]["DEVICE_LABEL"]["label"], uid))
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
